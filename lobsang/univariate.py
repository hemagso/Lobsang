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


def _label_barh(ax: Axes, labels: List[AnyStr]):
    """"Labels the bars of a matplotlib Horizontal Bar Plot (plt.barh)

    todo: Adjust Axis scales to fit the labels

    Parameters
    ----------
    ax: Axes object containing the plot we wish to label
    labels: List containing the labels of each column
    """
    bars = ax.patches
    assert len(bars) == len(labels), "Number of labels is different from the number of bars"
    for bar, label in zip(bars, labels):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.text(x, y, label, ha='left', va='center')


def _label_bar(ax: Axes, labels: List[AnyStr]):
    """"Labels the bars of a matplotlib Bar Plot (plt.bar)

    todo: Adjust Axis scales to fit the labels

    Parameters
    ----------
    ax: Axes object containing the plot we wish to label
    labels: List containing the labels of each column
    """
    bars = ax.patches
    assert len(bars) == len(labels), "Number of labels is different from the number of bars"
    for bar, label in zip(bars, labels):
        x = bar.get_x() + bar.get_width()/2
        y = bar.get_height()
        ax.text(x, y, label, ha='center', va='bottom')


def _make_percentage_labels(values: List[float], decimals: int = 1):
    """"Create percentage labels from a collection of values

    This function transforms a list of values into a list of percentages correspondent to those values.
    The percentages will be calculated by dividing each value by the sum of all values in the collection.

    Parameters
    ----------
    values: A list of numbers
    decimals: The number of decimal places to be used in the percentages. Default: 1.

    Returns
    ----------
    labels: List containing strings with the percentages
    """
    values = np.array(values)
    values = values / values.sum()
    labels = ["{value:.{decimals}%}".format(value=value, decimals=decimals) for value in values]
    return labels


def _missing_distribution(arr: np.array, ax: Axes, **kwargs):
    n = len(arr)
    n_miss = np.isnan(arr).sum()
    n_fill = n - n_miss

    headers = ["Filled", "Missing"]
    values = [n_fill, n_miss]

    ax.barh(headers, values, **kwargs)
    labels = _make_percentage_labels(values)
    _label_barh(ax, labels)


def _filled_distribution(arr: np.array, ax: Axes, **kwargs):
    arr_notna = arr[~np.isnan(arr)]
    values, _, bars = ax.hist(arr_notna, **kwargs)
    labels = _make_percentage_labels(values)
    _label_bar(ax, labels)


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
    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1, figure=fig, height_ratios=(1, 1))
    ax = plt.subplot(gs[0])

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