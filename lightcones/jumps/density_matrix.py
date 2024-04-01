import numpy as np
from lightcones import fock

def density_matrix(psi, space, mode_index):
    local_dim = space.max_total_occupation
    if not space.max_local_occupation is None:
        local_dim = min(local_dim, space.max_local_occupation[mode_index])
    rho = np.zeros((local_dim, local_dim), dtype = complex)
    for i in range(local_dim):
        for j in range(local_dim):
            rho[i, j] = np.vdot(psi, space.outer(j, i, mode_index) @ psi)
    return rho