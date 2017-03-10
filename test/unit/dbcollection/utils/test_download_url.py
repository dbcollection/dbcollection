#!/usr/bin/env python3

"""
download_url.py unit testing.
"""


import os
import sys
import numpy as np

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection', 'utils'))
sys.path.append(lib_path)
from download_url import *


#-----------------------
# Unit Test definitions
#-----------------------

class URLDownloadTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__.os.path.exists')
    @patch('__main__.download_single_file_progressbar')
    @patch('__main__.download_single_file_nodisplay')
    def test_download_file__succeed(self, mock_os, mock_progress, mock_notext):
        """
        Test download a single file .
        """

        # test downloading a file
        res_progress = download_file('any url','any dir','any fname', True)

        # Check if res is True
        self.assertTrue(res_progress, 'Download single file should return True')

        # test downloading a file
        res_notext = download_file('any url','any dir','any fname', False)

        # Check if res is True
        self.assertTrue(res_notext, 'Download single file should return True')


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
