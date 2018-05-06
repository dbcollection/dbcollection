#!/usr/bin/env python

"""
Test downloading coco.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'coco'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data2')
verbose = True

# Run tester
tester = TestBaseDB(name, 'no_task', data_dir, verbose)
tester.run('download')