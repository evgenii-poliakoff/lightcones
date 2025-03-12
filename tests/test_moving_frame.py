import os
import sys
import numpy as np
import pathlib
import pytest

import math
import lightcones as lc
import lightcones.linalg as ll

def complex_converter(x):
    return complex(x.strip('()'))

#@pytest.mark.skip(reason="This test fails on ar")
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
    
    # only check first n_rel coefficients in spread
    # because the modes which are irrelevant for the
    # considered time interval
    # are ill-conditioned
    # (are nearly-degenerate wrt rho_plus hence
    # defined up to spurious unitary transform)
    n_rel = len(ti_arrival)
    
    with pathlib.Path("./tests/cases/ti_arrival.txt").open() as f:
        ti_arrival_expected =  np.loadtxt(f)
    assert np.allclose(ti_arrival, ti_arrival_expected, rtol=1e-5, atol=1e-8), \
        f"ti_arrival does not match the expected"
        
    with pathlib.Path("./tests/cases/spread_min.txt").open() as f:
        spread_min_expected = np.loadtxt(f, dtype=complex, converters=complex_converter)
        
    # compare the commutators based on spread
        
    comm_expected = []
    comm_actual = []
        
    for ti in range(0, nt, 10):
        m_in = lc.m_in(ti_arrival, ti)
        for tj in range(ti, nt, 10):
            comm_expected.append(np.vdot( spread_min_expected[: m_in, ti],  spread_min_expected[: m_in, tj]))
            comm_actual.append(np.vdot( spread_min[: m_in, ti],  spread_min[: m_in, tj]))
        
    assert np.allclose(np.array(comm_expected), np.array(comm_actual), rtol=1e-5, atol=2e-8), \
        f"comm"
        
    # test U_min
    
    spread_actual = U_min.T.conj() @ spread_min
    assert np.allclose(spread_actual, spread, rtol=1e-5, atol=1e-8), \
        f"U_min"
    
    # test rho_plus_min
    
    rho_plus_actual = U_min.T.conj() @ rho_plus_min @ U_min
    assert np.allclose(rho_plus_actual, rho_plus, rtol=1e-5, atol=1e-8), \
        f"rho_plus_min"
        
    # test eigenvalues of rho_plus_min
    
    with pathlib.Path("./tests/cases/rho_plus_min.txt").open() as f:
        rho_plus_min_expected =  np.loadtxt(f, dtype=complex, converters=complex_converter)
    
    e, _ =  ll.find_largest_eigs(rho_plus_min, k = n_rel)
    e_expected, _ =  ll.find_largest_eigs(rho_plus_min_expected, k = n_rel)
    
    assert np.allclose(e, e_expected, rtol=1e-5, atol=1e-8), \
        f"e"
        
    # causal diamond frame
    
    cd_dim = 4
    spread_cd, U_cd = lc.causal_diamond_frame(spread_min, ti_arrival, U_min, rho_plus_min, dt, rtol, cd_dim)
    
    # test commutator
    
    comm_cd_actual = []
    for ti in range(0, nt, 10):
        m_out, m_in = lc.get_inout_range(ti_arrival, ti, cd_dim)
        for tj in range(ti, nt, 10):
            m_out_, m_in_ = lc.get_inout_range(ti_arrival, tj, cd_dim)
            vec_1 = spread_cd[: m_in, ti]
            vec_2 = spread_cd[: m_in_, tj]
            if (m_in_ > m_in):
                vec_1 = np.concatenate((vec_1, np.zeros(m_in_ - m_in)))
            for i in range(m_in, m_in_):
                if not U_cd[i] is None:
                    vec_1[i - cd_dim : i] = U_cd[i] @ vec_1[i - cd_dim : i]            
            comm_cd_actual.append(np.vdot(vec_1, vec_2))

    assert np.allclose(np.array(comm_expected), np.array(comm_cd_actual), rtol=1e-5, atol=2e-8), \
        f"comm_cd"
        
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
    