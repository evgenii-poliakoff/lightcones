import numpy as np
import pathlib
import math
import lightcones.space as sp
import lightcones.linalg as ll
import lightcones.models as lm

tol = 1e-10

def test_bipartite_all_states():
    
    j = 3
    s1 = sp.states(1, bounding_condition=sp.bounding_condition.more_than_n_occupied(2 * j))
    q = sp.spins(j, s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    b = sp.bosons(s2)
    
    bp = sp.bipartite(q.states.dimension, b.states.dimension)
    
    all = np.array(bp.all_states)
    
    with pathlib.Path("./tests/cases/bipartite_all_states.txt").open() as f:
        all_expected =  np.loadtxt(f)
             
    assert np.allclose(all, all_expected, rtol=0, atol=0), \
        f"all does not match"
    
def test_bipartite_occupations():
    
    j = 3
    s1 = sp.states(1, bounding_condition=sp.bounding_condition.more_than_n_occupied(2 * j))
    q = sp.spins(j, s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    b = sp.bosons(s2)
    
    bp = sp.bipartite(q.states.dimension, b.states.dimension)
    
    occ = []
    
    for i in range(bp.dimension):
        s = bp.all_states[i]
        occ.append([*q.states.state_at(s[0]), *b.states.state_at(s[1])])
             
    occ = np.array(occ)
    
    with pathlib.Path("./tests/cases/bipartite_occupations.txt").open() as f:
        occ_expected = np.loadtxt(f)
             
    assert np.allclose(occ, occ_expected, rtol=0, atol=0), \
        f"occ does not match"
        
def test_bipartite_index_of():
        
    j = 3
    s1 = sp.states(1, bounding_condition=sp.bounding_condition.more_than_n_occupied(2 * j))
    q = sp.spins(j, s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    b = sp.bosons(s2)
    
    bp = sp.bipartite(q.states.dimension, b.states.dimension)
        
    occ = (4, 2, 0)
    ind = bp.index_of((occ[0], b.states.index_of(occ[1:])))
    assert ind == 47, "ind does not match"
    
def test_bipartite_trace_out_L():
    
    # case 1
    
    j = 3
    s1 = sp.states(1, bounding_condition=sp.bounding_condition.more_than_n_occupied(2 * j))
    q = sp.spins(j, s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    b = sp.bosons(s2)
    
    bp = sp.bipartite(q.states.dimension, b.states.dimension)
    
    psi = bp.vector_with((0, b.states.index_of((0, 0)))) / math.sqrt(3.0) \
        + bp.vector_with((1, b.states.index_of((1, 0)))) / math.sqrt(3.0) \
        + bp.vector_with((2, b.states.index_of((1, 1)))) / math.sqrt(3.0)
        
    rho_actual = bp.trace_out_L(psi)
    
    rho_expected = \
        ll.projection_to(b.states.vector_with((0, 0))) / 3.0 + \
        ll.projection_to(b.states.vector_with((1, 0))) / 3.0 + \
        ll.projection_to(b.states.vector_with((1, 1))) / 3.0
    
    assert np.allclose(rho_actual, rho_expected, atol=tol), \
        f"rho does not match"
        
    # case 2
    
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f = sp.fermions(s)
    
    bp = sp.bipartite(f.states.dimension, f.states.dimension)
    
    psi = bp.vector_with((f.states.index_of((0, 0, 0)), f.states.index_of((1, 1, 1)))) / math.sqrt(2.0) \
        + bp.vector_with((f.states.index_of((1, 1, 1)), f.states.index_of((0, 0, 0)))) / math.sqrt(2.0)
        
    rho_actual = bp.trace_out_L(psi)
    
    rho_expected = \
        ll.projection_to(f.states.vector_with((0, 0, 0))) / 2.0 + \
        ll.projection_to(f.states.vector_with((1, 1, 1))) / 2.0
        
    assert np.allclose(rho_actual, rho_expected, atol=tol), \
        f"rho does not match"
        
def test_bipartite_trace_out_R():
    
    # case 1
    
    j = 3
    s1 = sp.states(1, bounding_condition=sp.bounding_condition.more_than_n_occupied(2 * j))
    q = sp.spins(j, s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    b = sp.bosons(s2)
    
    bp = sp.bipartite(q.states.dimension, b.states.dimension)
    
    psi = bp.vector_with((0, b.states.index_of((0, 0)))) / math.sqrt(3.0) \
        + bp.vector_with((1, b.states.index_of((1, 0)))) / math.sqrt(3.0) \
        + bp.vector_with((2, b.states.index_of((1, 1)))) / math.sqrt(3.0)
        
    rho_actual = bp.trace_out_R(psi)
    
    rho_expected = \
        ll.projection_to(q.states.vector_with((0,))) / 3.0 + \
        ll.projection_to(q.states.vector_with((1,))) / 3.0 + \
        ll.projection_to(q.states.vector_with((2,))) / 3.0
    
    assert np.allclose(rho_actual, rho_expected, atol=tol), \
        f"rho does not match"
        
    # case 2
    
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f = sp.fermions(s)
    
    bp = sp.bipartite(f.states.dimension, f.states.dimension)
    
    psi = bp.vector_with((f.states.index_of((0, 0, 0)), f.states.index_of((1, 1, 1)))) / math.sqrt(2.0) \
        + bp.vector_with((f.states.index_of((1, 0, 1)), f.states.index_of((0, 0, 0)))) / math.sqrt(2.0)
        
    rho_actual = bp.trace_out_R(psi)
    
    rho_expected = \
        ll.projection_to(f.states.vector_with((0, 0, 0))) / 2.0 + \
        ll.projection_to(f.states.vector_with((1, 0, 1))) / 2.0
        
    assert np.allclose(rho_actual, rho_expected, atol=tol), \
        f"rho does not match"

def test_bipartite_vac():
    
    l = lm.spinfull_fermions(2)
    r = lm.spinfull_fermions(3)
    bp = sp.bipartite(l.dimension, r.dimension)
    
    vac_actual = bp.vac()
    
    vac_expected = np.zeros(1024, dtype = complex)
    vac_expected[0] = 1.0
    
    assert np.allclose(vac_actual, vac_expected, atol=tol), \
        f"vac does not match"

def test_bipartite_kron():
    
    l = lm.spinfull_fermions(2)
    r = lm.spinfull_fermions(3)

    bp = sp.bipartite(l.dimension, r.dimension)

    A = 1 / math.sqrt(2) + 0.1
    B = math.sqrt(1 - A**2)

    psi = A * bp.kron(l.a_dag[0][0] @ l.vac(), r.a_dag[0][0] @ r.vac()) + \
        B * bp.kron(l.a_dag[1][0] @ l.vac(), r.a_dag[1][0] @ r.vac())
    
    rho = bp.trace_out_R(psi)
    pi, phi = ll.find_eigs_descending(rho)
    
    assert len(pi) == 16, \
        f"len(pi) does not match"
    
    pi_expected = np.zeros(16)
    pi_expected[0] = A**2
    pi_expected[1] = B**2
    
    assert np.allclose(pi, pi_expected, atol=tol), \
        f"pi does not match"
        
    assert np.allclose(l.a[0][0] @ phi[:, 0], l.vac()), \
        f"phi[:, 0] does not match"
        
    assert np.allclose(l.a[1][0] @ phi[:, 1], l.vac()), \
        f"phi[:, 1] does not match"
    