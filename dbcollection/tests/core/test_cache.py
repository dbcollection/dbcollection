"""
Test dbcollection/utils/cache.py.
"""


import os
import pytest
from dbcollection.core.cache import CacheManager


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


@pytest.fixture
def cache_manager():
    cache = CacheManager(is_test=True)
    cache.reset_cache(force_reset=True)  # clear old contents
    cache.write_data_cache(data)
    cache.reload_cache()
    return cache


@pytest.mark.parametrize("name, new_info, is_append", [
    ('new_dataset1', {}, True),
    ('new_dataset2', {}, False),
    ('test_dataset1', {}, False),
])
def test_add_data(name, new_info, is_append, cache_manager):
    cache_manager.add_data(name, new_info, is_append)
    assert(name in cache_manager.data['dataset'])
    assert(cache_manager.data['dataset'][name] == new_info)


@pytest.mark.parametrize("name, delete_cache", [
    ('test_dataset1', False),
    ('test_dataset2', False),
    ('test_dataset2', True),
])
def test_delete_dataset(name, delete_cache, cache_manager):
    cache_manager.delete_dataset(name, delete_cache)
    assert(not name in cache_manager.data['dataset'])


@pytest.mark.parametrize("name, delete_cache", [
    ('test_dataset_non_exists', False),
])
def test_delete_dataset_raise(name, delete_cache, cache_manager):
    with pytest.raises(Exception):
        cache_manager.delete_dataset(name, delete_cache)

@pytest.mark.parametrize("name, task", [
    ('test_dataset2', 'extra'),
])
def test_delete_task(name, task, cache_manager):
    cache_manager.delete_task(name, task)


@pytest.mark.parametrize("name, output", [
    ('test_dataset1', True),
    ('test_dataset2', True),
    ('test_dataset_non_exists', False),
    ('', False),
])
def test_exists_dataset(name, output, cache_manager):
    assert(output == cache_manager.exists_dataset(name))


@pytest.mark.parametrize("name, task, output", [
    ('test_dataset1', 'default', True),
    ('test_dataset1', 'classification', True),
    ('test_dataset1', 'classific', False),
    ('test_dataset2', 'extra', True),
    ('test_dataset_non_exists', 'default', False),
    ('', 'default', False),
])
def test_exists_task(name, task, output, cache_manager):
    assert(output == cache_manager.exists_task(name, task))


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
def test_get_dataset_storage_paths(name, output, cache_manager):
    assert(output == cache_manager.get_dataset_storage_paths(name))


@pytest.mark.parametrize("name, task", [
    ('test_dataset1', "default"),
    ('test_dataset1', "classification"),
    ('test_dataset1', "extra"),
    ('test_dataset2', "default"),
    ('test_dataset2', "classification"),
    ('test_dataset2', "extra"),
])
def test_get_task_cache_path__succeed(name, task, cache_manager):
    task_path = cache_manager.data["dataset"][name]["tasks"][task]
    assert(task_path == cache_manager.get_task_cache_path(name, task))


@pytest.mark.parametrize("name, task", [
    ('test_dataset1', ""),
    ('test_dataset1', "classific"),
    ('test_dataset1', "extra_"),
    ('test_dataset_non_exists', "default"),
    ('test_dataset_non_exists', "classification"),
    ('test_dataset_non_exists', "extra"),
])
def test_get_task_cache_path__fail(name, task, cache_manager):
    with pytest.raises(Exception):
        cache_manager.get_task_cache_path(name, task)

@pytest.mark.parametrize("name, keywords", [
    ('test_dataset1', "new_kw"),
    ('test_dataset1', ["new_kw1", "new_kw2"]),
])
def test_add_keywords(name, keywords, cache_manager):
    cache_manager.add_keywords(name, keywords)
    if not isinstance(keywords, list):
        keywords = [keywords]
    l = [kw for kw in keywords if kw in cache_manager.data["dataset"][name]["keywords"]]
    assert(any(l))
    l = [kw for kw in keywords if kw in cache_manager.data["category"]]
    assert(any(l))

@pytest.mark.parametrize("name, keywords", [
    ('test_dataset1', ""),
    ('test_dataset1', ["", ""]),
])
def test_add_keywords_empty(name, keywords, cache_manager):
    kw = list(cache_manager.data["dataset"][name]["keywords"])
    cache_manager.add_keywords(name, keywords)
    assert(set(kw) == set(cache_manager.data["dataset"][name]["keywords"]))
    l = [kw for kw in keywords if kw in cache_manager.data["category"]]
    assert(not any(l))


@pytest.mark.parametrize("name, data_dir, cache_tasks, cache_keywords, is_append", [
    ('test_dataset1', os.path.join('new', 'data', 'dir'), {"new_task": "new_file.h5"},
     ["new_kw1", "new_kw2"], False),
    ('test_dataset2', os.path.join('new', 'data', 'dir'), {"new_task": "new_file.h5"},
     ["new_kw1", "new_kw2"], True),
])
def test_update(name, data_dir, cache_tasks, cache_keywords, is_append, cache_manager):
    cache_manager.update(name, data_dir, cache_tasks, cache_keywords, is_append)
    assert(name in cache_manager.data["dataset"])
    if is_append:
        assert(data_dir != cache_manager.data["dataset"][name]["data_dir"])
    else:
        assert(data_dir == cache_manager.data["dataset"][name]["data_dir"])
    l = [task for task in cache_tasks if task in cache_manager.data["dataset"][name]["tasks"]]
    assert(any(l))
    l = [kw for kw in cache_keywords if kw in cache_manager.data["dataset"][name]["keywords"]]
    assert(any(l))


@pytest.mark.parametrize("field, value", [
    ('test_dataset1', "string"),
    ('test_dataset1', ['dummy_data']),
    ('test_dataset2', 1),
    ('test_dataset2', {'new': 'stuff'}),
])
def test_modify_field_dataset(field, value, cache_manager):
    cache_manager.modify_field(field, value)
    assert(value == cache_manager.data["dataset"][field])


@pytest.mark.parametrize("field, value", [
    ('image_processing', "new_val"),
    ('image_processing', ["new_val1", "new_val2"]),
    ('image_processing', ["new_val1", "new_val2"]),
    ('classification', 1),
])
def test_modify_field_dataset_keywords(field, value, cache_manager):
    cache_manager.modify_field(field, value)
    assert(value == cache_manager.data["category"][field])


@pytest.mark.parametrize("field, value", [
    ('default_cache_dir', "new_val"),
    ('default_cache_dir', ["new_val1", "new_val2"]),
])
def test_modify_field_info(field, value, cache_manager):
    cache_manager.modify_field(field, value)
    assert(value == cache_manager.data["info"][field])


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
def test_modify_field_raise(field, value, cache_manager):
    with pytest.raises(Exception):
        cache_manager.modify_field(field, value)
