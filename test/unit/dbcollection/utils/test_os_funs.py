#!/usr/bin/env python3

"""
os_funs.py unit testing.
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
from os_funs import *


#-----------------------
# Unit Test definitions
#-----------------------

class OSFunsTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('os.remove')
    def test_remove_file__succeed(self, mock_remove):
        """
        Test removing a file from disk.
        """
        # sample data
        sample_fname = 'test'

        # remove a dummy file
        delete_file(sample_fname)

        # check if the mocked function was correctly called
        self.assertTrue(mock_remove.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_remove.assert_called_with(sample_fname)


    @patch('os.remove', side_effect=OSError)
    def test_remove_file__fail_raise_error(self, mock_remove):
        """
        Test removing a file from disk.
        """
        # sample data
        sample_fname = 'test'

        # remove a dummy file
        with self.assertRaises(OSError):
            delete_file(sample_fname)

        # check if the mocked function was correctly called
        self.assertTrue(mock_remove.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_remove.assert_called_with(sample_fname)


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
