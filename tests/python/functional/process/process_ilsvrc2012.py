#!/usr/bin/env python3

"""
Test processing imagenet ilsvrc2012.
"""


from __future__ import print_function
import os
import dbcollection.manager as dbc

# storage dir
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')


# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)

# download dataset
print('\n==> dbcollection: download()')
dbc.download(name='ilsvrc2012', data_dir=data_dir, verbose=True, is_test=True)

# Process dataset
print('\n==> dbcollection: process()')
dbc.process(name='ilsvrc2012', task='default', verbose=True, is_test=True)
dbc.process(name='ilsvrc2012', task='raw256', verbose=True, is_test=True)


# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)