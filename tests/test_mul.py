import numpy as np
from lightcones.linalg import mul
from lightcones import fock

def test_mul():
    max_quanta = 5
    local_bounds = [1, 1, max_quanta, max_quanta]
    space = fock.space(statistics = 'Bose', num_modes = 4, max_local_occupations = local_bounds)
    a = space.outer(0, 0, 0)
    b = space.vacuum_state()
    c = mul(a, b)
    assert np.close(c, b, rtol=1e-5, atol=1e-8), \
        f"c not match the ethalon"
    
def test_mul_2():
    max_quanta = 5
    local_bounds = [1, 1, max_quanta, max_quanta]
    space = fock.space(statistics = 'Bose', num_modes = 4, max_local_occupations = local_bounds)
    a = [[space.outer(0, 0, 0), space.outer(0, 1, 0)],
           [space.outer(1, 0, 0), space.outer(1, 1, 0)]]
    b = space.vacuum_state()
    c = mul(a, b)
    c_expected = [[mul(a[0][0], b), mul(a[0][1], b)],
                  [mul(a[1][0], b), mul(a[1][1], b)]]
    for i in range(2):
        for j in range(2):
            np.allclose(c[i][j], c_expected[i][j], rtol=1e-5, atol=1e-8), \
                f"c not match the ethalon"