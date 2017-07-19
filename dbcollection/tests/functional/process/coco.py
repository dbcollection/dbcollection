#!/usr/bin/env python

"""
Test processing coco.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'coco'
task = 'detection'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('process')