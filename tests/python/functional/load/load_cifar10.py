#!/usr/bin/env python3

"""
Test loading cifar10.
"""


from __future__ import print_function
import os
import dbcollection.manager as dbc

# storage dir
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')


# delete any existing cache data + dir on disk
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('\n==> dbcollection: load()')
cifar10 = dbc.load(name='cifar10',
                   task='classification',
                   data_dir=data_dir,
                   verbose=True,
                   is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# print data from the loader
print('\n######### info #########')
print('Dataset: ' + cifar10.name)
print('Task: ' + cifar10.task)
print('Data path: ' + cifar10.data_dir)
print('Metadata cache path: ' + cifar10.cache_path)

# wipe the generated cache data + dir from the disk
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)