from __future__ import annotations
from importlib import resources
from pathlib import Path
import tempfile
import signal
import subprocess

import h5py

from kwave.h5input import (
    Grid,
    Medium,
    Sensor,
    Source,
    PML,
    SimulationFlags,
    KSpaceAndShiftVariables,
    H5Input,
)
from kwave.h5output import H5Output
from kwave.h5_dataclass_helper import serialize_to_hdf5, deserialize_from_hdf5


binary_root: Path = resources.files("kwave").parent / "binaries"

cuda_binary = "kspaceFirstOrder-CUDA.exe"


def kspaceFirstOrder(
    grid: Grid,
    medium: Medium,
    sensor: Sensor,
    source: Source,
    simulation_flags: SimulationFlags = None,
    pml: PML = None,
    kspace: KSpaceAndShiftVariables = None,
    data_name: str = "kwave_data",
    data_path: str | Path | None = None,
    **kwargs,
):
    """ """
    ndims = len(grid.shape)
    if pml is None:
        # Auto PML
        # TODO: implement getOptimalPMLSize
        if ndims == 3:
            pml = PML(
                pml_x_size=20,
                pml_x_alpha=2.0,
                pml_y_size=20,
                pml_y_alpha=2.0,
                pml_z_size=20,
                pml_z_alpha=2.0,
            )
        elif ndims == 2:
            pml = PML(pml_x_size=20, pml_x_alpha=2.0, pml_y_size=20, pml_y_alpha=2.0)
        else:
            pml = PML(pml_x_size=20, pml_x_alpha=2.0)

    if simulation_flags is None:
        simulation_flags = SimulationFlags(p0_source_flag=1, absorbing_flag=1)

    inp_args = dict(
        simulation_flags=simulation_flags,
        grid=grid,
        medium=medium,
        sensor=sensor,
        source=source,
        pml=pml,
    )
    if kspace is not None:
        inp_args["kspace"] = kspace
    inp_obj = H5Input(**inp_args)

    # infile = "./h5_test_data/example_ivp_binary_sensor_mask_input.h5"
    # outfile = "test_out.h5"
    # _run_binary(["-i", str(infile), "-o", str(outfile)])

    if data_path is None:
        data_path = Path(tempfile.gettempdir()) / "kwave"
    data_path.mkdir(exist_ok=True, parents=True)

    input_file = data_path / (data_name + "_input.h5")
    output_file = data_path / (data_name + "_output.h5")

    with h5py.File(input_file, "w") as fp:
        serialize_to_hdf5(inp_obj, fp)

    try:
        _run_binary(["-i", str(input_file), "-o", str(output_file)])
    except Exception as e:
        print(f"Run failed. Check the input file {input_file}")
        raise e

    with h5py.File(output_file, "r") as fp:
        output = deserialize_from_hdf5(H5Output, fp)

    return inp_obj, output


def kspaceFirstOrder_version():
    """
    Print the version and build info of the C++ binary.
    """
    binary = binary_root / cuda_binary
    if not binary.exists():
        raise ValueError(f"Binary not found at {binary}")

    cmd = [str(binary), "--version"]
    p = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    _print_stdout_realtime_subp(p)
    p.communicate()


def _run_binary(args: list[str]):
    """
    Call the C++ binary with args.
    Print stdout in real time and check the return code.
    """
    binary = binary_root / cuda_binary
    if not binary.exists():
        raise ValueError(f"Binary not found at {binary}")

    cmd = [str(binary), *args]
    p = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    _print_stdout_realtime_subp(p)

    p.communicate()  # update returncode
    if p.returncode != 0:
        raise ValueError(
            f"Binary {str(binary)} terminated with return code {p.returncode}."
        )


def _print_stdout_realtime_subp(p: subprocess.Popen):
    try:
        while True:
            s = p.stdout.readline()
            if s:
                print(s.decode(), end="")
            else:
                break
    except KeyboardInterrupt as e:
        p.send_signal(signal.SIGINT)
        raise e
