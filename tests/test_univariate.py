import pytest
from lobsang.univariate import _label_barh, _label_bar, _make_percentage_labels
import matplotlib.pyplot as plt


def test__make_percentage_labels():
    values = [2, 2, 4]
    assert _make_percentage_labels(values) == ["25.0%", "25.0%", "50.0%"]
    assert _make_percentage_labels(values, decimals=2) == ["25.00%", "25.00%", "50.00%"]
    with pytest.raises(TypeError):
        _make_percentage_labels(["a", "b", "c"])


@pytest.fixture()
def barh_ax():
    headers = ["Missing", "Filled"]
    values = [10, 20]
    _, ax = plt.subplots(1,1)
    ax.barh(headers, values)
    return ax


@pytest.fixture()
def barh_labels_1():
    return ["33.3%", "66.7%"]


@pytest.fixture()
def barh_labels_2():
    return ["20.0%", "50.0%", "30.0%"]


def test__label_barh_1(barh_ax, barh_labels_1):
    _label_barh(barh_ax, barh_labels_1)


def test__label_barh_2(barh_ax, barh_labels_2):
    with pytest.raises(AssertionError):
        _label_barh(barh_ax, barh_labels_2)


if __name__ == "__main__":
    pytest.main([__file__])
