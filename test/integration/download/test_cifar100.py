#!/usr/bin/env python3


"""
Test downloading the cifar100 dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbclt


# delete all cache data + dir
print('==> dbcollection.clear:')
dbclt.clear(is_test=True)

# download dataset
print('==> dbcollection.download:')
dbclt.download(name='cifar100', data_dir='/home/mf/tmp/download_data', verbose=True, is_test=True)

# print data from the loader
dbclt.info(is_test=True)

# delete all cache data + dir
print('==> dbcollection.clear:')
dbclt.clear(is_test=True)