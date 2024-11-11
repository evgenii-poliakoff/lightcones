import os
import sys
import numpy as np
import pathlib
import pytest
from .cases import spin_boson_model_jumps
from .cases import spin_boson_model_ring

@pytest.mark.skip(reason="It takes too much time")
def test_s_z_av():
    _mvf = spin_boson_model_jumps.mvf()
    n_samples = 4
    s_z_av_table_j = _mvf.compute_s_z_av(n_samples, seed = 10)
    s_z_av_table_j[:, 1] = s_z_av_table_j[:, 1] / n_samples
    
    artifact_file = pathlib.Path("./tests/test_artifacts/s_z_av_spin_boson_jumps.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(artifact_file, s_z_av_table_j)
    
    _mvf = spin_boson_model_ring.mvf()
    s_z_av_table_r = _mvf.compute_s_z_av(n_samples, seed = 10)
    s_z_av_table_r[:, 1] = s_z_av_table_r[:, 1] / n_samples
    
    artifact_file = pathlib.Path("./tests/test_artifacts/s_z_av_spin_boson_ring.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(artifact_file, s_z_av_table_r)
    
    n_av_j = s_z_av_table_j
    n_av_j[:, 1] = (n_av_j[:, 1] + 1.0) / 2  
    
    n_av_r = s_z_av_table_r
    n_av_r[:, 1] = (n_av_r[:, 1] + 1.0) / 2  
    
    assert np.allclose(n_av_j, n_av_r, rtol=1e-5, atol=5e-4), \
        f"s_z average for ring does not match the one for jumps"