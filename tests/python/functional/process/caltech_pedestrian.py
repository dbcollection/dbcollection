#!/usr/bin/env python3

"""
Test loading Caltech Pedestrian.
"""

import os
from dbcollection.utils.test import TestBaseDB


# setup
name = 'caltech_pedestrian'
task = 'detection'
data_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'download_data')
verbose = True

# Run tester
tester = TestBaseDB(name, task, data_dir, verbose)
tester.run('process')