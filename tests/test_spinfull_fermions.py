import numpy as np
import pytest
import lightcones.linalg as ll
import lightcones.space as sp
from lightcones.models import spinfull_fermions

tol = 1e-10

def test_spinfull_fermions():
    
    # case 1
    
    f = spinfull_fermions(1)
    
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
    
    f = spinfull_fermions(1)
    
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
    