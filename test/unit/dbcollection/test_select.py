#!/usr/bin/env python3

"""
select.py unit testing.
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
from select_filter import *

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', 'dbcollection', 'utils'))
sys.path.append(lib_path)
from string_ascii import convert_str_to_ascii



#-----------------------
# Unit Test definitions
#-----------------------

class SelectTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # sample data
        self.sample_test_hdf_file = 'test_select_data.h5'

        sample_train_filename = convert_str_to_ascii(['fname1', 'fname2', 'fname3', \
                                    'fname4', 'fname5', 'fname6', \
                                    'fname7', 'fname8', 'fname9'])
        sample_train_class = convert_str_to_ascii(['class1', 'class2', 'class3', 'class4'])
        sample_train_object_fields = convert_str_to_ascii(['filename', 'class'])
        sample_train_object_id = np.array([[1, 1], [2, 1], [3, 1], \
                                           [4, 2], [5, 2], [6, 2], \
                                           [7, 3], [8, 3], [9, 3], \
                                          ])

        # check if the file exists on disk
        if os.path.exists(self.sample_test_hdf_file):
            os.remove(self.sample_test_hdf_file)

        # create a hdf5 data file
        self.data = h5py.File(self.sample_test_hdf_file, 'w', libver='latest')
        tr = self.data.create_group('train')
        tr.create_dataset('filename', data=sample_train_filename)
        tr.create_dataset('class', data=sample_train_class)
        tr.create_dataset('object_fields', data=sample_train_object_fields)
        tr.create_dataset('object_id', data=sample_train_object_id)


    def test_select_one_class_from_data__valid_field(self):
        """
        Test selecting two classes from the available 4 classes.
        """
        # sample data
        sample_field_name = 'class'
        sample_is_select = True
        target_class = 'class1'
        sample_search = [sample_field_name, target_class, 'eq']
        expected_result = np.array([[1, 1], [2, 1], [3, 1]])
        expected_classes = [convert_str_to_ascii([target_class]).tolist()]

        # select data
        filter_data(self.data['train'], sample_search, sample_is_select)

        # check if the field sample_field_list exists
        self.assertEqual(self.data['train']['class'].value.tolist(), expected_classes, \
                         'classes: expected equal result')
        self.assertEqual(self.data['train']['object_id'].value.tolist(), expected_result.tolist(), \
                         'objects: expected equal result')


    def test_select_two_classes_from_data__valid_field(self):
        """
        Test selecting two classes from the available 4 classes.
        """
        # sample data
        sample_field_name = 'class'
        sample_is_select = True
        target_class1 = 'class1'
        target_class2 = 'class3'
        sample_search = [sample_field_name, [target_class1, target_class2], ['eq', 'eq']]
        expected_object_id = np.array([[1, 1], [2, 1], [3, 1], \
                                           [7, 3], [8, 3], [9, 3], \
                                          ])
        expected_classes = convert_str_to_ascii([target_class1, target_class2]).tolist()

        # select data
        filter_data(self.data['train'], sample_search, sample_is_select)

        # check if the field sample_field_list exists
        self.assertEqual(self.data['train']['class'].value.tolist(), expected_classes, \
                         'classes: expected equal result')
        self.assertEqual(self.data['train']['object_id'].value.tolist(), expected_object_id.tolist(), \
                         'objects: expected equal result')


    def test_filter_one_class_from_data__valid_field(self):
        """
        Test selecting two classes from the available 4 classes.
        """
        # sample data
        sample_field_name = 'class'
        sample_is_select = False
        target_class = 'class1'
        sample_search = [sample_field_name, target_class, 'eq']
        expected_object_id = np.array([ [4, 2], [5, 2], [6, 2], \
                                        [7, 3], [8, 3], [9, 3], \
                                      ])
        expected_classes = convert_str_to_ascii(['class2', 'class3', 'class4'])

        # select data
        filter_data(self.data['train'], sample_search, sample_is_select)

        # check if the field sample_field_list exists
        self.assertEqual(self.data['train']['class'].value.tolist(), expected_classes.tolist(), \
                         'classes: expected equal result')
        self.assertEqual(self.data['train']['object_id'].value.tolist(), expected_object_id.tolist(), \
                         'objects: expected equal result')


    def test_filter_two_classes_from_data__valid_field(self):
        """
        Test selecting two classes from the available 4 classes.
        """
        # sample data
        sample_field_name = 'class'
        sample_is_select = False
        target_class1 = 'class1'
        target_class2 = 'class3'
        sample_search = [sample_field_name, [target_class1, target_class2], ['eq', 'eq']]
        expected_object_id = np.array([[4, 2], [5, 2], [6, 2]])
        expected_classes = convert_str_to_ascii(['class2', 'class4']).tolist()

        # select data
        filter_data(self.data['train'], sample_search, sample_is_select)

        # check if the field sample_field_list exists
        self.assertEqual(self.data['train']['class'].value.tolist(), expected_classes, \
                         'classes: expected equal result')
        self.assertEqual(self.data['train']['object_id'].value.tolist(), expected_object_id.tolist(), \
                         'objects: expected equal result')


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
