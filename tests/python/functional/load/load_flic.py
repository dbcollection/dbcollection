#!/usr/bin/env python3

"""
Test loading flic.
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
flic = dbc.load(name='flic', task='keypoints', data_dir=data_dir, verbose=True, is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# print data from the loader
print('\n######### info #########')
print('Dataset: ' + flic.name)
print('Task: ' + flic.task)
print('Data path: ' + flic.data_dir)
print('Metadata cache path: ' + flic.cache_path)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)