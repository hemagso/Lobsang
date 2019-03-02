import pytest
import numpy as np
from lobsang.levels import _infer_measurement_by_count, infer_measurement_level


def test__infer_measurement_by_count():
    arr = np.random.rand(100)
    assert _infer_measurement_by_count(arr) == "interval"
    assert _infer_measurement_by_count(arr, threshold=20) == "interval"
    assert _infer_measurement_by_count(arr, threshold=20, use_first=10) == "nominal"
    arr = np.array(10*[1] + 20*[2] + 30*[5] + 50*[6] + 75*[9] + 200*[1500])
    assert _infer_measurement_by_count(arr) == "nominal"
    assert _infer_measurement_by_count(arr,  threshold=6) == "interval"


def test_infer_measurement_level():
    arr = np.random.rand(100)
    assert infer_measurement_level(arr) == "interval"
    assert infer_measurement_level(arr, threshold=20) == "interval"
    assert infer_measurement_level(arr, threshold=20, use_first=10) == "nominal"
    arr = np.array(10*[1] + 20*[2] + 30*[5] + 50*[6] + 75*[9] + 200*[1500])
    assert infer_measurement_level(arr) == "nominal"
    assert infer_measurement_level(arr,  threshold=6) == "interval"


if __name__ == "__main__":
    pytest.main([__file__])
