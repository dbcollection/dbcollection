"""
Test dbcollection/utils/pad.py.
"""


import pytest
from dbcollection.utils.pad import pad_list, unpad_list, squeeze_list, unsqueeze_list


@pytest.mark.parametrize("sample, output, fill_value", [
    ([[5, 1, 3], [9, 17, 324]], [[5, 1, 3], [9, 17, 324]], -1),
    ([[1, 1, 0], [1, 0]], [[1, 1, 0], [1, 0, -1]], -1),
    ([[1, 1, 0], [1, 0]], [[1, 1, 0], [1, 0, 0]], 0),
    ([[9, 99, 999, 9999], [], [1, 2, 10]], [[9, 99, 999, 9999],
                                            [3, 3, 3, 3],
                                            [1, 2, 10, 3]], 3),
])
def test_pad_list(sample, output, fill_value):
    assert(output == pad_list(sample, fill_value))


@pytest.mark.parametrize("sample, output, fill_value", [
    ([[1, 2, 3, -1, -1], [5, 6, -1, -1, -1]], [[1, 2, 3], [5, 6]], -1),
    ([[5, 0, -1], [1, 2, 3, 4, 5]], [[0, -1], [1, 2, 3, 4]], 5),
])
def test_unpad_list(sample, output, fill_value):
    assert(output == unpad_list(sample, fill_value))


@pytest.mark.parametrize("sample, output, fill_value", [
    ([[1,2], [3], [4,5,6]], [1, 2, -1, 3, -1, 4, 5, 6], -1),
    ([[1,1,1,1,1], [-1,-1,-1,-1,-1]], [1,1,1,1,1,9999, -1,-1,-1,-1,-1], 9999)
])
def test_squeeze_list(sample, output, fill_value):
    assert(output == squeeze_list(sample, fill_value))


@pytest.mark.parametrize("sample, output, fill_value", [
    ([1, 2, -1, 3, -1, 4, 5, 6], [[1,2], [3], [4,5,6]], -1),
    ([1,1,1,1,1,9999, -1,-1,-1,-1,-1], [[1,1,1,1,1], [-1,-1,-1,-1,-1]], 9999)
])
def test_unsqueeze_list(sample, output, fill_value):
    assert(output == unsqueeze_list(sample, fill_value))