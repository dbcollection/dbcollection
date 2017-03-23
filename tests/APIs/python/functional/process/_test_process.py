#!/usr/bin/env python3

"""
Test processing a dataset using the Python API.
"""


from __future__ import print_function
import os
import argparse
import dbcollection.manager as dbc

# storage dir
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')

# Instantiate the parser
parser = argparse.ArgumentParser(description='--- Download script options -----')
parser.add_argument('--name', action='store', default='cifar10',
                    help='Dataset name.')
parser.add_argument('--data_dir', action='store', default=data_dir,
                    help='Directory where the dataset\'s files are stored.')
args = parser.parse_args()

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)

# download dataset
print('\n==> dbcollection: load()')
dbc.download(name=args.name, data_dir=args.data_dir, verbose=True, is_test=True)

# Process dataset
print('\n==> dbcollection: load()')
dbc.process(name=args.name, verbose=True, is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)