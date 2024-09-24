import os
import sys
import numpy as np
import pathlib
from .cases import spin_boson_model_montecarlo

def test_s_z_av():
    s_z_av_table = spin_boson_model_montecarlo.compute_s_z_av(n_samples = 50, n_cpu = 20, seed = 0)
    
    artifact_file = pathlib.Path("./tests/test_artifacts/s_z_av_spin_boson_montecarlo.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(artifact_file, s_z_av_table)
    
    with pathlib.Path("./tests/cases/s_z_av_spin_boson_cd.txt").open() as f:
        s_z_av_expected =  np.loadtxt(f)
        
    n_av_mc = s_z_av_table
    n_av_mc[:, 1] = (n_av_mc[:, 1] + 1.0) / 2  
    
    n_av_exp = s_z_av_expected
    n_av_exp[:, 1] = (n_av_exp[:, 1] + 1.0) / 2  
        
    assert np.allclose(n_z_av_mc, n_z_av_exp, rtol=1e-2, atol=1e-2), \
        f"s_z average does not match the expected"