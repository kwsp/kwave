# %%
import numpy as np
import matplotlib.pyplot as plt
import kwave

# %%
grid = kwave.Grid(
    Nx=128,  # number of grid points in the x (row) direction
    Ny=128,  # number of grid points in the y (column) direction
    dx=0.1e-3,  # grid point spacing in the x direction [m]
    dy=0.1e-3,  # grid point spacing in the y direction [m]
)

grid.make_time(1500)

# %%
medium = kwave.Medium(c0=1500.0, alpha_coeff=0.75, alpha_power=1.5)

# %%
from kwave.shapes import make_disc

disc1 = 5 * make_disc(grid.Nx, grid.Ny, 50, 50, 8)
disc2 = 3 * make_disc(grid.Nx, grid.Ny, 80, 60, 5)

# %%
source = kwave.Source(p0_source_input=disc1 + disc2)

# %%
from kwave.shapes import make_circle

sensor_mask = make_circle(
    Nx=grid.Nx,
    Ny=grid.Ny,
    cx=grid.Nx // 2,
    cy=grid.Ny // 2,
    radius=grid.Nx // 2 - 22,
    arc_angle=3 * np.pi / 2,
    plot=True,
)

# %%
sensor = kwave.Sensor.make_binary_sensor(sensor_mask=sensor_mask)

# %%
input, output = kwave.kspaceFirstOrder(
    grid=grid,
    medium=medium,
    sensor=sensor,
    source=source,
)


# %%
# Plot the initial pressure and sensor distribution
def vizualize_medium(h5inp: kwave.H5Input):
    sim = h5inp.simulation_flags
    grid = h5inp.grid
    sensor = h5inp.sensor

    source = h5inp.source

    if sim.p0_source_flag and len(grid.shape) == 2:
        shape = (grid.Ny, grid.Nx)

        mask = sensor.get_binary_mask(shape)
        p0 = source.p0_source_input
        if len(p0.shape) == 3:
            assert p0.shape[0] == 1
            p0 = p0[0]
        res = mask + p0

        f, ax = plt.subplots()
        extent = [0, grid.Nx * grid.dx * 1e3, grid.Ny * grid.dy * 1e3, 0]
        ax.imshow(res, extent=extent)
        ax.set_xlabel("x-position [mm]")
        ax.set_ylabel("y-position [mm]")


vizualize_medium(input)

# %%
# Plot the simulated sensor data
p = output.results.p

f, ax = plt.subplots()
im = ax.imshow(p[0].T)
f.colorbar(im)
ax.set_ylabel("Sensor Position")
ax.set_xlabel("Time Step")


# %%
# Plot the re-ordered sensor data
sensor_data_reordered = kwave.reorder_sensor_data(
    output.grid, input.sensor, output.results.p
)

f, ax = plt.subplots()
ax.imshow(sensor_data_reordered.T)
ax.set_ylabel("Sensor Position")
ax.set_xlabel("Time Step")
