#!/usr/bin/env python3

"""
Test loading flic.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'flic'
task = 'keypoints'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('load')