#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
download.py unit testing.
"""


import unittest
import os, sys, inspect
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..','..'))
sys.path.append(lib_path)
import datasets


#-----------------------
# Unit Test definitions
#-----------------------

class DownloadTest(unittest.TestCase):
    """
    Test class.
    """

    def test_download_file(self):
        """
        Test downloading a file.
        """
        self.assertEqual(self.widget.size(), 1,
             'incorrect default size')

    def test_two(self):
        """
        Test two.
        """
        self.assertEqual(self.widget.size(), 2,
             'incorrect default size')


#----------------
# Run Test Suite
#----------------

def main(level=2):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
