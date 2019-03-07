""""Univariate distribution analysis

This module contains methods to create distribution plots for different types of features. It contains the
following methods:

- interval_distribution: Distribution analysis for interval scaled variables.
- nominal_distribution: Distribution analysis for nominal scaled variables.
- distribution: Distribution analysis. Measurement scale will be inferred from the data.
"""

# Author: Henrique Magalhães Soares
# Licence: MIT

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import gridspec
from matplotlib.axes import Axes
from typing import List, AnyStr, Tuple, Union
from .levels import infer_measurement_level
from .chart_helpers import label_bar, label_barh, make_percentage_labels


def _missing_distribution(arr: np.array, ax: Axes, **kwargs):
    """"Create a plot for missing values distribution in an numpy array

    Parameters
    ----------
    arr: Array containing the data
    ax: Matplotlib Axes object where we will draw the chart.
    **kwargs: Other named parameters that will be forwarded to _make_percentage_labels and matplotlib plot methods.
    """
    n = len(arr)
    n_miss = np.isnan(arr).sum()
    n_fill = n - n_miss

    headers = ["Filled", "Missing"]
    values = [n_fill, n_miss]

    ax.barh(headers, values, **kwargs)
    labels = make_percentage_labels(values, **kwargs)
    label_barh(ax, labels)


def _filled_distribution(arr: np.array, ax: Axes, **kwargs):
    """"Create a plot of the distribution of filled values in a numpy array

    Parameters
    ----------
    arr: Array containing the data
    ax: Matplotlib Axes object where we will draw the chart.
    **kwargs: Other named parameters that will be forwarded to _make_percentage_labels and matplotlib plot methods.
    """
    arr_notna = arr[~np.isnan(arr)]
    values, _, bars = ax.hist(arr_notna, edgecolor="white", **kwargs)
    labels = make_percentage_labels(values, **kwargs)
    label_bar(ax, labels)


def interval_distribution(arr: np.array, **kwargs) -> Tuple[plt.Figure, Tuple[Axes, Axes]]:
    """"Plot a distribution analysis for interval scaled features

    This function performs and plot the distribution analysis over a numpy array. This analysis consists in
    a missing values distribution (Plotting the percentage of NaN values versus valid values) as well as a
    histogram over the valid values.

    Parameters
    ----------
        arr: Numpy array, the array containing the data.
        **kwargs: Keyword arguments that will be forwarded to the underlying matplotlib functions.

    Returns
    -----------
        fig, (ax_fill, ax_dist)
        fig: Matplotlib figure
        ax_fill: Matplotlib Axes object for the missing values distribution plot
        ax_dist: Matplotlib Axes object for the filled values distribution plot
    """
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, figure=fig, height_ratios=(1, 2))
    ax_fill, ax_dist = (plt.subplot(gs_i) for gs_i in gs)

    _missing_distribution(arr, ax_fill, **kwargs)
    _filled_distribution(arr, ax_dist, **kwargs)
    return fig, (ax_fill, ax_dist)


def nominal_distribution(arr: np.array, **kwargs) -> Tuple[plt.Figure, Tuple[Axes]]:
    """"Plot a distribution analysis for nominal scaled features

    Parameters
    ----------
        arr: Numpy array, the array containing the data.
        **kwargs: Keyword arguments that will be forwarded to the underlying matplotlib functions.

    Returns
    -----------
        fig, (ax_fill, ax_dist)
        fig: Matplotlib figure
        ax_fill: Matplotlib Axes object for the missing values distribution plot
        ax_dist: Matplotlib Axes object for the filled values distribution plot
    """
    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1, figure=fig)
    ax = plt.subplot(gs[0])

    values, counts = np.unique(arr, return_counts=True)
    values = [str(v) for v in values]
    ax.barh(values, counts)

    labels = make_percentage_labels(counts, **kwargs)
    label_barh(ax, labels)

    return fig, ax


def distribution(arr: np.array, **kwargs) -> \
        Union[Tuple[str, plt.Figure, Tuple[Axes, Axes]], Tuple[str, plt.Figure, Tuple[Axes]]]:
    """"Plot a distribution analysis on the data contained within an array.

    The analysis depends of the measurement level of the data inside the array, which will be inferred from
    the data itself using the infer_measurement_level method. To learn more about the analysis generated, see
    the documentation on the following methods:

    - interval_distribution
    - nominal_distribution

    Parameters
    ----------
        arr: Numpy array, the array containing the data.
        **kwargs: Keyword arguments that will be forwarded to the underlying matplotlib and
            infer_meansurement_levels methods.

    Returns
    -----------
        measurement_level, fig, ax
            measurement_level: String indicating the inferred measurement level ("interval" or "nominal")
            fig: Matplotlib figure
            ax: Tuple containing the matplotlib Axes objects for the plots. The number of axes objects will
                depend on the measurement level (1 for nominal, 2 for interval)
    """
    measurement_level = infer_measurement_level(arr, **kwargs)
    if measurement_level == "interval":
        fig, ax = interval_distribution(arr, **kwargs)
    elif measurement_level == "nominal":
        fig, ax = nominal_distribution(arr, **kwargs)
    return measurement_level, fig, ax