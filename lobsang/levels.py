import numpy as np
from typing import Union, AnyStr

MEASUREMENT_LEVELS = ["nominal", "interval"]


def infer_measurement_level(arr: np.array, method: AnyStr = "count_unique", **kwargs) -> str:
    """"Infers the measurement level for the data in an array

    This function infers the measurement level of a feature stored within a numpy array. The measurement
    levels can be one of two categories:

    - interval: Variables in which the interval between values is meaningful in some way.
    - nominal: Variables in which only identity between values is meaningful in some way.

    This classification is a simplification of Stanley Smith Stevens Level of Measurement classification.
    More about it can be read in this Wikipedia article (https://en.wikipedia.org/wiki/Level_of_measurement)

    To classify correcly between these measurement levels one usually has to have knowledge about the process
    generating the data. However, sometimes this measurement levels are reflected in the data itself. To make
    the inference, this function currently has 1 available method:

    - count_unique: This method decide the measurement level based on the number of unique values present on the
        data. For more detais about it, see the documentation for the _infer_measurement_by_count method.

    Parameters
    ----------
    arr: Numpy array containing the data
    method: Method to be used to infer the measurement level. Default: count_unique.
    kwargs: Other named arguments used by each method.

    Returns
    ----------
    measurement_level: String with one of these two values: "interval", "nominal"

    """
    assert method in ["count_unique"], "Invalid inference method"
    if method == "count_unique":
        return _infer_measurement_by_count(arr, **kwargs)


def _infer_measurement_by_count(arr: np.array, threshold: int = 10, use_first: Union[None, int] = None) -> str:
    if use_first:
        arr = arr[0:use_first]
    unique_count = len(np.unique(arr))
    if unique_count >= threshold:
        return "interval"
    else:
        return "nominal"
