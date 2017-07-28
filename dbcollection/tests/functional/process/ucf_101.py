#!/usr/bin/env python

"""
Test loading ucf101.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'ucf_101'
task = 'recognition'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('process')