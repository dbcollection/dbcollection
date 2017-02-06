#!/usr/bin/env python3

"""
md5hash.py unit testing.
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
from md5hash import *


#-----------------------
# Unit Test definitions
#-----------------------

class MD5HashTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__open_read_file', return_value)
    @patch('__main__.hashlib')
    def test_get_hash_value__success(self, mock_hash, mock_file):
        """
        Test retrieving a checksum from a file.
        """
        # sample data
        sample_file_name = 'test.md5'

        # mock function return values
        hashlib.md5.return_value = True
        hashlib.hexdigest.return_value = True

        # get hash value from a dummy file
        res = get_hash_value(sample_file_name)

        # check if the result is True
        self.assertTrue(res, 'Should have given True')


    def test_get_hash_value__fail(self):
        """
        Test retrieving a checksum from a file.
        """
        self.fail()


    def test_check_file_integrity_md5(self):
        """
        Test checking if the md5 hashes match
        """
        self.fail()


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
