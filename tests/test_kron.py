import numpy as np
import lightcones.linalg as la
from lightcones import fock
from lightcones.linalg import kron as k
import lightcones.space as sp

def coo_allclose(a, b, rtol=1e-5, atol=1e-8):
    err = a - b
    if len(err.data) == 0:
        return True
    max_err = err.data.max()
    return max_err <= atol + rtol * max_err.max()

def test_kron_old():
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
                
def test_kron_sl():
    s1 = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f1 = sp.fermions(s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f2 = sp.fermions(s2)
    
    # a
    a_expected = [la.kron(f1.parity, f2.a[0]), la.kron(f1.parity, f2.a[1])]
    a = k(f1.parity, f2.a)
    
    assert len(a) == len(a_expected)
    for i in range(len(a)):
        assert coo_allclose(a[i], a_expected[i], rtol=1e-5, atol=1e-8), \
            f"a not match the expected"
    
    # a_dag
    a_dag_expected = [la.kron(f1.parity, f2.a_dag[0]), la.kron(f1.parity, f2.a_dag[1])]
    a_dag = k(f1.parity, f2.a_dag)
    
    assert len(a_dag) == len(a_dag_expected)
    for i in range(len(a_dag)):
        assert coo_allclose(a_dag[i], a_dag_expected[i], rtol=1e-5, atol=1e-8), \
            f"a_dag not match the expected"
            
def test_kron_ls():
    s1 = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f1 = sp.fermions(s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f2 = sp.fermions(s2)
    
    # a
    a_expected = [la.kron(f1.a[0], f2.parity), la.kron(f1.a[1], f2.parity), la.kron(f1.a[2], f2.parity)]
    a = k(f1.a, f2.parity)
    
    assert len(a) == len(a_expected)
    for i in range(len(a)):
        assert coo_allclose(a[i], a_expected[i], rtol=1e-5, atol=1e-8), \
            f"a not match the expected"
    
    # a_dag
    a_dag_expected = [la.kron(f1.a_dag[0], f2.parity), la.kron(f1.a_dag[1], f2.parity), la.kron(f1.a_dag[2], f2.parity)]
    a_dag = k(f1.a_dag, f2.parity)
    
    assert len(a_dag) == len(a_dag_expected)
    for i in range(len(a_dag)):
        assert coo_allclose(a_dag[i], a_dag_expected[i], rtol=1e-5, atol=1e-8), \
            f"a_dag not match the expected"
            
def test_kron_ll():
    s1 = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f1 = sp.fermions(s1)
    
    s2 = sp.states(2, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    f2 = sp.fermions(s2)
    
    a_expected = [[la.kron(f1.a_dag[0], f2.a[0]), la.kron(f1.a_dag[0], f2.a[1])],
                  [la.kron(f1.a_dag[1], f2.a[0]), la.kron(f1.a_dag[1], f2.a[1])],
                  [la.kron(f1.a_dag[2], f2.a[0]), la.kron(f1.a_dag[2], f2.a[1])]]
    
    a = k(f1.a_dag, f2.a)
    
    assert len(a) == len(a_expected)
    for i in range(len(f1.a_dag)):
        for j in  range(len(f2.a)):
            assert coo_allclose(a[i][j], a_expected[i][j], rtol=1e-5, atol=1e-8), \
                f"a not match the expected"
