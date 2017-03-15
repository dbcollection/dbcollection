#!/usr/bin/env python3

"""
file_extraction.py unit testing.
"""


import os
import sys

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

#dir_path = os.path.dirname(os.path.realpath(__file__))
#lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection', 'utils'))
#sys.path.append(lib_path)
#from file_extraction import *

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
#sys.path.append(lib_path)
sys.path.insert(0, lib_path)
from dbcollection.utils.file_extraction import *

#-----------------------
# Unit Test definitions
#-----------------------

class FileExtractionTest(unittest.TestCase):
    """
    Test class.
    """

    def test_get_file_extension(self):
        """
        Test retrieve file extension.
        """
        fname = 'file.ext'
        target = 'ext'

        # test removing a file
        res = get_file_extension(fname)

        # check if the extension matches
        self.assertEqual(res, target, 'extension mismatch {}!={}'.format(res, target))


    def test_get_extractor_method__extract_tar_ext(self):
        """
        Test selecting the file extractor function for a tar file.
        """
        # sample data
        sample_ext = 'tar'

        # get method
        method = get_extractor_method(sample_ext)

        # assert if functions are the same
        self.assertEqual(extract_file_tar, method, 'Functions should be the same')


    def test_get_extractor_method__extract_zip_ext(self):
        """
        Test selecting the file extractor function for a zip file.
        """
        # sample data
        sample_ext = 'zip'

        # get method
        method = get_extractor_method(sample_ext)

        # assert if functions are the same
        self.assertEqual(extract_file_zip, method, 'Functions should be the same')


    def test_get_extractor_method__invalid_extract_ext(self):
        """
        Test selecting the file extractor function for an invalid extension.
        """
        # sample data
        sample_ext = 'none'

        # get method
        with self.assertRaises(KeyError):
            method = get_extractor_method(sample_ext)


    def test_extract_file(self):
        """
        Test extracting a file to disk.
        """
        # sample data
        sample_fname = 'file.tar'
        sample_dir_path = 'dir/path/'
        sample_verbose = False

        # extract file (should raise an exception)
        with self.assertRaises(FileNotFoundError):
            extract_file(sample_fname, sample_dir_path, sample_verbose)


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
