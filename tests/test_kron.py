import numpy as np
import lightcones.linalg as la
from lightcones import fock
from lightcones.linalg import kron as k

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
            assert np.allclose(pr[i][j].toarray(), pr_expected[i][j].toarray(), rtol=1e-5, atol=1e-8), \
                f"pr not match the ethalon"

