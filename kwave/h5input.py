"""
This module defines the input HDF5 parameters as listed in Table B.1 from the k-wave user manual.
Table B.1: List of datasets that may be present in the input HDF5 file.

Serialization

Deserialization

"""
from __future__ import annotations
from typing import Annotated
import numpy as np
from dataclasses import dataclass, field

from kwave.h5_dataclass_helper import (
    LongReal,
    LongRealOptional,
    FloatReal,
    FloatRealOptional,
)

__all__ = (
    "SimulationFlags",
    "Grid",
    "Medium",
    "Sensor",
    "Source",
    "PML",
    "KSpaceAndShiftVariables",
    "H5Input",
)


@dataclass
class SimulationFlags:
    """
    1. Simulation Flags (Output)
    """

    p0_source_flag: LongReal = 1
    absorbing_flag: LongReal = 1
    transducer_source_flag: LongReal = 0
    nonlinear_flag: LongReal = 0
    ux_source_flag: LongReal = 0
    uy_source_flag: LongReal = 0
    uz_source_flag: LongReal = 0
    p_source_flag: LongReal = 0
    nonuniform_grid_flag: LongReal = 0  # must be set to 0
    # The following are not documented in the v1.1 user manual
    elastic_flag: LongReal = 0
    sxx_source_flag: LongReal = 0
    sxy_source_flag: LongReal = 0
    sxz_source_flag: LongReal = 0
    syy_source_flag: LongReal = 0
    syz_source_flag: LongReal = 0
    szz_source_flag: LongReal = 0
    axisymmetric_flag: LongReal = 0


@dataclass
class Grid:
    """
    2. Grid Properties (Same for input and output)
    """

    Nx: LongReal
    dx: FloatReal

    Ny: LongReal = LongReal(1)
    dy: FloatRealOptional = None

    Nz: LongReal = LongReal(1)
    dz: FloatRealOptional = None

    Nt: LongReal = None
    dt: FloatReal = None

    def is_2D(self):
        return self.Nz == 1

    @property
    def shape(self) -> tuple[int, ...]:
        if self.Ny == 1 and self.Nz == 1:
            return (self.Nx,)
        if self.Nz == 1:
            return self.Ny, self.Nx
        return self.Nz, self.Ny, self.Nx

    @property
    def x_size(self):
        return self.Nx * self.dx

    @property
    def y_size(self):
        return self.Ny * self.dy

    @property
    def z_size(self):
        return self.Nz * self.dz

    @property
    def t_array(self):
        return np.arange(self.Nt) * self.dt

    def make_time(self, c: float, cfl=0.3, t_end=None):
        c_max = np.max(c)
        c_min = np.min(c)

        if t_end is None:
            shape = self.shape
            match len(shape):
                case 3:
                    t_end = (
                        np.linalg.norm((self.x_size, self.y_size, self.z_size)) / c_min
                    )
                case 2:
                    t_end = np.linalg.norm((self.x_size, self.y_size)) / c_min
                case _:
                    t_end = self.x_size / c_min

        min_grid_dim = 0.0
        match len(shape):
            case 3:
                min_grid_dim = min(self.dx, self.dy, self.dz)
            case 2:
                min_grid_dim = min(self.dx, self.dy)
            case _:
                min_grid_dim = self.dx

        self.dt = cfl * min_grid_dim / c_max

        self.Nt = np.ceil(t_end / self.dt)

        if (np.floor(t_end / self.dt) != np.ceil(t_end / self.dt)) and np.remainder(
            t_end, self.dt
        ) == 0:
            self.Nt += 1


@dataclass
class Medium:
    """
    3. Medium Properties

    When homogeneous, parameters are single values
    When heterogenous, parameters have shape ("Nz", "Ny", "Nx")
    """

    # 3.1 Regular Medium Properties
    rho0: Annotated[FloatReal, ("Nz", "Ny", "Nx"), (1, 1, 1)] = 1.0
    rho0_sgx: Annotated[FloatReal, ("Nz", "Ny", "Nx"), (1, 1, 1)] = 1.0
    rho0_sgy: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx"), (1, 1, 1)] = 1.0
    rho0_sgz: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx"), (1, 1, 1)] = 1.0
    c0: Annotated[FloatReal, ("Nz", "Ny", "Nx"), (1, 1, 1)] = 1500.0
    c_ref: FloatReal = FloatReal(1500.0)

    # 3.2 Nonlinear Medium Properties (defined if `nonlinear_flag = 1`)
    BonA: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx"), (1, 1, 1)] = None

    ## 3.3 Absorbing Medium Properties (defined if `absorbing_flag = 1`)
    alpha_coeff: Annotated[FloatRealOptional, ("Nz", "Ny", "Nx"), (1, 1, 1)] = None
    alpha_power: FloatRealOptional = None


@dataclass
class Sensor:
    """
    4. Sensor Properties
    """

    sensor_mask_type: LongReal = 0
    sensor_mask_index: Annotated[
        LongRealOptional, (1, 1, "Nsens")
    ] = None  # sensor_mask_type == 0
    sensor_mask_corners: Annotated[
        LongRealOptional, (1, 6, "Ncubes")
    ] = None  # sensor_mask_type == 1

    @classmethod
    def make_binary_sensor(cls, sensor_mask: np.ndarray) -> Sensor:
        sensor_mask_index = np.ravel_multi_index(
            np.nonzero(sensor_mask), sensor_mask.shape
        )
        sensor_mask_index = sensor_mask_index[np.newaxis, np.newaxis, :]
        return cls(sensor_mask_type=0, sensor_mask_index=sensor_mask_index)

    # helper functions for sensor_mask_type == 0
    def get_binary_mask(self, shape: tuple[int]):
        if self.sensor_mask_type == 0:
            indices = self.get_xy_sensor_mask_index(shape)
            mask = np.zeros(shape, dtype=np.uint8)
            mask[indices] = 1
            return mask
        else:
            raise NotImplementedError()

    def get_xy_sensor_mask_index(self, shape: tuple[int]):
        assert self.sensor_mask_type == 0
        assert len(shape) == 2
        return np.unravel_index(self.sensor_mask_index[0, 0], shape)


@dataclass
class Source:
    """
    5. Source Properties

    """

    # 5.1 Velocity Source Terms (defined if `ux_source_flag = 1` or `uy_source_flag = 1` or `uz_source_flag = 1`)
    u_source_mode: LongRealOptional = None
    u_source_many: LongRealOptional = None
    u_source_index: Annotated[LongRealOptional, (1, 1, "Nsrc")] = None
    ux_source_input: Annotated[
        LongRealOptional,
        [
            (lambda self: self.sensor_mask_type == 0, (1, "Nt_src", 1)),
            (lambda self: self.sensor_mask_type == 1, (1, "Nt_src", "Nsrc")),
        ],
    ] = None
    uy_source_input: Annotated[
        LongRealOptional,
        [
            (lambda self: self.sensor_mask_type == 0, (1, "Nt_src", 1)),
            (lambda self: self.sensor_mask_type == 1, (1, "Nt_src", "Nsrc")),
        ],
    ] = None
    uz_source_input: Annotated[
        LongRealOptional,
        [
            (lambda self: self.sensor_mask_type == 0, (1, "Nt_src", 1)),
            (lambda self: self.sensor_mask_type == 1, ("Nsrc", "Nt_src", 1)),
        ],
    ] = None

    # 5.2 Pressure Source Terms (defined if `p_source_flag` = 1)
    p_source_mode: LongRealOptional = None
    p_source_many: LongRealOptional = None
    p_source_index: Annotated[FloatRealOptional, (1, 1, "Nsrc")] = None
    p_source_input: Annotated[
        FloatRealOptional,
        [
            (lambda self: self.p_source_many == 0, (1, "Nt_src", 1)),
            (lambda self: self.p_source_many == 1, (1, "Nt_src", "Nsrc")),
        ],
    ] = None

    # 5.3 Transducer Source Terms (defined if `transducer_source_flag = 1`)
    u_source_index: Annotated[LongRealOptional, (1, 1, "Nsrc")] = None
    transducer_source_input: Annotated[FloatRealOptional, (1, 1, "Nt_src")] = None
    delay_mask: Annotated[FloatRealOptional, (1, 1, "Nsrc")] = None

    # 5.4 IVP Source Terms (defined if `p0_source_flag = 1`)
    p0_source_input: Annotated[FloatReal, ("Nz", "Ny", "Nx")] = None


@dataclass
class KSpaceAndShiftVariables:
    """
    6. k-space and Shift Variables

    Not used
    """

    ...


@dataclass
class PML:
    """
    7. PML Variables
    """

    pml_x_size: LongReal
    pml_x_alpha: FloatReal

    pml_y_size: LongReal
    pml_y_alpha: FloatReal

    pml_z_size: LongReal = LongReal(0)
    pml_z_alpha: FloatRealOptional = None

    pml_x: Annotated[FloatRealOptional, (1, 1, "Nx")] = None
    pml_x_sgx: Annotated[FloatRealOptional, (1, 1, "Nx")] = None
    pml_y: Annotated[FloatRealOptional, (1, "Ny", 1)] = None
    pml_y_sgy: Annotated[FloatRealOptional, (1, "Ny", 1)] = None
    pml_z: Annotated[FloatRealOptional, ("Nz", 1, 1)] = None
    pml_z_sgz: Annotated[FloatRealOptional, ("Nz", 1, 1)] = None


@dataclass
class H5Input:
    simulation_flags: SimulationFlags
    grid: Grid
    medium: Medium
    sensor: Sensor
    source: Source
    pml: PML
    kspace: KSpaceAndShiftVariables = field(default_factory=KSpaceAndShiftVariables)
