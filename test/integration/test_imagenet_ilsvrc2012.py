#!/usr/bin/env python3


"""
Test downloading the ImageNet ILSVRC2012 dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbclt


# delete all cache data + dir
print('\n==> dbcollection.remove:')
dbclt.manage_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('\n==> dbcollection.download:')
dbclt.setup(name='ilsvrc2012', data_dir='/media/HDD2/Datasets/Imagenet', is_download=False, verbose=True, is_test=True)

# download dataset
print('\n==> dbcollection.download:')
loader = dbclt.load(name='ilsvrc2012', task='classification', verbose=True, is_test=True)

# print data from the loader
dbclt.info(is_test=True)

# print data from the loader
print('######### info #########')
print('Dataset: ' + loader.name)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)

# delete all cache data + dir
print('==> dbcollection.remove:')
dbclt.manage_cache(delete_cache=True, is_test=True)