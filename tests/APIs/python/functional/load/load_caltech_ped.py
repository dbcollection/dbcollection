#!/usr/bin/env python3

"""
Test loading caltech_pedestrian.
"""


from __future__ import print_function
import os
import dbcollection.manager as dbc

# storage dir
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')


# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('\n==> dbcollection: load()')
ped = dbc.load(name='caltech_pedestrian', task='detection', data_dir=data_dir, verbose=True, is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# print data from the loader
print('\n######### info #########')
print('Dataset: ' + ped.name)
print('Task: ' + ped.task)
print('Data path: ' + ped.data_dir)
print('Metadata cache path: ' + ped.cache_path)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)