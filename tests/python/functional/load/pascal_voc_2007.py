#!/usr/bin/env python3

"""
Test loading Pascal VOC 2007.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'pascal_voc_2007'
task = 'detection'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('load')