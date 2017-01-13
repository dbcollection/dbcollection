#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
utils.py unit testing.
"""

# import utils.py
import os, sys, inspect
dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','datasets'))
sys.path.append(lib_path)
import utils

from clint.textui import progress
import urllib
import requests
import tarfile
import zipfile
import os

import unittest
from unittest import mock


#-----------------------
# Unit Test definitions
#-----------------------

class UtilsTest(unittest.TestCase):
    """
    Test class.
    """


    @mock.patch('utils.os')
    def test_create_dir(self, mock_os):
        """
        Test dir creation.
        """

        # test removing a file
        utils.create_dir('any path')

        # check if the path was the same
        mock_os.makedirs.assert_called_with("any path")


    @mock.patch('utils.os.path.exists')
    @mock.patch('utils.download_single_file_progressbar')
    @mock.patch('utils.download_single_file_nodisplay')
    def test_download_file(self, mock_os, mock_progress, mock_notext):
        """
        Test download a single file .
        """

        # test downloading a file
        res_progress = utils.download_file('any url','any dir','any fname', True)

        # Check if res is True
        self.assertTrue(res_progress, 'Download single file should return True')

        # test downloading a file
        res_notext = utils.download_file('any url','any dir','any fname', False)

        # Check if res is True
        self.assertTrue(res_notext, 'Download single file should return True')


    def test_get_file_extension(self):
        """
        Test retrieve file extension.
        """
        fname = 'file.ext'
        target = 'ext'

        # test removing a file
        res = utils.get_file_extension(fname)

        # check if the extension matches
        self.assertEqual(res, target, 'extension mismatch {}!={}'.format(res, target))


    @mock.patch('utils.get_file_extension')
    @mock.patch('utils.extract_file_zip')
    @mock.patch('utils.extract_file_tar')
    @mock.patch('utils.raise_exception')
    def test_extract_file(self, mock_raise_exception, mock_ext_tar, mock_ext_zip, mock_ext_get):
        """
        Test extract a file to disk.
        """

        # mock return value type
        mock_ext_get.return_value = 'zip'
        # extract file to disk
        res_zip = utils.extract_file('any path', 'any fname')
        # Check if res is True
        self.assertTrue(res_zip,'Should have returned True')

        # mock return value type
        mock_ext_get.return_value = 'tar'
        # extract file to disk
        res_tar = utils.extract_file('any path', 'any fname')
        # Check if res is True
        self.assertTrue(res_tar,'Should have returned True')

        # mock return value type
        mock_ext_get.return_value = 'gz'
        # extract file to disk
        res_gz = utils.extract_file('any path', 'any fname')
        # Check if res is True
        self.assertTrue(res_gz,'Should have returned True')

        # mock return value type
        mock_ext_get.return_value = 'coiso'
        # extract file to disk
        res_gz = utils.extract_file('any path', 'any fname')
        # Check if res is True
        self.assertTrue(res_gz,'Should have returned True')


    @mock.patch('utils.os')
    def test_remove_file(self, mock_os):
        """
        Test file removal.
        """

        # test removing a file
        utils.remove_file('any path')

        # check if the path was the same
        mock_os.remove.assert_called_with("any path")


#----------------
# Run Test Suite
#----------------

def main(level=2):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
