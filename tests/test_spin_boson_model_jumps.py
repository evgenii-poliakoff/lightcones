import os
import sys
import numpy as np
import pathlib
from .cases import spin_boson_model_jumps

def test_s_z_av():
    tr = spin_boson_model_jumps.trajectory()
    s_z_av_table = tr.compute_s_z_av()
    with pathlib.Path("./tests/cases/s_z_av_spin_boson.txt").open() as f:
        s_z_av_expected =  np.loadtxt(f)
    assert np.allclose(s_z_av_table, s_z_av_expected, rtol=1e-5, atol=5e-4), \
        f"s_z average does not match the expected"