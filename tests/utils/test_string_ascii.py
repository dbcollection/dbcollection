"""
Test dbcollection/utils/string_ascii.py.
"""


import pytest
import numpy as np
from dbcollection.utils.string_ascii import (str_to_ascii,
                                             ascii_to_str,
                                             convert_str_to_ascii,
                                             convert_ascii_to_str)


testdata_single_string = [
    ('string1', [115, 116, 114, 105, 110, 103, 49]),
    ('string2', [115, 116, 114, 105, 110, 103, 50]),
    ('string3', [115, 116, 114, 105, 110, 103, 51]),
    ('one', [111, 110, 101]),
    ('two', [116, 119, 111]),
    ('three', [116, 104, 114, 101, 101])
]

testdata_multiple_strings = [
    (['string1', 'string2', 'string3'], [[115, 116, 114, 105, 110, 103, 49, 0],
                                         [115, 116, 114, 105, 110, 103, 50, 0],
                                         [115, 116, 114, 105, 110, 103, 51, 0]]),
    (['one', 'two', 'three', 'four'], [[111, 110, 101, 0, 0, 0],
                                       [116, 119, 111, 0, 0, 0],
                                       [116, 104, 114, 101, 101, 0],
                                       [102, 111, 117, 114, 0, 0]]),
    (['will', 'it', 'blend?'], [[119, 105, 108, 108, 0, 0, 0],
                                [105, 116, 0, 0, 0, 0, 0],
                                [98, 108, 101, 110, 100, 63, 0]])
]


@pytest.mark.parametrize("sample, output", testdata_single_string)
def test_str_to_ascii(sample, output):
    res = str_to_ascii(sample)
    assert(output == res.tolist())

@pytest.mark.parametrize("output, sample", testdata_single_string)
def test_ascii_to_str(sample, output):
    res = ascii_to_str(np.array(sample, dtype=np.uint8))
    assert(output == res)

@pytest.mark.parametrize("sample, output", testdata_single_string)
def test_convert_str_to_ascii_single_string(sample, output):
    res = convert_str_to_ascii(sample)
    assert(output + [0] == res.tolist())

@pytest.mark.parametrize("sample, output", testdata_multiple_strings)
def test_convert_str_to_ascii_multiple_strings(sample, output):
    res = convert_str_to_ascii(sample)
    assert(output == res.tolist())

@pytest.mark.parametrize("output, sample", testdata_single_string)
def test_convert_ascii_to_str_single_string(sample, output):
    res = convert_ascii_to_str(np.array(sample, dtype=np.uint8))
    assert(output == res)

@pytest.mark.parametrize("output, sample", testdata_multiple_strings)
def test_convert_ascii_to_str_multiple_strings(sample, output):
    res = convert_ascii_to_str(np.array(sample, dtype=np.uint8))
    assert(output == res)
