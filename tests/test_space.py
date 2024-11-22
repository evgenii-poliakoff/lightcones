import lightcones.space as sp

def test_space():
    # test bounding conditions
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_in_total(3))
    all_states_expected = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0), (0, 2, 1), (0, 3, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 1, 0), (1, 1, 1), (1, 2, 0), (2, 0, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
    assert s.all_states == all_states_expected
    
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied())
    all_states_expected = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    assert s.all_states == all_states_expected
    
    # test skip condition
    s = sp.states(3, bounding_condition=sp.bounding_condition.more_than_singly_occupied(), skip_condition=sp.skip_condition.odd())
    all_states_expected = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    assert s.all_states == all_states_expected
    
    # 
    assert s.num_modes == 3
    assert s.dimension == 4
    
    # 
    assert s.state_at(1) == (0, 1, 1)
    
    #
    assert s.index_of((1, 0, 1)) == 2
    
    