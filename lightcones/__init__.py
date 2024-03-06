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
