import os
import sys
import numpy as np
import pathlib

import numpy as np
import lightcones as lc
import lightcones.linalg as la

def test_moving_frame():
    # chain
    n_sites = 100
    # on-site energies
    es = [1]*n_sites
    # hoppings
    hs = [0.05]*(n_sites-1)

    # time grid
    dt = 0.01
    nt = 10000

    # spread
    spread = lc.spread(es, hs, nt, dt)

    # rho_plus
    rho_plus = lc.rho_plus(spread, dt)

    # minimal light cone
    rtol = 10**(-4)
    ti_arrival, spread_min, U_min, rho_plus_min = lc.minimal_forward_frame(spread, rho_plus, dt, rtol)
    
    with pathlib.Path("./tests/cases/ti_arrival.txt").open() as f:
        ti_arrival_expected =  np.loadtxt(f)
    assert np.allclose(ti_arrival, ti_arrival_expected, rtol=1e-5, atol=1e-8), \
        f"ti_arrival does not match the expected"
        
    with pathlib.Path("./tests/cases/spread_min.txt").open() as f:
        spread_min_expected =  np.loadtxt(f)
    assert np.allclose(spread_min, spread_min_expected, rtol=1e-5, atol=1e-8), \
        f"spread_min does not match the expected"
        
    with pathlib.Path("./tests/cases/U_min.txt").open() as f:
        U_min_expected =  np.loadtxt(f)
    assert np.allclose(U_min, U_min_expected, rtol=1e-5, atol=1e-8), \
        f"U_min does not match the expected"
        
    with pathlib.Path("./tests/cases/rho_plus_min.txt").open() as f:
        rho_plus_min_expected =  np.loadtxt(f)
    assert np.allclose(rho_plus_min, rho_plus_min_expected, rtol=1e-5, atol=1e-8), \
        f"rho_plus_min does not match the expected"