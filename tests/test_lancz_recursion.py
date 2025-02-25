import numpy as np
import lightcones.linalg as ll

tol = 1e-10

def test_lancz_recursion():
    
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([1, 1, 1, 1])
    H = ll.tridiag(a, b)
    
    psi0 = np.array([1, 0, 0, 0, 0])
    
    H_expected = H.todense()
    H_actual = ll.lancz_recursion(psi0, H, 5).todense()
    
    assert np.allclose(H_expected, H_actual, atol=tol), \
        f"H"