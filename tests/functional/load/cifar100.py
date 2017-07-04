#!/usr/bin/env python3

"""
Test loading cifar100.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'cifar100'
task = 'classification'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('load')