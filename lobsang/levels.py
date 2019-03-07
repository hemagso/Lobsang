""""Univariate distribution analysis

This module contains methods to identify and deal with different measurement levels. It contains the following
methods:

- infer_measurement_level: Determines the measurement level of a feature from the data.
"""

# Author: Henrique Magalhães Soares
# Licence: MIT

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

    The following methods are available for use:

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
    """"Infers the measurement scale of a feature by using the count method

    This method uses the fact that interval measurement level variables usually are real valued features
    and, therefore, have a lot of different values. In contrast to that, nominal variables usually are the
    result of discrete categorization, having a smaller set of unique values.

    This is of course not a rule. Counts are integer valued on the interval scale, and may have few values.
    ZIP codes are nominal level features with lot's of unique values. It's always best to understand your
    data generating process, assigning it the appropriate measurement level.

    This function counts the number of unique values in a numpy array, and classifies it as interval if
    this number is above a threshold.

    Parameters
    ----------
    arr: Numpy array containing the data
    threshold: Threshold of unique values for the classification. Default: 10
    use_first: Number of elements on the array to be used when counting unique values. Default: None (Use all values)

    Returns
    ----------
    measurement_level: String with one of these two values: "interval", "nominal"


    """
    if use_first:
        arr = arr[0:use_first]
    unique_count = len(np.unique(arr))
    if unique_count >= threshold:
        return "interval"
    else:
        return "nominal"
