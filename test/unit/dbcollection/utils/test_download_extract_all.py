#!/usr/bin/env python3

"""
__init__.py unit testing.
"""

import os
import sys
import numpy as np

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection'))
sys.path.append(lib_path)
import utils


#-----------------------
# Unit Test definitions
#-----------------------

class DownloadExtractTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__.utils.url_get_filename')
    @patch('__main__.utils.download_file')
    @patch('__main__.utils.extract_file')
    @patch('__main__.utils.remove_file')
    def test_download_extract_all__succeed(self, mock_remove, mock_extract, mock_download, mock_url):
        """
        Test download+extract all files
        """
        # url samples
        sample_urls = ['url1/fname.tar', 'url2/fname.tar', 'url3/fname.zip']
        sample_md5sum = [] #'testsum'
        sample_dir_save = 'dir/test'
        sample_clean_cache = False
        sample_verbose = False

        # process download+extract all files
        utils.download_extract_all(sample_urls, sample_md5sum, sample_dir_save, \
                                   sample_clean_cache, sample_verbose)

        # check if the mocked functions were called properly
        self.assertTrue(mock_url.called, "Failed to mock utils.url_get_filename().")
        self.assertTrue(mock_download.called, "Failed to mock utils.download_file().")
        self.assertTrue(mock_extract.called, "Failed to mock utils.extract_file().")
        self.assertFalse(mock_remove.called, "Failed to mock utils.remove_file().")


    @patch('__main__.utils.url_get_filename')
    @patch('__main__.utils.download_file')
    @patch('__main__.utils.check_file_integrity_md5')
    @patch('__main__.utils.extract_file')
    @patch('__main__.utils.remove_file')
    def test_download_extract_all__succeed_md5(self, mock_remove, mock_extract, mock_md5, mock_download, mock_url):
        """
        Test download+extract all files
        """
        # url samples
        sample_urls = ['url1/fname.tar', 'url2/fname.tar', 'url3/fname.zip']
        sample_md5sum = ['testsum1', 'testsum2', 'testsum3']
        sample_dir_save = 'dir/test'
        sample_clean_cache = False
        sample_verbose = False

        # mock function return values
        mock_md5.return_value = True

        # process download+extract all files
        utils.download_extract_all(sample_urls, sample_md5sum, sample_dir_save, sample_clean_cache, sample_verbose)

        # check if the mocked functions were called properly
        self.assertTrue(mock_url.called, "Failed to mock utils.url_get_filename().")
        self.assertTrue(mock_download.called, "Failed to mock utils.download_file().")
        self.assertTrue(mock_md5.called, "Failed to mock utils.check_file_integrity_md5().")
        self.assertTrue(mock_extract.called, "Failed to mock utils.extract_file().")
        self.assertFalse(mock_remove.called, "Failed to mock utils.remove_file().")


    @patch('__main__.utils.url_get_filename')
    @patch('__main__.utils.download_file')
    @patch('__main__.utils.check_file_integrity_md5')
    @patch('__main__.utils.extract_file')
    @patch('__main__.utils.remove_file')
    def test_download_extract_all__fail_md5(self, mock_remove, mock_extract, mock_md5, mock_download, mock_url):
        """
        Test download+extract all files
        """
        # url samples
        sample_urls = 'url'
        sample_md5sum = 'testsum'
        sample_dir_save = 'dir/test'
        sample_clean_cache = False
        sample_verbose = False

        # mock function effect
        mock_md5.return_value = False

        # process download+extract all files
        with self.assertRaises(Exception):
            utils.download_extract_all(sample_urls, sample_md5sum, sample_dir_save, \
                                   sample_clean_cache, sample_verbose)

        # check if the mocked functions were called properly
        self.assertTrue(mock_url.called, "Failed to mock utils.url_get_filename().")
        self.assertTrue(mock_download.called, "Failed to mock utils.download_file().")
        self.assertFalse(mock_extract.called, "Failed to mock utils.extract_file().")
        self.assertFalse(mock_remove.called, "Failed to mock utils.remove_file().")


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
