import numpy as np
import pytest
import lightcones.linalg as ll
import lightcones.space as sp
from lightcones.models import fermions_with_spin

tol = 1e-10

def test_fermions_with_spin():
    
    # case 1
    
    f = fermions_with_spin(1)
    
    U = 1
    
    H_S = U * f.n[0][0] @ f.n[1][0]
    
    E, V = ll.find_eigs_ascending(H_S.todense())
    
    E_expected = np.array([0., 0., 0., 1.])
    assert np.allclose(E, E_expected, atol=tol), \
        f"E does not match"
        
    psi_expected = np.array([0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j])
    assert np.allclose(V[:, 3], psi_expected, atol=tol), \
        f"psi does not match"
        
    # case 2
    
    f = fermions_with_spin(1)
    
    U = 1
    mu = U * (1/2.0 + 1/3.0)
    
    H_S = U * f.n[0][0] @ f.n[1][0] - mu * (f.n[0][0] + f.n[1][0])
    
    E, V = ll.find_eigs_ascending(H_S.todense())
    
    E_expected = np.array([-0.83333333333, -0.83333333333, -0.66666666667,  0.           ])
    assert np.allclose(E, E_expected, atol=tol), \
        f"E does not match"
    psi_expected = np.array([1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j])
    assert np.allclose(V[:, 3], psi_expected, atol=tol), \
        f"psi does not match"
    psi_expected = np.array([0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j])
    assert np.allclose(V[:, 2], psi_expected, atol=tol), \
        f"psi does not match"
    
    # case 3
    
    f = fermions_with_spin(2)
    
    t = 0.2
    U = 0.3
    H_hopp = sum([sum([- t * (f.a_dag[s][i] @ f.a[s][i - 1] + f.a_dag[s][i - 1] @ f.a[s][i]) for s in range(2)]) for i in range(2)])
    H_int = sum([U * f.n[0][i] @ f.n[1][i] for i in range(2)])
    H = H_hopp + H_int
    
    E, V = ll.find_eigs_ascending(H.todense())
    E_expected = np.array([-6.63941029805e-01, -4.00000000000e-01, -4.00000000000e-01,
       -1.00000000000e-01, -1.00000000000e-01,  0.00000000000e+00,
        0.00000000000e+00,  0.00000000000e+00,  9.99200722163e-16,
        3.00000000000e-01,  4.00000000000e-01,  4.00000000000e-01,
        6.00000000000e-01,  7.00000000000e-01,  7.00000000000e-01,
        9.63941029805e-01])
    assert np.allclose(E, E_expected, atol=tol), \
        f"E does not match"
        
    def test_fermions_with_spin_vac():
        
        f = fermions_with_spin(2)
        
        vac_actual = f.vac
        
        vac_expected = np.zeros(16, dtype = complex)
        vac_expected[0] = 1.0
        
        assert np.allclose(vac_actual, vac_expected, atol=tol), \
            f"vac does not match"