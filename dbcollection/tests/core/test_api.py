"""
Test dbcollection main API methods
"""


import pytest
from dbcollection.core.api import (download,
                                   process,
                                   load,
                                   add,
                                   remove,
                                   config_cache,
                                   query,
                                   info_cache,
                                   info_datasets,
                                   fetch_list_datasets)


testdata = [
    ('mnist', 'classification', None, True, True, True),
]

def test_fetch_list_datasets():
    db_list = fetch_list_datasets()
    assert 'mnist' in db_list

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_download(name, task, data_dir, extract_data, verbose, is_test):
    download(name=name,
             data_dir=data_dir,
             extract_data=extract_data,
             verbose=verbose,
             is_test=is_test)
    config_cache(reset_cache=True, is_test=True)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_process(name, task, data_dir, extract_data, verbose, is_test):
    download(name=name,
             data_dir=data_dir,
             extract_data=extract_data,
             verbose=verbose,
             is_test=is_test)
    process(name=name,
            task=task,
            verbose=verbose,
            is_test=is_test)
    config_cache(reset_cache=True, is_test=True)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_load(name, task, data_dir, extract_data, verbose, is_test):
    db = load(name=name,
              task=task,
              data_dir=data_dir,
              verbose=verbose,
              is_test=is_test)
    config_cache(reset_cache=True, is_test=True)
    assert(db.db_name == name)


def test_add():
    add(name='new_db',
        task='new_task',
        data_dir='new/path/db',
        file_path='newdb.h5',
        keywords=['new_category'],
        is_test=True)
    add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    config_cache(reset_cache=True, is_test=True)
    pass


def test_remove():
    add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    remove(name='new_db',
           task='new_task',
           delete_data=True,
           is_test=True)
    config_cache(reset_cache=True, is_test=True)
    pass


def test_config_cache():
    config_cache(reset_cache=True, is_test=True)
    pass


def test_query():
    query_info = query('info', True)
    assert(any(query_info))


def test_query_return_empty():
    query_info = query('undefined_dataset', True)
    assert(not any(query_info))


def test_info_cache():
    info_cache(is_test=True)
    pass

def test_info_datasets():
    info_datasets(is_test=True)
    pass
