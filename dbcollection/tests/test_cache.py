"""
Test dbcollection/utils/cache.py.
"""


import os
import pytest
from dbcollection.cache import CacheManager


data = {
    "info": {
        "default_cache_dir": os.path.join('some','path','dir')
    },
    "dataset": {
        "test_dataset1": {
            "cache_dir": os.path.join('some','path','dir','test_dataset1'),
            "data_dir": os.path.join('some','path','dir','test_dataset1', 'data'),
            "tasks": {
                "default": "file1.h5",
                "classification": "file2.h5",
                "extra": "file3.h5"
            },
            "keywords": ['image_processing', 'classification']
        },
        "test_dataset2": {
            "cache_dir": os.path.join('some','path','dir','test_dataset2'),
            "data_dir": os.path.join('some','path','dir','test_dataset2', 'data'),
            "tasks": {
                "default": "file4.h5",
                "classification": "file5.h5",
                "extra": "file6.h5"
            },
            "keywords": ['image_processing', 'classification']
        },
    },
    "category": {
        'image_processing': ['test_dataset1, test_dataset2'],
        'classification': ['test_dataset1, test_dataset2']
    }
}

cache = CacheManager(is_test=True)

def reset_cache_data():
    data = {
        "info": {
            "default_cache_dir": os.path.join('some','path','dir')
        },
        "dataset": {
            "test_dataset1": {
                "cache_dir": os.path.join('some','path','dir','test_dataset1'),
                "data_dir": os.path.join('some','path','dir','test_dataset1', 'data'),
                "tasks": {
                    "default": "file1.h5",
                    "classification": "file2.h5",
                    "extra": "file3.h5"
                },
                "keywords": ['image_processing', 'classification']
            },
            "test_dataset2": {
                "cache_dir": os.path.join('some','path','dir','test_dataset2'),
                "data_dir": os.path.join('some','path','dir','test_dataset2', 'data'),
                "tasks": {
                    "default": "file4.h5",
                    "classification": "file5.h5",
                    "extra": "file6.h5"
                },
                "keywords": ['image_processing', 'classification']
            },
        },
        "category": {
            'image_processing': ['test_dataset1, test_dataset2'],
            'classification': ['test_dataset1, test_dataset2']
        }
    }
    cache.data = data
    cache.default_cache_dir = data["info"]["default_cache_dir"]
    cache.write_data_cache(data)


@pytest.mark.parametrize("name, new_info, is_append", [
    ('new_dataset1', {}, True),
    ('new_dataset2', {}, False),
    ('test_dataset1', {}, False),
])
def test_add_data(name, new_info, is_append):
    reset_cache_data()
    cache.add_data(name, new_info, is_append)
    assert(name in cache.data['dataset'])
    assert(cache.data['dataset'][name] == new_info)


@pytest.mark.parametrize("name, delete_cache", [
    ('test_dataset1', False),
    ('test_dataset2', False),
    ('test_dataset2', True),
])
def test_delete_dataset(name, delete_cache):
    reset_cache_data()
    cache.delete_dataset(name, delete_cache)
    assert(not name in cache.data['dataset'])


@pytest.mark.parametrize("name, delete_cache", [
    ('test_dataset_non_exists', False),
])
def test_delete_dataset_raise(name, delete_cache):
    reset_cache_data()
    with pytest.raises(Exception):
        cache.delete_dataset(name, delete_cache)


@pytest.mark.parametrize("name, output", [
    ('test_dataset1', True),
    ('test_dataset2', True),
    ('test_dataset_non_exists', False),
    ('', False),
])
def test_exists_dataset(name, output):
    reset_cache_data()
    assert(output == cache.exists_dataset(name))


@pytest.mark.parametrize("name, task, output", [
    ('test_dataset1', 'default', True),
    ('test_dataset1', 'classification', True),
    ('test_dataset1', 'classific', False),
    ('test_dataset2', 'extra', True),
    ('test_dataset_non_exists', 'default', False),
    ('', 'default', False),
])
def test_exists_task(name, task, output):
    reset_cache_data()
    assert(output == cache.exists_task(name, task))


@pytest.mark.parametrize("name, output", [
    ('test_dataset1', {
        "data_dir": data["dataset"]["test_dataset1"]["data_dir"],
        "cache_dir": data["dataset"]["test_dataset1"]["cache_dir"]
    }),
    ('test_dataset2', {
        "data_dir": data["dataset"]["test_dataset2"]["data_dir"],
        "cache_dir": data["dataset"]["test_dataset2"]["cache_dir"]
    }),
])
def test_get_dataset_storage_paths(name, output):
    reset_cache_data()
    assert(output == cache.get_dataset_storage_paths(name))


@pytest.mark.parametrize("name, task", [
    ('test_dataset1', "default"),
    ('test_dataset1', "classification"),
    ('test_dataset1', "extra"),
    ('test_dataset2', "default"),
    ('test_dataset2', "classification"),
    ('test_dataset2', "extra"),
])
def test_get_cache_path__succeed(name, task):
    reset_cache_data()
    task_path = cache.data["dataset"][name]["tasks"][task]
    assert(task_path == cache.get_cache_path(name, task))


@pytest.mark.parametrize("name, task", [
    ('test_dataset1', ""),
    ('test_dataset1', "classific"),
    ('test_dataset1', "extra_"),
    ('test_dataset_non_exists', "default"),
    ('test_dataset_non_exists', "classification"),
    ('test_dataset_non_exists', "extra"),
])
def test_get_cache_path__fail(name, task):
    reset_cache_data()
    with pytest.raises(Exception):
        cache.get_cache_path(name, task)

@pytest.mark.parametrize("name, keywords", [
    ('test_dataset1', "new_kw"),
    ('test_dataset1', ["new_kw1", "new_kw2"]),
])
def test_add_keywords(name, keywords):
    reset_cache_data()
    cache.add_keywords(name, keywords)
    if not isinstance(keywords, list):
        keywords = [keywords]
    l = [kw for kw in keywords if kw in cache.data["dataset"][name]["keywords"]]
    assert(any(l))
    l = [kw for kw in keywords if kw in cache.data["category"]]
    assert(any(l))

@pytest.mark.parametrize("name, keywords", [
    ('test_dataset1', ""),
    ('test_dataset1', ["", ""]),
])
def test_add_keywords_empty(name, keywords):
    reset_cache_data()
    kw = list(cache.data["dataset"][name]["keywords"])
    cache.add_keywords(name, keywords)
    assert(set(kw) == set(cache.data["dataset"][name]["keywords"]))
    l = [kw for kw in keywords if kw in cache.data["category"]]
    assert(not any(l))


@pytest.mark.parametrize("name, data_dir, cache_tasks, cache_keywords, is_append", [
    ('test_dataset1', os.path.join('new', 'data', 'dir'), {"new_task": "new_file.h5"},
     ["new_kw1", "new_kw2"], False),
    ('test_dataset2', os.path.join('new', 'data', 'dir'), {"new_task": "new_file.h5"},
     ["new_kw1", "new_kw2"], True),
])
def test_update(name, data_dir, cache_tasks, cache_keywords, is_append):
    reset_cache_data()
    cache.update(name, data_dir, cache_tasks, cache_keywords, is_append)
    assert(name in cache.data["dataset"])
    if is_append:
        assert(data_dir != cache.data["dataset"][name]["data_dir"])
    else:
        assert(data_dir == cache.data["dataset"][name]["data_dir"])
    l = [task for task in cache_tasks if task in cache.data["dataset"][name]["tasks"]]
    assert(any(l))
    l = [kw for kw in cache_keywords if kw in cache.data["dataset"][name]["keywords"]]
    assert(any(l))


@pytest.mark.parametrize("field, value", [
    ('test_dataset1', "string"),
    ('test_dataset1', ['dummy_data']),
    ('test_dataset2', 1),
    ('test_dataset2', {'new': 'stuff'}),
])
def test_modify_field_dataset(field, value):
    reset_cache_data()
    cache.modify_field(field, value)
    assert(value == cache.data["dataset"][field])


@pytest.mark.parametrize("field, value", [
    ('image_processing', "new_val"),
    ('image_processing', ["new_val1", "new_val2"]),
    ('image_processing', ["new_val1", "new_val2"]),
    ('classification', 1),
])
def test_modify_field_dataset_keywords(field, value):
    reset_cache_data()
    cache.modify_field(field, value)
    assert(value == cache.data["category"][field])


@pytest.mark.parametrize("field, value", [
    ('default_cache_dir', "new_val"),
    ('default_cache_dir', ["new_val1", "new_val2"]),
])
def test_modify_field_info(field, value):
    reset_cache_data()
    cache.modify_field(field, value)
    assert(value == cache.data["info"][field])


@pytest.mark.parametrize("field, value", [
    ('test_dataset1', {}),
    ('test_dataset1', []),
    ('test_dataset1', ""),
    ('test_dataset1_', ['dummy_data']),
    ('test_dataset2', {}),
    ({}, {}),
    (['test_dataset1'], ['new_value']),
    ('info2', "new_val"),
    ('default_cache_dir_', "new_val"),
])
def test_modify_field_raise(field, value):
    reset_cache_data()
    with pytest.raises(Exception):
        cache.modify_field(field, value)