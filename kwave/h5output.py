from __future__ import annotations
from typing import Annotated
import numpy as np
from dataclasses import dataclass

from kwave.h5_dataclass_helper import (
    LongReal,
    LongRealOptional,
    FloatRealOptional,
)

from kwave.h5input import (
    SimulationFlags,
    Grid,
    Sensor,
    PML,
)


__all__ = (
    "SimulationFlags",
    "SimulationFlagsOutput",
    "Grid",
    "Sensor",
    "PML",
    "SimulationResults",
    "H5Output",
)


@dataclass
class SimulationFlagsOutput(SimulationFlags):
    """
    1. Simulation Flags
    """

    u_source_mode: LongRealOptional = LongReal(0)
    u_source_many: LongRealOptional = LongReal(0)
    p_source_mode: LongRealOptional = LongReal(0)
    p_source_many: LongRealOptional = LongReal(0)


@dataclass
class SimulationResults:
    """
    5. Simulation Results
    """

    # 5.1 Binary Sensor Mask (defined if sensor_mask_type = 0)

    p: Annotated[FloatRealOptional, (1, "Nt-s+1", "Nsens")]  # -p or --p_raw
    p_rms: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --p_rms
    p_max: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --p_max
    p_min: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --p_min
    p_max_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --p_max_all
    p_min_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --p_min_all
    p_final: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --p_final
    ux: Annotated[FloatRealOptional, (1, "Nt-s+1", "Nsens")]  # -u or --u_raw
    uy: Annotated[FloatRealOptional, (1, "Nt-s+1", "Nsens")]  # -u or --u_raw
    uz: Annotated[FloatRealOptional, (1, "Nt-s+1", "Nsens")]  # -u or --u_raw
    ux_non_staggered: Annotated[
        FloatRealOptional, (1, "Nt-s+1", "Nsens")
    ]  # --u_non_staggered
    uy_non_staggered: Annotated[
        FloatRealOptional, (1, "Nt-s+1", "Nsens")
    ]  # --u_non_staggered
    uz_non_staggered: Annotated[
        FloatRealOptional, (1, "Nt-s+1", "Nsens")
    ]  # --u_non_staggered
    ux_rms: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_rms
    uy_rms: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_rms
    uz_rms: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_rms
    ux_max: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_max
    uy_max: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_max
    uz_max: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_max
    ux_min: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_min
    uy_min: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_min
    uz_min: Annotated[FloatRealOptional, (1, 1, "Nsens")]  # --u_min
    ux_max_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_max_all
    uy_max_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_max_all
    uz_max_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_max_all
    ux_min_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_min_all
    uy_min_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_min_all
    uz_min_all: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_min_all
    ux_final: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_final
    uy_final: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_final
    uz_final: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx")]  # --u_final

    # 5.2 Opposing Cuboid Corners Sensor Mask (defined if sensor_mask_type = 1) (implemented = False)
    #
    # Note, each output group (e.g., /p) contains a dataset for each cuboid defined in
    # sensor_mask_corners, where /1 indicates the first dataset, /2 indicates the second
    # dataset, and so on up to Ncubes.

    # | Name               | Size (Nx, Ny, Nz)    | Data Type | Domain Type | Conditions            |
    # | ------------------ | -------------------- | --------- | ----------- | --------------------- |
    # | p/1                | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -p or --p_raw         |
    # | p_rms/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_rms               |
    # | p_max/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_max               |
    # | p_min/1            | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --p_min               |
    # | p_max_all          | (Nx, Ny, Nz)         | float     | real        | --p_max_all           |
    # | p_min_all          | (Nx, Ny, Nz)         | float     | real        | --p_min_all           |
    # | p_final            | (Nx, Ny, Nz)         | float     | real        | --p_final             |
    # | ux/1               | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -u or--u_raw          |
    # | uy/1               | (Cx, Cy, Cz, Nt-s+1) | float     | real        | -u or--u_raw          |
    # | uz/1               | (Cx, Cy, Cz, Nt-s+1) | float     | rea         | -u or--u_raw          |
    # | ux_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
    # | uy_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
    # | uz_non_staggered/1 | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_non_staggered_raw |
    # | ux_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
    # | uy_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
    # | uz_rms/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_rms               |
    # | ux_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
    # | uy_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
    # | uz_max/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_max               |
    # | ux_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
    # | uy_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
    # | uz_min/1           | (Cx, Cy, Cz, Nt-s+1) | float     | real        | --u_min               |
    # | ux_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
    # | uy_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
    # | uz_max_all         | (Nx, Ny, Nz)         | float     | real        | --u_max_all           |
    # | ux_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
    # | uy_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
    # | uz_min_all         | (Nx, Ny, Nz)         | float     | real        | --u_min_all           |
    # | ux_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
    # | uy_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
    # | uz_final           | (Nx, Ny, Nz)         | float     | real        | --u_final             |
    ...


@dataclass
class H5Output:
    # 1. Simulation Flags
    simulation_flags: SimulationFlagsOutput
    # 2. Grid Properties
    grid: Grid
    # 3. PML Variables
    pml: PML
    # 4. Sensor Variables (defined if --copy_sensor_mask)
    sensor: Sensor
    # 5. Simulation Results
    results: SimulationResults
