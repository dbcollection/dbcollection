#!/usr/bin/env python

"""
Test downloading cifar10.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'cifar10'
task = 'classification'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('download')