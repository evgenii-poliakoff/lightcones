import numpy as np
import lightcones.linalg as la

def test_chain2star():
    # from star to chain
    n_sites = 10
    dw = 0.01
    w = np.array([1.0 + i*dw for i in range(n_sites)])
    c = np.array([i*dw for i in range(n_sites)])
    J = c**2
    alpha, beta = la.lancz(w, J)
    
    # back to star form
    e = alpha
    h = np.sqrt(beta)
    coupling = h[0]
    H = la.tridiag(e, h[1:])
    H_dense = H.todense()
    w_, modes_ = la.find_eigs_ascending(H_dense)
    J_ = modes_[0,:]**2 * coupling**2
    
    # check
    assert np.allclose(w, w_, rtol=1e-5, atol=1e-8), \
        f"w not match the ethalon"
    assert np.allclose(J, J_, rtol=1e-5, atol=1e-8), \
        f"J not match the ethalon"