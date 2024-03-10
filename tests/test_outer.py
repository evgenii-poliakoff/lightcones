import numpy as np
from lightcones import fock

def test_outer_boson():
    max_quanta = 5
    local_bounds = [1, 1, max_quanta, max_quanta]
    space = fock.space(statistics = 'Bose', num_modes = 4, max_local_occupations = local_bounds)
    psi = np.zeros(space.dimension, dtype = complex)
    occupations = [0, 1, 5, 5]
    psi[space.index(occupations)] = np.sqrt(0.5)
    occupations = [1, 1, 4, 5]
    psi[space.index(occupations)] = np.sqrt(0.5)
    pr = [[space.outer(0, 0, 0), space.outer(0, 1, 0)],
          [space.outer(1, 0, 0), space.outer(1, 1, 0)]]
    rho = np.zeros((2, 2), dtype = complex)
    for p in range(2):
        for q in range(2):
            rho[p, q] = np.vdot(psi, pr[p][q] @ psi)
    rho_expected = np.zeros((2, 2), dtype = complex)
    rho_expected[0, 0] = 0.5
    rho_expected[1, 1] = 0.5
    assert np.allclose(rho, rho_expected, rtol=1e-5, atol=1e-8), \
        f"rho not match the ethalon"
    