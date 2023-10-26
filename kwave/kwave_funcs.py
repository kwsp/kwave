"""
Implements some MATLAB functions from the k-Wave package
"""
from __future__ import annotations
import numpy as np
from numpy import fft
import matplotlib.pyplot as plt

from kwave.h5output import Grid, Sensor


def gaussian(x, magnitude=None, mean=0, variance=1):
    """
    INPUTS:
        x           - x-axis variable

    OPTIONAL INPUTS:
        magnitude   - bell height (default = normalised)
        mean        - mean or expected value (default = 0)
        variance    - variance ~ bell width (default = 1)

    ABOUT: ported from MATLAB
    """
    if magnitude is None:
        magnitude = (2 * np.pi * variance) ** -0.5

    gauss_distr = magnitude * np.exp(-((x - mean) ** 2) / (2 * variance))
    return gauss_distr


def gaussian_filter(
    x: np.ndarray, Fs: float, freq: float, bandwidth: float, plot: bool = False
):
    """frequency domain Gaussian filter
    DESCRIPTION:
        gaussianFilter applies a frequency domain Gaussian filter with the
        specified center frequency and percentage bandwidth to the input
        signal. If the input signal is given as a matrix, the filter is
        applied to each matrix row.

    INPUTS:
        signal      - signal/s to filter
        Fs          - sampling frequency [Hz]
        freq        - filter center frequency [Hz]
        bandwidth   - filter bandwidth [%]

    OPTIONAL INPUTS:
        plot_filter - Boolean controlling whether the filtering process is
                    plotted

    OUTPUTS:
        signal      - filtered signal/s

    ABOUT: ported from k-Wave
    """
    N = x.shape[1]
    if N % 2 == 0:
        # N is even
        f = np.arange(-N // 2, N // 2) * Fs / N
    else:
        # N is odd
        f = np.arange(-(N - 1) // 2, (N - 1) // 2 + 1) * Fs / N

    # compute gaussian filter coefficients
    mean = freq
    variance = (bandwidth / 100 * freq / (2 * np.sqrt(2 * np.log(2)))) ** 2
    magnitude = 1

    # create the double-sided Gaussian filter
    gauss_filter = np.maximum(
        gaussian(f, magnitude, mean, variance), gaussian(f, magnitude, -mean, variance)
    )

    # apply filter
    x_filt = np.real(
        fft.ifft(fft.ifftshift(gauss_filter * fft.fftshift(fft.fft(x), -1), -1))
    )

    # plot filter
    if plot:
        # compute amplitude spectrum of central signal element
        as_ = fft.fftshift(np.abs(fft.fft(x[len(x // 2)])) / N, -1)
        af = fft.fftshift(np.abs(fft.fft(x_filt[len(x_filt) // 2])) / N, -1)

        # get axis scaling factors
        # [f_sc, f_scale, f_prefix] = scaleSI(f)

        # produce plot
        fig, ax = plt.subplots()
        # ax.plot(f * f_scale, as_ / np.max(as_), 'k-')
        ax.plot(f, as_ / np.max(as_), "k-", label="Original Signal")
        # ax.plot(f * f_scale, gauss_filter, 'b-');
        ax.plot(f, gauss_filter, "b-", label="Gaussian Filter")
        # ax.plot(f * f_scale, as_filtered / np.max(as_), 'r-')
        ax.plot(f, af / np.max(as_), "r-", label="Filtered Signal")
        # ax.set_xlabel('Frequency [' f_prefix 'Hz]')
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("Normalised Amplitude")
        ax.legend()
        plt.tight_layout()
        # ax.set_xlim([0, f(end) .* f_scale])
        ax.set_xlim([0, f[-1]])
        ax.set_ylim([0, 1])

    return x


def envelope_detection(x: np.ndarray):
    """Extract signal envelope using the Hilbert Transform.
    DESCRIPTION:
        envelopeDetection applies the Hilbert transform to extract the
        envelope from an input vector x. If x is a matrix, the envelope along
        each row is returned.

        Example:
            x = toneBurst(10e6, 0.5e6, 10);
            plot(0:length(x) - 1, x, 'k-', 0:length(x) - 1, envelopeDetection(x), 'r-');
            legend('Input Signal', 'Envelope');

    INPUTS:
        x           - input function

    OUTPUTS:
        env         - envelope of input function

    ABOUT: ported from k-Wave
    """

    if len(x.shape) == 1:
        x = np.expand_dims(x, 0)

    # compute the FFT of the input function (use zero padding to prevent
    # effects of wrapping at the beginning of the envelope), if x is a matrix
    # the fft's are computed across each row
    X = fft.fft(x, x.shape[1] * 2, -1)

    # multiply the fft by -1i
    X = -1j * X

    # set the DC frequency to zero
    X[0] = 0

    # calculate where the negative frequencies start in the FFT
    neg_f_index = int(np.ceil(X.shape[1] / 2))

    # multiply the negative frequency components by -1
    X[:, neg_f_index:] = -X[:, neg_f_index:]

    # compute the Hilbert transform using the inverse fft
    z = fft.ifft(X)

    # extract the envelope
    env = np.abs(x + 1j * z[:, : x.shape[1]])
    return env


def log_compression(signal: np.ndarray, a: float, normalise=False):
    """Log compress an input signal.
    DESCRIPTION:
        logCompression compresses the input signal using the expression
        signal = log10(1 + a * signal) ./ log10(1 + a)

    USAGE:
        signal = logCompression(signal, a)
        signal = logCompression(signal, a, normalise)

    INPUTS:
        signal      - input signal
        a           - compression factor

    OPTIONAL INPUTS
        normalise   - Boolean controlling whether the maximum of the input
                    signal is normalised to unity before compression
                    (default = false). If set to true, the original
                    magnitude is restored after compression.

    OUTPUTS:
        signal      - log compressed signal

    ABOUT: ported from k-Wave
    """
    # compress signal
    if normalise:
        mx = np.max(signal)
        signal = mx * (np.log10(1 + a * signal / mx) / np.log10(1 + a))
    else:
        signal = np.log10(1 + a * signal) / np.log10(1 + a)

    return signal


def stacked_plot(tt: np.ndarray, xx: np.ndarray, labels: list, xlabel=None):
    """Stacked linear plot.
    DESCRIPTION:
        stackedPlot produces a series of stacked linear plots of the rows in
        data (a 2D matrix) against the vector x. The vector y defines the
        y-axis label for each linear plot. The plot scaling is defined using
        the global maximum and minimum of the data. The plot can be annotated
        in the normal fashion after display.

    INPUTS:
        x       - vector defining the x-axis values
        y       - vector defining the y-axis labels used for each plot
        data    - 2D matrix to plot

    ABOUT: ported from k-wave
    """
    N = xx.shape[0]
    assert N == len(labels)
    _, ax = plt.subplots(N, 1, sharex=True)
    for i, label in enumerate(labels):
        ax[i].plot(tt, xx[i])
        ax[i].set_yticks([np.mean(ax[i].get_ylim())])
        ax[i].set_yticklabels([label])
    if xlabel:
        plt.xlabel(xlabel)
    plt.tight_layout()


def reorder_sensor_data(kgrid: Grid, sensor: Sensor, sensor_data: np.ndarray):
    """
    Reorder sensor data from kspaceFirstOrder2D based on angle.

    DESCRIPTION:
        reorderSensorData reorders the time series from kspaceFirstOrder2D
        based on the angle that each sensor point makes with the centre of
        the grid. The sensor mask must be a binary mask, and the angles are
        defined from the upper left quadrant or negative y-axis in the same
        way as within makeCircle and makeCartCircle.

    USAGE:
        [reordered_sensor_data, indices_new] = reorderSensorData(kgrid, sensor, sensor_data)

    INPUTS:
        kgrid         - k-Wave grid object returned by kWaveGrid
        sensor        - k-Wave sensor structure where sensor.mask is
                        defined as binary grid
        sensor_data   - sensor data returned by kspaceFirstOrder2D ordered
                        using MATLAB's standard column-wise linear matrix
                        indexing

    OUTPUTS:
        reordered_sensor_data
                    - time varying sensor data reordered by the angle that
                        each sensor point makes with the centre of the grid

    ABOUT:
        author        - Ben Cox
        date          - 30th May 2012
        last update   - 21st March 2019

    """
    # check simulation is 2D
    if not kgrid.is_2D():
        raise ValueError("The simulation must be 2D.")

    if len(sensor_data.shape) == 3:
        assert sensor_data.shape[0] == 1
        sensor_data = sensor_data[0]

    # check sensor.mask is a binary mask
    ...

    # find the coordinates of the sensor points
    y_sensor, x_sensor = sensor.get_xy_sensor_mask_index(kgrid.shape)

    # find the angle of each sensor point (from the centre)
    angle = np.arctan2(-x_sensor, -y_sensor)
    angle[angle < 0] += 2 * np.pi

    # sort the sensor points in order of increasing angle
    sort_idx = np.argsort(angle)

    # reorder the measure time series so that adjacent time series correspond
    # to adjacent sensor points.
    reordered_sensor_data = sensor_data[:, sort_idx]
    return reordered_sensor_data
