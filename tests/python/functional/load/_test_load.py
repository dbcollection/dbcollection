#!/usr/bin/env python3

"""
Test loading a dataset using the Python API.
"""


from __future__ import print_function
import os
import argparse
import dbcollection.manager as dbc

# storage dir
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')

# Instantiate the parser
parser = argparse.ArgumentParser(description='--- Load script options -----')
parser.add_argument('--name', action='store', default='cifar10',
                    help='Dataset name.')
parser.add_argument('--task', action='store', default='default',
                    help='Task name.')
parser.add_argument('--data_dir', action='store', default=data_dir,
                    help='Directory where the dataset\'s files are stored.')
args = parser.parse_args()

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('\n==> dbcollection: load()')
loader = dbc.load(name=args.name, task=args.task, data_dir=args.data_dir, verbose=True, is_test=True)

# print data from the loader
print('\n==> dbcollection: info()')
dbc.info(is_test=True)

# print data from the loader
print('\n######### info #########')
print('Dataset: ' + loader.name)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)

# delete all cache data + dir
print('\n==> dbcollection: config_cache()')
dbc.config_cache(delete_cache=True, is_test=True)