"""
dbcollection/utils.py unit testing.
"""


# import utils.py
import os
import sys
import inspect
import urllib
import requests
import tarfile
import zipfile
import json
from clint.textui import progress
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..','dbcollection'))
sys.path.append(lib_path)
import utils



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


    @patch('utils.get_hash_value')
    def test_check_file_integrity_md5(self, mock_get):
        """
        Test checking a file's integrity using md5 checksum.
        """
        # some dummy data
        sample_file_name = 'dir/myfile'
        sample_md5sum = 'sample_sum'

        # mock function output
        mock_get.return_value = sample_md5sum

        # compute function
        utils.check_file_integrity_md5(sample_file_name, sample_md5sum)

        # it should not raise an exception
        self.assertTrue(True)


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
        sample_md5sum = [] #'testsum'

        # process download+extract all files
        utils.download_extract_all(url_samples, sample_md5sum, 'any dir', True, True)

        # check if the mocked functions were called properly
        self.assertFalse(mock_url.url_get_filename.called, "Failed to mock utils.url_get_filename().")
        self.assertFalse(mock_download.download_file.called, "Failed to mock utils.download_file().")
        self.assertFalse(mock_extract.extract_file.called, "Failed to mock utils.extract_file().")
        self.assertFalse(mock_remove.remove_file.called, "Failed to mock utils.remove_file().")


    @patch('scipy.io.loadmat')
    def test_load_matlab_file(self, mock_loadmat):
        """
        Test loading a matlab file to memory.
        """
        # dummy file name
        sample_file_name = "dir/myfile.mat"
        sample_data = [1,2,3,4,5,6,'str']

        # mock function output
        mock_loadmat.return_value = sample_data

        # load dummy file
        res_data = utils.load_matlab(sample_file_name)

        # check if the sample data is the same as the returned from the load of the dummy file
        self.assertEqual(res_data, sample_data, 'Data lists should be equal')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.load')
    def test_load_json(self, mock_json):
        """
        Test loading a json file.
        """
        # dummy file name
        sample_file_name = "dir/myfile.json"
        sample_data = [1,2,3,4,5,6,'str']

        # mock function output
        mock_json.return_value = sample_data

        # load dummy file
        res_data = utils.load_json(sample_file_name)

        # check if the sample data is the same as the returned from the load of the dummy file
        self.assertEqual(res_data, sample_data, 'Data lists should be equal')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('pickle.load')
    def test_load_pickel(self, mock_pickle):
        """
        Test loading a pickle file.
        """
        # some dummy file name
        sample_file_name = 'dir/myfile'
        sample_data = 'test1'

        # mock function output
        mock_pickle.return_value = sample_data

        # load dummy file
        res_data = utils.load_pickle(sample_file_name)

        # check if the returned data matches the dummy data
        self.assertEqual(res_data, sample_data, 'Data vars should be equal')

#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
