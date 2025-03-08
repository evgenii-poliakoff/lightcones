import numpy as np
from scipy.stats import unitary_group
import math
import lightcones.jumps as lj
import lightcones.linalg as ll

tol = 1e-10

def test_make_jumps():
    
    # probabilities
    pi = [0.5, 0.3, 0.2]
    
    # random basis
    U = unitary_group.rvs(3)
    
    # density matrix
    rho = U @ np.diag(pi) @ U.T.conj()
    rho = ll.make_hermitean(rho)
    
    # do sampling
    N = 1000
    counts = np.zeros(3)
    for i in range(N):
        ind, psi, pi_ = lj.make_jump_(rho)
        assert np.allclose(pi, pi_, atol=tol), \
            f"pi"
        fidelity = np.abs(psi.T.conj() @ U)
        assert np.allclose(fidelity, np.eye(3), atol=tol), \
            f"U"
        counts[ind] += 1

    counts = counts / N
    assert np.allclose(counts, pi, atol=3/math.sqrt(N)), \
            f"counts"
    