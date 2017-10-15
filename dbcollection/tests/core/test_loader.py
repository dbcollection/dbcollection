"""
Test dbcollection/utils/loader.py.
"""


import pytest
import dbcollection as dbc
from dbcollection.core.api import config_cache
from dbcollection.utils.string_ascii import convert_ascii_to_str as tostr_


@pytest.fixture(scope="module")
def loader():
    config_cache(reset_cache=True, is_test=True)
    return dbc.load('mnist', is_test=True)


@pytest.mark.parametrize("output", [
    (['0', '1','2', '3', '4', '5', '6', '7', '8', '9']),
])
def test_get_all(output, loader):
    assert(output == tostr_(loader.get('train', 'classes')))


@pytest.mark.parametrize("output", [
    (['0', '1','2', '3', '4', '5', '6', '7', '8', '9']),
    (['0', '1','2', '3', '4']),
])
def test_get_range(output, loader):
    assert(output == tostr_(loader.get('train', 'classes', list(range(len(output))))))


@pytest.mark.parametrize("output", [
    (['5', '6', '7', '8', '9']),
    (['1','2', '4']),
])
def test_get_range2(output, loader):
    idx_list = [int(l) for l in output]
    assert(output == tostr_(loader.get('train', 'classes', idx_list)))


@pytest.mark.parametrize("output, index", [
    ([0, 5], 0),
    ([1, 0], 1),
    ([2, 4], 2),
    ([3, 1], 3),
    ([4, 9], 4),
])
def test_object_single(output, index, loader):
    assert(output == loader.object('train', index).tolist())


@pytest.mark.parametrize("output, index", [
    ([[0, 5], [1, 0]], [0, 1]),
    ([[2, 4], [3, 1]], [2, 3]),
    ([[4, 9], [5, 2]], [4, 5]),
])
def test_object_two(output, index, loader):
    assert(output == loader.object('train', index).tolist())


def test_object_no_index(loader):
    assert((60000, 2) == loader.object('train').shape)

def test_object_empty_index(loader):
    with pytest.raises(ValueError):
        shape = loader.object('train', []).shape

@pytest.mark.parametrize("field_name, output", [
    ('classes', (10, 2)),
    ('images', (60000, 28, 28)),
    ('object_ids', (60000, 2)),
])
def test_size_1(field_name, output, loader):
    assert(output == loader.size('train', field_name))


def test_size_2(loader):
    assert((60000, 2) == loader.size('train'))

def test_list(loader):
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
def test_object_field_id(field_name, output, loader):
    assert(output == loader.object_field_id('train', field_name))


def test_info(loader):
    loader.info()
    pass


@pytest.mark.parametrize("set_name", [
    ('train'),
    ('test'),
])
def test_info_set_succeed(set_name, loader):
    loader.info(set_name)
    pass


@pytest.mark.parametrize("set_name", [
    ('train1'),
    ('val'),
])
def test_info_set_fail(set_name, loader):
    with pytest.raises(Exception):
        loader.info(set_name)


#@pytest.mark.parametrize("set_name", [
#    ('train'),
#    ('test'),
#])
#def test__print_info_succeed(set_name, loader):
#    loader._print_info(set_name)
#    pass
#
#
#@pytest.mark.parametrize("set_name", [
#    ('train1'),
#    ('val'),
#])
#def test__print_info_fail(set_name, loader):
#    with pytest.raises(Exception):
#        loader._print_info(set_name)
#