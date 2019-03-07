import numpy as np


def groupby(keys, values, agg):
    aggregated = {key: agg(values[keys == key]) for key in np.unique(keys)}
    keys = np.array(list(aggregated.keys()))
    values = np.array(list(aggregated.values()))
    return keys, values
