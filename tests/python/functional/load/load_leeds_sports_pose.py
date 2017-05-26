#!/usr/bin/env python3

"""
Test loading leeds_sports_pose.
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
lsp = dbc.load(name='leeds_sports_pose', task='keypoints_original', data_dir=data_dir, verbose=True, is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# print data from the loader
print('\n######### info #########')
print('Dataset: ' + lsp.name)
print('Task: ' + lsp.task)
print('Data path: ' + lsp.data_dir)
print('Metadata cache path: ' + lsp.cache_path)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)