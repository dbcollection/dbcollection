"""
Test dbcollection/manager.py.
"""


import pytest
import dbcollection.manager as dbc


testdata = [
    ('mnist', 'classification', None, True, True, True),
]

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_download(name, task, data_dir, extract_data, verbose, is_test):
    dbc.download(name=name,
                 data_dir=data_dir,
                 extract_data=extract_data,
                 verbose=verbose,
                 is_test=is_test)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_process(name, task, data_dir, extract_data, verbose, is_test):
    dbc.process(name, task, verbose, is_test)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose, is_test",
                         testdata)
def test_load(name, task, data_dir, extract_data, verbose, is_test):
    db = dbc.load(name, task, data_dir, verbose, is_test)
    assert(db.name == name)


def test_add():
    dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    pass


def test_remove():
    dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'], True)
    dbc.remove('new_db', 'new_task', True, True)
    pass


def test_config_cache():
    dbc.config_cache(reset_cache=True, is_test=True)
    pass


def test_query():
    query_info = dbc.query('info', True)
    assert(any(query_info))


def test_query_return_empty():
    query_info = dbc.query('undefined_dataset', True)
    assert(not any(query_info))


def test_info():
    dbc.info(is_test=True)
    pass


def test_info_list_datasets():
    dbc.info(name='all', is_test=True)
    pass
