import numpy as np
import lightcones.linalg as la
from lightcones import fock
from lightcones.linalg import kron as k

def coo_allclose(a, b, rtol=1e-5, atol=1e-8):
    err = a - b
    if len(err.data) == 0:
        return True
    max_err = err.data.max()
    return max_err <= atol + rtol * max_err.max()

def test_kron():
    max_quanta = 5
    local_bounds = [1, 1, max_quanta, max_quanta]
    space = fock.space(statistics = 'Bose', num_modes = 4, max_local_occupations = local_bounds)
    pr1 = [[space.outer(0, 0, 0), space.outer(0, 1, 0)],
           [space.outer(1, 0, 0), space.outer(1, 1, 0)]]
    pr2 = [[space.outer(0, 0, 1), space.outer(0, 1, 1)],
           [space.outer(1, 0, 1), space.outer(1, 1, 1)]]
    pr = la.kron(pr1, pr2)
    pr_expected = [[k(pr1[0][0], pr2[0][0]), k(pr1[0][0], pr2[0][1]), k(pr1[0][1], pr2[0][0]), k(pr1[0][1], pr2[0][1])],
                   [k(pr1[0][0], pr2[1][0]), k(pr1[0][0], pr2[1][1]), k(pr1[0][1], pr2[1][0]), k(pr1[0][1], pr2[1][1])],
                   [k(pr1[1][0], pr2[0][0]), k(pr1[1][0], pr2[0][1]), k(pr1[1][1], pr2[0][0]), k(pr1[1][1], pr2[0][1])],
                   [k(pr1[1][0], pr2[1][0]), k(pr1[1][0], pr2[1][1]), k(pr1[1][1], pr2[1][0]), k(pr1[1][1], pr2[1][1])]]
    for i in range(4):
        for j in range(4):
            assert coo_allclose(pr[i][j], pr_expected[i][j], rtol=1e-5, atol=1e-8), \
                f"pr not match the expected"

