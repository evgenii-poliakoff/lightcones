import os
import sys
import numpy as np
import pathlib

import numpy as np
import lightcones as lc
import lightcones.linalg as la

def complex_converter(x):
    x = x.decode('utf-8')
    return complex(x.strip('()'))

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
        spread_min_expected = np.loadtxt(f, dtype=complex, converters=complex_converter)
    assert np.allclose(spread_min, spread_min_expected, rtol=1e-5, atol=2e-8), \
        f"spread_min does not match the expected"
        
    with pathlib.Path("./tests/cases/U_min.txt").open() as f:
        U_min_expected =  np.loadtxt(f, dtype=complex, converters=complex_converter)
    assert np.allclose(U_min, U_min_expected, rtol=1e-5, atol=1e-8), \
        f"U_min does not match the expected"
        
    with pathlib.Path("./tests/cases/rho_plus_min.txt").open() as f:
        rho_plus_min_expected =  np.loadtxt(f, dtype=complex, converters=complex_converter)
    assert np.allclose(rho_plus_min, rho_plus_min_expected, rtol=1e-5, atol=1e-8), \
        f"rho_plus_min does not match the expected"
        
    # causal diamond frame
    cd_dim = 4
    spread_cd, U_cd = lc.causal_diamond_frame(spread_min, ti_arrival, U_min, rho_plus_min, dt, rtol, cd_dim)
    
    with pathlib.Path("./tests/cases/spread_cd.txt").open() as f:
        spread_cd_expected =  np.loadtxt(f, dtype=complex, converters=complex_converter)
    assert np.allclose(spread_cd, spread_cd_expected, rtol=1e-5, atol=1e-8), \
        f"spread_min does not match the expected"
        
    marker = np.empty((0, 0))
    U_cd_computed = [m if m is not None else marker for m in U_cd]
    U_cd_expected = np.load('./tests/cases/U_cd.npz')
    ind = 0
    for key in U_cd_expected.files:
        assert np.allclose(U_cd_computed[ind], U_cd_expected[key], rtol=1e-5, atol=1e-8), \
        f"U_cd does not match the expected for ind " + str(ind)
        ind = ind + 1
        
    # moving frame
    spread_mv, H_mv = lc.moving_frame(spread_cd, ti_arrival, U_cd, dt, cd_dim)
    
    with pathlib.Path("./tests/cases/spread_mv.txt").open() as f:
        spread_mv_expected =  np.loadtxt(f, dtype=complex, converters=complex_converter)
    assert np.allclose(spread_mv, spread_mv_expected, rtol=1e-5, atol=1e-8), \
        f"spread_min does not match the expected"
        
    H_mv_computed = [m if m is not None else marker for m in H_mv]
    H_mv_expected = np.load('./tests/cases/H_mv.npz')
    ind = 0
    for key in H_mv_expected.files:
        assert np.allclose(H_mv_computed[ind], H_mv_expected[key], rtol=1e-5, atol=1e-8), \
        f"H_mv does not match the expected for ind " + str(ind)
        ind = ind + 1
    