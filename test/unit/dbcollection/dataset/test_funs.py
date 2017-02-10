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
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection', 'dataset'))
sys.path.append(lib_path)
from funs import *


#-----------------------
# Unit Test definitions
#-----------------------

class FunsTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__.fetch_dataset_constructor')
    @patch('__main__.os.path.join')
    def test_setup_dataset_constructor(self, mock_join, mock_fetch):
        """
        Test configurating a dataset constructor class.
        """
        # sample data
        sample_name = 'cifar10'
        sample_data_dir = ''
        sample_cache_dir = ''
        sample_verbose = True
        sample_join_out = 'out'
        sample_fetch_output_category = 'category_output'
        sample_constructor_output = 'constructor_output'

        # mock function return value
        mock_join.return_value = sample_join_out

        # mock fetch function behaviour
        # def output(name):
        #     def constructor(*args):
        #         return sample_constructor_output
        #     return sample_fetch_output_category, constructor
        # mock_fetch.side_effect = output


        # setup dataset constructor
        dloader, data_dir, cache_dir, category = setup_dataset_constructor(
            sample_name, sample_data_dir, sample_cache_dir, sample_verbose)

        # check if the outputs are the correct ones
        self.assertEqual(dloader, sample_constructor_output, 'dataset_loader')
        self.assertEqual(data_dir, sample_join_out, 'data_dir_')
        self.assertEqual(cache_dir, sample_join_out, 'cache_dir_')
        self.assertEqual(category, sample_fetch_output_category, 'category')


    @patch('__main__.setup_dataset_constructor')
    @patch('__main__.os.path.exists', return_value=True)
    def test_download(self, mock_exists, mock_setup):
        """
        Test downloading a dataset.
        """
        # sample data
        sample_name = 'cifar10'
        sample_data_dir = ''
        sample_cache_dir = ''
        sample_verbose = True

        # download a dataset
        download(sample_name, sample_data_dir, sample_cache_dir, sample_verbose)



    def test_process(self):
        """
        Test processing a dataset.
        """
        self.fail()


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()

