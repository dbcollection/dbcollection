"""
Test cifar10 hdf5 file contents.
"""


import pytest
import dbcollection.manager as dbc
from dbcollection.utils.cache import CacheManager
from dbcollection.utils.string_ascii import convert_ascii_to_str as ascii2str

name = 'cifar10'
cache_manager = CacheManager(is_test=True)


@pytest.mark.skiptif(not cache_manager.exists_task(name, 'classification'),
                     reason='Dataset is not available for testing: {}'.format(name))
def test_cifar10__task_classification():
    cifar10 = dbc.load(name='cifar10', task='classification')

    assert set(cifar10.sets) == set(['train', 'test'])

    # check train values
    assert ascii2str(cifar10.get('train', 'classes', 0)) == 'airplane'
    assert set(cifar10.object('train', 0).tolist()) == set([0, 6])
    assert set(cifar10.list('train')) == set(['classes', 'images', 'list_images_per_class', 'object_fields', 'object_ids'])

    # check test values
    assert ascii2str(cifar10.get('test', 'classes', 0)) == 'airplane'
    assert set(cifar10.object('test', 0).tolist()) == set([0, 3])
    assert set(cifar10.list('test')) == set(['classes', 'images', 'list_images_per_class', 'object_fields', 'object_ids'])