"""
Test dbcollection main API methods
"""


import pytest

from dbcollection.core.api.download import download
from dbcollection.core.api.process import process
from dbcollection.core.api.load import load
from dbcollection.core.api.add import add
from dbcollection.core.api.remove import remove
from dbcollection.core.api.config_cache import config_cache
from dbcollection.core.api.query import query
from dbcollection.core.api.info import info_cache, info_datasets
from dbcollection.core.api.list_datasets import fetch_list_datasets


testdata = [
    ('mnist', 'classification', None, True, True, True),
]

def test_fetch_list_datasets():
    db_list = fetch_list_datasets()
    assert 'mnist' in db_list

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_download(name, task, data_dir, extract_data, verbose, is_test):
    config_cache(reset_cache=True, is_test=True)
    download(name=name,
             data_dir=data_dir,
             extract_data=extract_data,
             verbose=verbose,
             is_test=is_test)

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_process(name, task, data_dir, extract_data, verbose, is_test):
    config_cache(reset_cache=True, is_test=True)
    download(name=name,
             data_dir=data_dir,
             extract_data=extract_data,
             verbose=verbose,
             is_test=is_test)
    process(name=name,
            task=task,
            verbose=verbose,
            is_test=is_test)

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_load(name, task, data_dir, extract_data, verbose, is_test):
    config_cache(reset_cache=True, is_test=True)
    db = load(name=name,
              task=task,
              data_dir=data_dir,
              verbose=verbose,
              is_test=is_test)
    assert(db.db_name == name)

def test_add():
    config_cache(reset_cache=True, is_test=True)
    add(name='new_db',
        task='new_task',
        data_dir='new/path/db',
        file_path='newdb.h5',
        keywords=['new_category'],
        is_test=True)
    add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)

def test_remove():
    add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    try:
        remove(name='new_db',
               task='new_task',
               delete_data=True,
               is_test=True)
    except Exception:
        pass
    config_cache(reset_cache=True, is_test=True)

def test_config_cache():
    config_cache(reset_cache=True, is_test=True)

def test_query():
    query_info = query('info', True)
    assert(any(query_info))

def test_query_return_empty():
    query_info = query('undefined_dataset', True)
    assert(not any(query_info))

def test_info_cache():
    info_cache(is_test=True)

def test_info_datasets():
    info_datasets(is_test=True)

