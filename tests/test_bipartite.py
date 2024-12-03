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
    