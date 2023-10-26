import tempfile
from pathlib import Path

import h5py
from kwave import H5Input
from kwave.h5_dataclass_helper import serialize_to_hdf5, deserialize_from_hdf5
from kwave.h5_compare import compare_hdf5_files


def test_serialization_deserialization_input():
    true_input_path = "h5_test_data/example_ivp_binary_sensor_mask_input.h5"
    with h5py.File(true_input_path, "r") as example_input:
        inp = deserialize_from_hdf5(H5Input, example_input)

    with tempfile.TemporaryDirectory() as tempdir:
        new_path = Path(tempdir) / "test_out.h5"
        with h5py.File(new_path, "w") as new_h5:
            serialize_to_hdf5(inp, new_h5)

        compare_hdf5_files(new_path, true_input_path)
