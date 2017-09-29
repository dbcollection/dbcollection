"""
Test dbcollection/manager.py.
"""


import pytest
import dbcollection.manager as dbc


testdata = [
    ('mnist', 'classification', None, True, True),
]

# download mnist before using it
loader = dbc.load(name=testdata[0][0], is_test=True)

@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose",
                         testdata)
def test_download(name, task, data_dir, extract_data, verbose):
    dbc.download(name=name,
                 data_dir=data_dir,
                 extract_data=extract_data,
                 verbose=verbose,
                 is_test=True)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose",
                         testdata)
def test_process(name, task, data_dir, extract_data, verbose):
    dbc.process(name=name,
                task=task,
                verbose=verbose)
    pass


@pytest.mark.parametrize("name, task, data_dir, extract_data, verbose",
                         testdata)
def test_load(name, task, data_dir, extract_data, verbose):
    db = dbc.load(name=name,
                  task=task,
                  data_dir=data_dir,
                  verbose=verbose)
    assert(db.name == name)


def test_add():
    dbc.add(name='new_db',
            task='new_task',
            data_dir='new/path/db',
            file_path='newdb.h5',
            keywords = ['new_category'],
            is_test=True)
    # check if it correctly handles adding the same info
    dbc.add(name='new_db',
            task='new_task',
            data_dir='new/path/db',
            file_path='newdb.h5',
            keywords=['new_category'],
            is_test=True)
    pass


def test_remove():
    dbc.add(name='new_db',
            task='new_task',
            data_dir='new/path/db',
            file_path='newdb.h5',
            keywords = ['new_category'],
            is_test=True)
    dbc.remove(name='new_db',
               task='new_task',
               delete_data=True,
               is_test=True)
    pass


def test_config_cache():
    dbc.config_cache(reset_cache=True, is_test=True)
    pass


def test_query():
    query_info = dbc.query('info', is_test=True)
    assert(any(query_info))


def test_query_return_empty():
    query_info = dbc.query('undefined_dataset', is_test=True)
    assert(not any(query_info))


def test_info():
    dbc.info(is_test=True)
    pass


def test_info_list_datasets():
    dbc.info(name='all', is_test=True)
    pass
