import numpy as np
import lightcones.linalg as la
from lightcones.solvers.schrodinger import solve

def spread(e, h, nt, dt):
    """
    Calculate the spread of operator

    Parameters:
    - e (numpy.ndarray of numpy.float64): array of on-site energies e[0] ... e[n_sites - 1]
    - h (numpy.ndarray of numpy.float64): array of hoppings h[0] ... h[n_sites - 2]
    - nt (int): number of time steps during which to compute spread
    - dt (float): size of one time step

    Returns:
    - numpy.ndarray of numpy.complex128: 2D array containing the spread of operator alpha[k, l] = \alpha(l*dt)_{k}
    """
    n_sites = len(e)
    # first-quantized Hamiltonian
    H = la.tridiag(e, h)

    # initial condition: quantum on site 0 of the chain
    phi_0 = np.zeros(n_sites, dtype = complex)
    phi_0[0] = 1 # initially quantum is on the site 0

    # Here we store the propagated orbitals (the spread)
    phi_lc = np.zeros((n_sites, nt), dtype = np.cdouble) 

    def apply_h(ti, phi_in, phi_out):
        la.mv(H, phi_in, phi_out, cout=1)

    def eval_o(ti, phi):
        phi_lc[:, ti] = phi
    
    solve(0, nt-1, dt, apply_h, phi_0, eval_o = eval_o)
    
    return phi_lc

def rho_plus(spread, dt):
    """
    Compute rho_plus given the spread of operator
    
    Parameters:
    - spread (numpy.ndarray of numpy.complex128): 2D array of coefficients spread[k, l] = \alpha(l*dt)_{k}
    - dt (float): size of one time step
    
    Returns:
    - numpy.ndarray of numpy.complex128: 2D array containing matrix elements for the rho_plus for the duration of the spread
    """
    
    # get dimensions
    n_sites, nt = spread.shape
    
    # here rho_plus will be stored
    rho_lc = np.zeros((n_sites, n_sites), dtype = np.cdouble)
    
    for i in range(0, nt):
        phi = la.as_column_vector(spread[:, i])
        rho_lc += la.dyad(phi, phi) * dt

    la.make_hermitean(rho_lc)

    return rho_lc

def minimal_forward_frame(spread, rho_plus, dt, rtol):
    """
    Compute the frame of a minimal light cone

    Parameters:
    - spread (numpy.ndarray of numpy.complex128): 2D array of coefficients spread[k, l] = \alpha(l*dt)_{k}
    - rho_plus (numpy.ndarray of numpy.complex128): 2D array containing matrix elements for the rho_plus for the duration of the spread
    - dt (float): size of one time step
    - rtol (float): relative cutoff treshold for the light cone boundary
    
    Returns:
    - numpy.ndarray of numpy.complex128: Unitary matrix U_min
    """
    
    # find the modes which manage to couple before the end of the
    # time interval
    pi, U_rel = la.find_largest_eigs(rho_plus)
    g_metric = pi - rtol * pi[0]
    inside_lightcone = g_metric > 0
    n_rel =  sum(inside_lightcone)
    
    # begin to construct the rotation U_min
    U_min = U_rel
    # also recompute the spread
    spread_min = U_min.T.conj() @ spread
    # and rho_plus 
    rho_plus_min = np.diag(pi[: n_rel].astype('cdouble'))

    # number of time steps
    ntg = np.size(spread, 1)

    # Here we store the arrival times
    times_in = []
    
    # Number of non-optimal modes
    # (which we continue to transform)
    n = n_rel
        
    # Propagate backwards in time
    for i in reversed(range(0, ntg)):
        pi_min, _ = la.find_smallest_eigs(rho_plus_min, 1)
        pi_max, _ = la.find_largest_eigs(rho_plus_min, 1)
        g_metric = pi_min - rtol * pi_max
        outside_lightcone = g_metric < 0

        if outside_lightcone:
            pi, U = la.find_eigs_descending(rho_plus_min)
            spread_min[: n, :] = U.T.conj() @ spread_min[: n, :]
            U_min[: n, :] = U.T.conj() @ U_min[: n, :]
            rho_plus_min = np.diag(pi[: -1].astype('cdouble'))
            times_in.insert(0, i + 1)
            n = n_rel - len(times_in)

        psi = la.as_column_vector(spread_min[: n, i])
        rho_plus_min -= la.dyad(psi, psi) * dt
        la.make_hermitean(rho_plus_min)
        
    times_in.append(ntg)
    
    return times_in, U_min, spread_min
    