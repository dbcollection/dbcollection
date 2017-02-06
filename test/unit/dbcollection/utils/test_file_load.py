#!/usr/bin/env python3

"""
file_load.py unit testing.
"""


import os
import sys

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection', 'utils'))
sys.path.append(lib_path)
from file_load import *


#-----------------------
# Unit Test definitions
#-----------------------

class FileLoadTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('builtins.open', mock_open(read_data=True))
    def test_open_read_file__success(self):
        """
        Test opening a file in read mode.
        """
        # sample data
        sample_file_name = 'test.txt'
        sample_mode = 'r'

        # open and read a file
        res = open_read_file(sample_file_name, sample_mode)

        # check if the output is true
        self.assertTrue(res, 'Should have given true')
    

    @patch('__main__.open',side_effect=IOError)
    def test_open_read_file__fail(self, mock_file):
        """
        Test opening a file in read mode.
        """
        # sample data
        sample_file_name = 'test.txt'
        sample_mode = 'r'

        # open and read a file
        with self.assertRaises(IOError):
            res = open_read_file(sample_file_name, sample_mode)


    @patch('__main__.scipy.loadmat', return_value=True)
    def test_load_matlab_file__valid(self, mock_loadmat):
        """
        Description
        """
        # sample data
        sample_file_name = 'filename.mat'

        # load dummy file
        res = load_matlab(sample_file_name)

        # check if the output is True
        self.assertTrue(res, 'Should have given True')

        # check if the function was correctly called
        self.assertTrue(mock_loadmat.called, 'Function should have been called')

        # check if the function was called with the right parmeters
        mock_loadmat.assert_called_with(sample_file_name)


    @patch('__main__.scipy.loadmat')
    def test_load_matlab_file__raise_exception(self, mock_loadmat):
        """
        Description
        """
        # sample data
        sample_file_name = 'filename.mat'

        # load dummy file
        res = load_matlab(sample_file_name)

        # mock function behaviour
        mock_loadmat.side_effect = IOError


        # load dummy file (should raise an exception)
        with self.assertRaises(IOError):
            res = load_matlab(sample_file_name)

        # check if the function was correctly called
        self.assertTrue(mock_loadmat.called, 'Function should have been called')

        # check if the function was called with the right parmeters
        mock_loadmat.assert_called_with(sample_file_name)


    @patch('builtins.open', mock_open(read_data='test'))
    @patch('__main__.json.load', return_value=True)
    def test_load_json__succeed(self, mock_load):
        """
        Test opening and reading the data of a json file.
        """
        # sample data
        sample_file_name = 'test.txt'

        # load a json file
        res = load_json(sample_file_name)
    
        # check if the output is True
        self.assertTrue(res, 'Should have given True')

        # check if the mocked function was correctly called
        self.assertTrue(mock_load.called, 'json.load() should have been called')


    @patch('builtins.open', mock_open(read_data='test'))
    @patch('__main__.pickle.load', return_value=True)
    def test_load_pickle__succeed(self, mock_load):
        """
        Test opening and reading the data of a pickled file.
        """
        # sample data
        sample_file_name = 'test.json'

        # load a json file
        res = load_pickle(sample_file_name)
    
        # check if the output is True
        self.assertTrue(res, 'Should have given True')

        # check if the mocked function was correctly called
        self.assertTrue(mock_load.called, 'pickle.load() should have been called')


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
