import os
import sys
import numpy as np
import pathlib
from .cases import spin_boson_model_jumps
        
def test_s_z_av():
    _mvf = spin_boson_model_jumps.mvf()
    n_samples = 4
    s_z_av_table = _mvf.compute_s_z_av(n_samples)
    s_z_av_table[:, 1] = s_z_av_table[:, 1] / n_samples
    
    artifact_file = pathlib.Path("./tests/test_artifacts/s_z_av_spin_boson_jumps.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(artifact_file, s_z_av_table)
    
    with pathlib.Path("./tests/cases/s_z_av_spin_boson_cd.txt").open() as f:
        s_z_av_expected = np.loadtxt(f)
    
    n_av = s_z_av_table
    n_av[:, 1] = (n_av[:, 1] + 1.0) / 2  
    
    n_av_expected = s_z_av_expected
    n_av_expected[:, 1] = (n_av_expected[:, 1] + 1.0) / 2  
    
    assert np.allclose(n_av, n_av_expected, rtol=1e-2, atol=1e-2), \
        f"s_z average does not match the expected"