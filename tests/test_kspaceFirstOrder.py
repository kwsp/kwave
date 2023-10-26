import tempfile
from pathlib import Path

import h5py
import numpy as np
import kwave.kspaceFirstOrder_runner
from kwave.h5_compare import compare_hdf5_files


def test_kspaceFirstOrder_output():
    infile = "./h5_test_data/example_ivp_binary_sensor_mask_input.h5"
    true_output = "./h5_test_data/example_ivp_binary_sensor_mask_output.h5"

    with tempfile.TemporaryDirectory() as tempdir:
        outfile = Path(tempdir) / "test_out.h5"

        kwave.kspaceFirstOrder_runner._run_binary(
            ["-i", str(infile), "-o", str(outfile)]
        )

        compare_hdf5_files(true_output, outfile)
