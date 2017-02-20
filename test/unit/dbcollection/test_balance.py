#!/usr/bin/env python3

"""
balance.py unit testing.
"""


import os
import sys
import numpy as np
import h5py

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', 'dbcollection'))
sys.path.append(lib_path)
from balance import *

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', 'dbcollection', 'utils'))
sys.path.append(lib_path)
from string_ascii import convert_str_to_ascii


#-----------------------
# Unit Test definitions
#-----------------------

class BalanceSetsTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # sample data
        self.sample_test_hdf_file = 'test_balance_data.h5'

        # check if the file exists on disk
        if os.path.exists(self.sample_test_hdf_file):
            os.remove(self.sample_test_hdf_file)

        # create a hdf5 data file
        self.data = h5py.File(self.sample_test_hdf_file, 'w', libver='latest')

        # create train data
        self.train_filename = convert_str_to_ascii([\
            'fname1', 'fname2', 'fname3', \
            'fname4', 'fname5', 'fname6', \
            'fname7', 'fname8', 'fname9'])
        self.train_class = convert_str_to_ascii(['class1', 'class2', 'class3'])
        self.train_object_fields = convert_str_to_ascii(['filename', 'class'])
        self.train_object_id = np.array([\
            [1, 1], [2, 1], [3, 1], \
            [4, 2], [5, 2], [6, 2], \
            [7, 3], [8, 3], [9, 3]])

        tr = self.data.create_group('train')
        tr.create_dataset('filename', data=self.train_filename)
        tr.create_dataset('class', data=self.train_class)
        tr.create_dataset('object_fields', data=self.train_object_fields)
        tr.create_dataset('object_id', data=self.train_object_id)

        # create val data
        self.val_filename = convert_str_to_ascii([
            'fname10', 'fname11', 'fname12', \
            'fname13', 'fname14', 'fname15', \
            'fname16', 'fname17', 'fname18'])
        self.val_class = convert_str_to_ascii(['class1', 'class2', 'class3'])
        self.val_object_fields = convert_str_to_ascii(['filename', 'class'])
        self.val_object_id = np.array([ \
            [1, 1], [2, 1], [3, 1],\
            [4, 2], [5, 2], [6, 2],\
            [7, 3], [8, 3], [9, 3]])

        val = self.data.create_group('val')
        val.create_dataset('filename', data=self.val_filename)
        val.create_dataset('class', data=self.val_class)
        val.create_dataset('object_fields', data=self.val_object_fields)
        val.create_dataset('object_id', data=self.val_object_id)

        # create test data
        self.test_filename = convert_str_to_ascii([
            'fname10', 'fname11', 'fname12', \
            'fname13', 'fname14', 'fname15', \
            'fname16', 'fname17', 'fname18'])
        self.test_class = convert_str_to_ascii(['class1', 'class2', 'class3'])
        self.test_object_fields = convert_str_to_ascii(['filename', 'class'])
        self.test_object_id = np.array([ \
            [1, 1], [2, 1], [3, 1],\
            [4, 2], [5, 2], [6, 2],\
            [7, 3], [8, 3], [9, 3]])

        ts = self.data.create_group('test')
        ts.create_dataset('filename', data=self.test_filename)
        ts.create_dataset('class', data=self.test_class)
        ts.create_dataset('object_fields', data=self.test_object_fields)
        ts.create_dataset('object_id', data=self.test_object_id)


    def test_balance_train_val_sets__100_100_invalid_range(self):
        """
        Test balancing the train and validation sets with a 100-100 split.

        NOTE: This should error due to invalid range (> 100).
        """
        # sample data
        sets = ['train', 'val']
        splits = [100, 100]

        # attempt to balance sets
        with self.assertRaises(AssertionError):
            balance(self.data, sets, splits)


    def test_balance_train_val_sets__10_10_invalid_range(self):
        """
        Test balancing the train and validation sets with a 10-10 split.

        NOTE: This should error due to invalid range (<100).
        """
        # sample data
        sets = ['train', 'val']
        splits = [10, 10]

        # attempt to balance sets
        with self.assertRaises(AssertionError):
            balance(self.data, sets, splits)


    def test_balance_train_val_sets__100_0_valid_range(self):
        """
        Test balancing the train and validation sets with a 100-100 split.

        NOTE: This should not give an error.
        """
        # sample data
        sets = ['train', 'val']
        splits = [100, 0]

        # attempt to balance sets
        balance(self.data, sets, splits)


    def test_balance_train_val_sets__50_50_valid_range(self):
        """
        Test balancing the train and validation sets with a 50-50 split.

        Note: The sets should stay the same.
        """
        # sample data
        sets = ['train', 'val']
        splits = [50, 50]

        # do balancing
        balance(self.data, sets, splits)

        # check if the data remains the same
        self.assertEqual(self.data['train']['filename'].value.tolist(), \
                         self.train_filename.tolist(), \
                         'train: filename')

        self.assertEqual(self.data['train']['object_fields'].value.tolist(), \
                         self.train_object_fields.tolist(), \
                         'train: object_fields')

        self.assertEqual(self.data['val']['filename'].value.tolist(), \
                         self.val_filename.tolist(), \
                         'val: filename')

        self.assertEqual(self.data['val']['object_fields'].value.tolist(), \
                         self.val_object_fields.tolist(), \
                         'val: object_fields')


    def test_balance_train_val_sets__75_25_valid_range(self):
        """
        Test balancing the train and validation sets with a 75-25 split.
        """
        # sample data
        sets = ['train', 'val']
        splits = [75, 25]

        # do balancing
        balance(self.data, sets, splits)
        
        # check if the data remains the same
        self.assertNotEqual(self.data['train']['filename'].value.tolist(), \
                         self.train_filename.tolist(), \
                         'train: filename')

        self.assertNotEqual(self.data['train']['object_fields'].value.tolist(), \
                         self.train_object_fields.tolist(), \
                         'train: object_fields')

        self.assertNotEqual(self.data['val']['filename'].value.tolist(), \
                         self.val_filename.tolist(), \
                         'val: filename')

        self.assertNotEqual(self.data['val']['object_fields'].value.tolist(), \
                         self.val_object_fields.tolist(), \
                         'val: object_fields')
        

    def tearDown(self):
        """
        Remove the temporary data files.
        """
        self.data.close()

        # check if the file exists on disk
        if os.path.exists(self.sample_test_hdf_file):
            os.remove(self.sample_test_hdf_file)

#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
