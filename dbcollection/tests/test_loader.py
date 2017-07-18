"""
Test dbcollection/utils/loader.py.
"""


import os
import pytest
import dbcollection as dbc
from dbcollection.utils.string_ascii import convert_ascii_to_str as tostr_


loader = dbc.load('mnist')


@pytest.mark.parametrize("output", [
    (['0', '1','2', '3', '4', '5', '6', '7', '8', '9']),
])
def test_get_all(output):
    assert(output == tostr_(loader.get('train', 'classes')))


@pytest.mark.parametrize("output", [
    (['0', '1','2', '3', '4', '5', '6', '7', '8', '9']),
    (['0', '1','2', '3', '4']),
])
def test_get_range(output):
    assert(output == tostr_(loader.get('train', 'classes', list(range(len(output))))))


@pytest.mark.parametrize("output", [
    (['5', '6', '7', '8', '9']),
    (['1','2', '4']),
])
def test_get_range2(output):
    idx_list = [int(l) for l in output]
    assert(output == tostr_(loader.get('train', 'classes', idx_list)))


@pytest.mark.parametrize("output, index", [
    ([0, 5], 0),
    ([1, 0], 1),
    ([2, 4], 2),
    ([3, 1], 3),
    ([4, 9], 4),
])
def test_object_single(output, index):
    assert(output == loader.object('train', index).tolist())


@pytest.mark.parametrize("output, index", [
    ([[0, 5], [1, 0]], [0, 1]),
    ([[2, 4], [3, 1]], [2, 3]),
    ([[4, 9], [5, 2]], [4, 5]),
])
def test_object_two(output, index):
    assert(output == loader.object('train', index).tolist())


@pytest.mark.parametrize("field_name, output", [
    ('classes', [10, 2]),
    ('images', [60000, 28, 28]),
    ('object_ids', [60000, 2]),
])
def test_size_1(field_name, output):
    assert(output == loader.size('train', field_name))


def test_size_2():
    assert([60000, 2] == loader.size('train'))

def test_list():
    sample_field_names = ['classes',
                          'images',
                          'labels',
                          'list_images_per_class',
                          'object_fields',
                          'object_ids']
    assert(set(sample_field_names) == set(loader.list('train')))


@pytest.mark.parametrize("field_name, output", [
    ('images', 0),
    ('labels', 1),
])
def test_object_field_id(field_name, output):
    assert(output == loader.object_field_id('train', field_name))