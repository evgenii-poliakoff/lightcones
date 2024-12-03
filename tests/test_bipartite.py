import numpy as np
import pathlib
import lightcones.space as sp

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