import numpy as np
from matplotlib.axes import Axes
from typing import List, Tuple, AnyStr


def label_barh(ax: Axes, labels: List[AnyStr]):
    """"Labels the bars of a matplotlib Horizontal Bar Plot (plt.barh)

    todo: Adjust axis to fit labels in a smarter way

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
        ax.annotate(label, xy=(x, y), ha="left", va="center", clip_on=True)
        # We increase the axis by 3% to fit the labels.
        x_min, x_max = ax.get_xlim()
        ax.set_xlim(x_min, 1.03*x_max)


def label_bar(ax: Axes, labels: List[AnyStr]):
    """"Labels the bars of a matplotlib Bar Plot (plt.bar)

    todo: Adjust axis to fit labels in a smarter way

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
        ax.annotate(label, xy=(x, y), ha="center", va="bottom", clip_on=True)
        # We increase the axis by 3% to fit the labels.
        y_min, y_max = ax.get_ylim()
        ax.set_ylim(y_min, 1.03*y_max)


def make_percentage_labels(values: List[float], decimals: int = 1):
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
