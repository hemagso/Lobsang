""""Bivariate analysis

This module contains methods analyze the bivariate relationship between features


"""

# Author: Henrique Magalhães Soares
# Licence: MIT

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib import gridspec
from typing import Tuple, List


def _groupby(keys, values, agg):
    aggregated = {key: agg(values[keys == key]) for key in np.unique(keys)}
    keys = np.array(list(aggregated.keys()))
    values = np.array(list(aggregated.values()))
    return keys, values


def bivariate_nom_int(arr_nom: np.array, arr_int: np.array) -> Tuple[plt.Figure, Axes]:
    keys, values = _groupby(arr_nom, arr_int, np.mean)
    keys = np.array([str(v) for v in keys])

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 1, figure=fig)
    ax = plt.subplot(gs[0])

    ax.bar(keys, values)

    return fig, ax