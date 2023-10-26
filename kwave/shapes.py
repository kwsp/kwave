from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def make_disc(Nx: int, Ny: int, cx: int, cy: int, radius: float, plot=False):
    """
    Create a binary map of a filled disc within a 2D grid.

    DESCRIPTION:
        makeDisc creates a binary map of a filled disc within a
        two-dimensional grid (the disc position is denoted by 1's in the
        matrix with 0's elsewhere). A single grid point is taken as the disc
        centre thus the total diameter of the disc will always be an odd
        number of grid points. As the returned disc has a constant radius, if
        used within a k-Wave grid where dx ~= dy, the disc will appear oval
        shaped. If part of the disc overlaps the grid edge, the rest of the
        disc will wrap to the grid edge on the opposite side.

    USAGE:
        disc = makeDisc(Nx, Ny, cx, cy, radius)
        disc = makeDisc(Nx, Ny, cx, cy, radius, plot_disc)

    INPUTS:
        Nx, Ny          - size of the 2D grid [grid points]
        cx, cy          - centre of the disc [grid points]
        radius          - disc radius [grid points]

    OPTIONAL INPUTS:
        plot_disc       - Boolean controlling whether the disc is plotted
                        using imagesc (default = false)

    OUTPUTS:
        disc            - 2D binary map of a filled disc

    See also makeCircle, makeBall
    """
    cx, cy = round(cx), round(cy)
    if not (cx in range(Nx) and cy in range(Ny)):
        raise ValueError("Disc center must be within grid.")

    arr = np.zeros((Ny, Nx), dtype=np.uint8)

    # Generate an array of indices that covers the specified region
    y, x = np.ogrid[:Ny, :Nx]

    # Mask the pixels inside the circle
    mask = (x - cx) ** 2 + (y - cy) ** 2 <= radius**2
    arr[mask] = 1

    if plot:
        # You can visualize the result using Matplotlib
        plt.imshow(arr, cmap="gray")
        plt.xlabel("x-position [grid points]")
        plt.ylabel("y-position [grid points]")
        plt.show()

    return arr


def make_circle(
    Nx: int,
    Ny: int,
    cx: int,
    cy: int,
    radius: float,
    arc_angle: float | None = None,
    plot=False,
):
    """
    Create a binary map of a circle within a 2D grid.

    DESCRIPTION:
        makeCircle creates a binary map of a circle or arc (using the
        midpoint circle algorithm) within a two-dimensional grid (the circle
        position is denoted by 1's in the matrix with 0's elsewhere). A
        single grid point is taken as the circle centre thus the total
        diameter will always be an odd number of grid points.

        Note: The centre of the circle and the radius are not constrained by
        the grid dimensions, so it is possible to create sections of circles,
        or a blank image if none of the circle intersects the grid.

    USAGE:
        circle = makeCircle(Nx, Ny, cx, cy, radius)
        circle = makeCircle(Nx, Ny, cx, cy, radius, arc_angle)
        circle = makeCircle(Nx, Ny, cx, cy, radius, arc_angle, plot_circle)

    INPUTS:
        Nx, Ny          - size of the 2D grid [grid points]
        cx, cy          - centre of the circle [grid points], if set to 0,
                        the centre of the grid is used
        radius          - circle radius [grid points]

    OPTIONAL INPUTS:
        arc_angle       - arc angle for incomplete circle [radians]
                        (default = 2*pi)
        plot_circle     - Boolean controlling whether the circle is plotted
                        using imagesc (default = false)

    OUTPUTS:
        circle          - 2D binary map of a circle

    See also makeCartCircle, makeDisc

    TODO: the circle is not exactly the same as makeCircle from MATLAB
    """
    cx, cy = round(cx), round(cy)
    if not (cx in range(Nx) and cy in range(Ny)):
        raise ValueError("Circle center must be within grid.")

    # Create an empty array filled with zeros
    arr = np.zeros((Ny, Nx), dtype=np.uint8)

    # Bresenham's circle drawing algorithm to draw a continuous circumference
    x, y = radius, 0
    err = 0

    while x >= y:
        # Set the corresponding points on all octants of the circle
        arr[cy + y, cx + x] = 1
        arr[cy + x, cx + y] = 1
        arr[cy + y, cx - x] = 1
        arr[cy + x, cx - y] = 1
        arr[cy - y, cx - x] = 1
        arr[cy - x, cx - y] = 1
        arr[cy - y, cx + x] = 1
        arr[cy - x, cx + y] = 1

        if err <= 0:
            y += 1
            err += 2 * y + 1

        if err > 0:
            x -= 1
            err -= 2 * x + 1

    if arc_angle is not None:
        # Generate an array of indices that covers the specified region
        y, x = np.ogrid[:Ny, :Nx]

        # Calculate the angle from the center to each pixel
        angles = np.arctan2(y - cy, x - cx)
        angles[angles < 0] += 2 * np.pi

        # Use the angle to mask the pixels within the specified arc
        start_angle = 0
        mask = (angles >= start_angle) & (angles <= arc_angle)

        arr = mask & arr

    if plot:
        # You can visualize the result using Matplotlib
        plt.imshow(arr, cmap="gray")
        plt.xlabel("x-position [grid points]")
        plt.ylabel("y-position [grid points]")
        plt.show()

    return arr
