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
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..','datasets'))
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
from unittest.mock import patch


#-----------------------
# Unit Test definitions
#-----------------------

class UtilsTest(unittest.TestCase):
    """ Test class. """

    @patch('utils.os')
    def test_create_dir(self, mock_os):
        """
        Test dir creation.
        """

        # test removing a file
        utils.create_dir('any path')

        # check if the path was the same
        mock_os.makedirs.assert_called_with("any path")


    @patch('utils.os.path.exists')
    @patch('utils.download_single_file_progressbar')
    @patch('utils.download_single_file_nodisplay')
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


    @patch('utils.raise_exception')
    def test_get_extractor_method(self, mock_raise):
        """
        Test selecting the file extractor function.
        """

        ext = 'tar'
        # get method
        method = utils.get_extractor_method(ext)
        # assert if functions are the same
        self.assertEqual(utils.extract_file_tar, method, 'Functions should be equal')

        ext = 'zip'
        # get method
        method = utils.get_extractor_method(ext)
        # assert if functions are the same
        self.assertEqual(utils.extract_file_zip, method, 'Functions should be equal')

        # assert if functions are different
        self.assertNotEqual(utils.extract_file_tar, method, 'Functions should be equal')

        ext = 'none'
        # check if it gives an exception (note: it should)
        check = utils.get_extractor_method(ext)


    def test_url_get_filename(self):
        """
        Test extracting the filename out of the url and
        merge it with the dir path.
        """
        # sample url
        url_sample = 'http://some/url/filename.zip'

        # sample dir path
        dir_path = 'some/path/'

        # valid path + fname
        valid = dir_path + 'filename.zip'

        # get path+filename
        res = utils.url_get_filename(url_sample, dir_path)

        #check if res and valid are the same
        self.assertEqual(res, valid, 'Filenames should be the same')



   # @mock.patch('utils.get_file_extension')
    @patch('utils.get_extractor_method')
    def test_extract_file(self, mock_extractor):
        """
        Test extract a file to disk.
        """

        # mock function
        mock_extractor.get_extractor_method.side_effect = lambda x,y: True

        # extract file to disk
        res_zip = utils.extract_file('any path', 'any fname')

        self.assertIsNone(res_zip, 'Should give none')


    @patch('utils.os')
    def test_remove_file(self, mock_os):
        """
        Test file removal.
        """

        # test removing a file
        utils.remove_file('any path')

        # check if the path was the same
        mock_os.remove.assert_called_with("any path")


    @patch('utils.url_get_filename')
    @patch('utils.download_file')
    @patch('utils.extract_file')
    @patch('utils.remove_file')
    def test_download_extract_all(self, mock_remove, mock_extract, mock_download, mock_url):
        """
        Test download+extract all files
        """
        # url samples
        url_samples = ['url1/fname.tar', 'url2/fname.tar', 'url3/fname.zip']

        # process download+extract all files
        utils.download_extract_all(url_samples, 'any dir', True, True)

        # check if the mocked functions were called properly
        self.assertFalse(mock_url.url_get_filename.called, "Failed to mock utils.url_get_filename().")
        self.assertFalse(mock_download.download_file.called, "Failed to mock utils.download_file().")
        self.assertFalse(mock_extract.extract_file.called, "Failed to mock utils.extract_file().")
        self.assertFalse(mock_remove.remove_file.called, "Failed to mock utils.remove_file().")


#----------------
# Run Test Suite
#----------------

def main(level=2):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main(1)
