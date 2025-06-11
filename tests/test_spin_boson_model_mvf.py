import os
import sys
import numpy as np
import pytest
import pathlib
from .cases import spin_boson_model_mvf

@pytest.mark.skip(reason="This test fails on ar")
def test_s_z_av():
    s_z_av_table = spin_boson_model_mvf.compute_s_z_av()

    artifact_file = pathlib.Path("./tests/test_artifacts/s_z_av_spin_boson_model_mvf.txt")
    artifact_file.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(artifact_file, s_z_av_table)

    with pathlib.Path("./tests/cases/s_z_av_spin_boson_cd.txt").open() as f:
        s_z_av_expected =  np.loadtxt(f)
    assert np.allclose(s_z_av_table, s_z_av_expected, rtol=1e-4, atol=1e-4), \
        f"s_z average does not match the expected"