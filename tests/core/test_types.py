"""
Test dbcollection/core/loader.py.
"""

import os
import numpy as np
from numpy.testing import assert_array_equal
import pytest

from dbcollection.core.types import (
    parse_data_format_by_type,
    parse_filename,
    parse_string,
    parse_number,
    parse_boolean,
    parse_list_string,
    parse_list_number,
    parse_list_boolean,
    parse_list_of_lists_number
)
from dbcollection.utils.string_ascii import convert_str_to_ascii
from dbcollection.utils.pad import pad_list, squeeze_list, unsqueeze_list


def test_parse_data_format_by_type__convert_filename():
    data = convert_str_to_ascii('dummy_var.jpg')
    ctype = 'filename'
    path = '/some/dir'
    data_parsed = parse_data_format_by_type(data, ctype, path)
    assert data_parsed == '/some/dir/dummy_var.jpg'


def test_parse_filename():
    data = convert_str_to_ascii('/some/path/to/file.jpg')
    data_parsed = parse_filename(data)
    assert data_parsed == '/some/path/to/file.jpg'


def test_parse_filename___multiple_filenames():
    data = convert_str_to_ascii(['/some/path/to/file1.jpg', '/some/path/to/file2.jpg'])
    data_parsed = parse_filename(data)
    assert data_parsed == ['/some/path/to/file1.jpg', '/some/path/to/file2.jpg']


def test_parse_filename__join_path():
    data = convert_str_to_ascii('/some/path/to/file.jpg')
    path = '/root/dir/path'
    data_parsed = parse_filename(data, path)
    assert data_parsed == '/root/dir/path/some/path/to/file.jpg'


def test_parse_filename__multiple_filenames_join_path():
    data = convert_str_to_ascii(['/some/path/to/file1.jpg', '/some/path/to/file2.jpg'])
    path = '/root/dir/path'
    data_parsed = parse_filename(data, path)
    assert data_parsed == ['/root/dir/path/some/path/to/file1.jpg', '/root/dir/path/some/path/to/file2.jpg']


def test_parse_string():
    data = convert_str_to_ascii('/some/path/to/file.jpg')
    assert parse_string(data) == '/some/path/to/file.jpg'


def test_parse_string__multiple_strings():
    data = convert_str_to_ascii(['/some/path/to/file1.jpg', '/some/path/to/file2.jpg'])
    assert parse_string(data) == ['/some/path/to/file1.jpg', '/some/path/to/file2.jpg']


def test_parse_number():
    data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert parse_number(data) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_parse_number__multidimensional():
    data = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    assert parse_number(data) == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]


def test_parse_number__single_value():
    data = np.array([101])
    assert parse_number(data) == 101


def test_parse_boolean():
    data = np.array([0, 1, 1, 0], dtype=np.uint8)
    assert parse_boolean(data) == [False, True, True, False]


def test_parse_boolean__single1():
    data = np.array([0], dtype=np.uint8)
    assert parse_boolean(data) == False


def test_parse_boolean__single2():
    data = np.array([1], dtype=np.uint8)
    assert parse_boolean(data) == True


def test_parse_list_string():
    data = [['string1', 'string2'], ['string3', 'string4']]
    data_ = np.array([convert_str_to_ascii(l) for l in data], dtype=np.uint8)
    assert parse_list_string(data_) == data


def test_parse_list_string__uneven_list():
    data = [['string1', 'string2'], ['string3']]
    data_ = np.array([convert_str_to_ascii(l) for l in pad_list(data, val='')], dtype=np.uint8)
    assert parse_list_string(data_) == data


def test_parse_list_number():
    data = [[1], [2, 3], [4, 5, 6]]
    data_ = np.array(pad_list(data, val=-1))
    assert parse_list_number(data_, pad_value=-1) == data


def test_parse_list_number__list_with_single_value():
    data = [[1]]
    data_ = np.array(pad_list(data, val=-1))
    assert parse_list_number(data_, pad_value=-1) == data


def test_parse_list_boolean():
    data = [[0, 1], [0, 1, 1, 0], [0]]
    data_ = np.array(pad_list(data, val=-1), dtype=np.uint8)
    assert parse_list_boolean(data_, pad_value=-1) == [[False, True], [False, True, True, False], [False]]


def test_parse_list_boolean():
    data = [[0, 1]]
    data_ = np.array(pad_list(data, val=-1), dtype=np.uint8)
    assert parse_list_boolean(data_, pad_value=-1) == [[False, True]]


def test_parse_list_of_lists_number():
    data = [[[0, 1], [0, 1, 1, 0], [0]],
            [[1, 2, 3], [4, 5, 6, 7, 8], [9]]]
    data_ = np.array(pad_list([squeeze_list(l, val=-1) for l in data]), dtype=np.int32)
    assert parse_list_of_lists_number(data_, pad_value=-1) == data


def test_parse_list_of_lists_number__single_list():
    data = [[[0, 1], [0, 1, 1, 0], [0]]]
    data_ = np.array(pad_list([squeeze_list(l, val=-1) for l in data]), dtype=np.int32)
    assert parse_list_of_lists_number(data_, pad_value=-1) == data
