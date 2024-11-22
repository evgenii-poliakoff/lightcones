import numpy as np
import pytest
import lightcones.space as sp

tol = 1e-10

def test_fermions():
    
    # exception throwing
    
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_in_total(2))
    with pytest.raises(ValueError) as exc_info:
        f = sp.fermions(s)
    assert str(exc_info.value) == "Using more than singly occupied states to construct fermionic operators"
    
    #
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f = sp.fermions(s)
    
    # vac
    vac = f.vac()
    expected = [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]
    assert np.allclose(vac, expected, atol=tol), \
        f"vac"
    
    # eye
    
    m = f.eye
    data = [1., 1., 1., 1., 1., 1., 1., 1.]
    indices = [0, 1, 2, 3, 4, 5, 6, 7]
    indptr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    assert np.allclose(m.data, data, atol=tol), \
        f"data for eye"
    assert np.array_equal(m.indices, indices), \
        f"indices for eye"
    assert np.array_equal(m.indptr, indptr), \
        f"indptr for eye"
        
    # zero
    
    m = f.zero
    data = []
    indices = []
    indptr = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    assert np.allclose(m.data, data, atol=tol), \
        f"data for zero"
    assert np.array_equal(m.indices, indices), \
        f"indices for zero"
    assert np.array_equal(m.indptr, indptr), \
        f"indptr for zero"
    
    # a[0]
    m1 = f.a[0]
    
    data = [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j]
    indices = [0, 1, 2, 3]
    indptr = [0, 0, 0, 0, 0, 1, 2, 3, 4]
    
    assert np.allclose(m1.data, data, atol=tol), \
        f"data for a[0]"
    assert np.array_equal(m1.indices, indices), \
        f"indices for a[0]"
    assert np.array_equal(m1.indptr, indptr), \
        f"indptr for a[0]"
        
    # a[1]
    
    m2 = f.a[1]
    
    data = [1.+0.j,  1.+0.j, -1.+0.j, -1.+0.j]
    indices = [0, 1, 4, 5]
    indptr = [0, 0, 0, 1, 2, 2, 2, 3, 4]
    
    assert np.allclose(m2.data, data, atol=tol), \
        f"data for a[1]"
    assert np.array_equal(m2.indices, indices), \
        f"indices for a[1]"
    assert np.array_equal(m2.indptr, indptr), \
        f"indptr for a[1]"
    
    # a[2]
    
    m3 = f.a[2]
    
    data = [1.+0.j, -1.+0.j, -1.+0.j,  1.+0.j]
    indices = [0, 2, 4, 6]
    indptr = [0, 0, 1, 1, 2, 2, 3, 3, 4]
    
    assert np.allclose(m3.data, data, atol=tol), \
        f"data for a[1]"
    assert np.array_equal(m3.indices, indices), \
        f"indices for a[1]"
    assert np.array_equal(m3.indptr, indptr), \
        f"indptr for a[1]"
    
    # a_dag[0]
    
    m1 = f.a_dag[0]
    
    data = [1.+0.j, 1.+0.j, 1.+0.j, 1.+0.j]
    indices = [4, 5, 6, 7]
    indptr = [0, 1, 2, 3, 4, 4, 4, 4, 4]
    
    assert np.allclose(m1.data, data, atol=tol), \
        f"data for a_dag[0]"
    assert np.array_equal(m1.indices, indices), \
        f"indices for a_dag[0]"
    assert np.array_equal(m1.indptr, indptr), \
        f"indptr for a_dag[0]"
    
    # a_dag[1]
    
    m2 = f.a_dag[1]
    
    data = [1.+0.j,  1.+0.j, -1.+0.j, -1.+0.j]
    indices = [2, 3, 6, 7]
    indptr = [0, 1, 2, 2, 2, 3, 4, 4, 4]
    
    assert np.allclose(m2.data, data, atol=tol), \
        f"data for a_dag[1]"
    assert np.array_equal(m2.indices, indices), \
        f"indices for a_dag[1]"
    assert np.array_equal(m2.indptr, indptr), \
        f"indptr for a_dag[1]"
    
    # a_dag[2]
    
    m3 = f.a_dag[2]
    
    data = [1.+0.j, -1.+0.j, -1.+0.j,  1.+0.j]
    indices = [1, 3, 5, 7]
    indptr = [0, 1, 1, 2, 2, 3, 3, 4, 4]
    
    assert np.allclose(m3.data, data, atol=tol), \
        f"data for a_dag[2]"
    assert np.array_equal(m3.indices, indices), \
        f"indices for a_dag[2]"
    assert np.array_equal(m3.indptr, indptr), \
        f"indptr for a_dag[2]"
    
    
    