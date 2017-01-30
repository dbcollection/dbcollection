#!/usr/bin/env python3


"""
dbcollection/loader.py unit testing.
"""

import os
import sys
import numpy as np

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..'))
sys.path.append(lib_path)
from dbcollection import utils, loader


#-----------------------
# Unit Test definitions
#-----------------------

class ManagerHDF5Test(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # some dummy data
        self.data = {
            'filenames': utils.convert_str_ascii(['dir1/fname1.jpg', 'dir1/fname2.jpg','dir1/fname3.jpg', 'dir1/fname4.jpg']),
            'class_names': utils.convert_str_ascii(['banana','orange','apple']),
            'object_fields': utils.convert_str_ascii(['filenames', 'class_id']),
            'object_id': np.array([[0,0], [1,1], [2,2], [3,1]]),
            'class_id': np.array([0, 1, 2, 1])
        }
        self.manager = loader.ManagerHDF5(self.data)


    def test_get_data_from_field_filenames(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'filenames'
        sample_id = 0
        sample_field_data = self.manager.data[sample_field_name][sample_id]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_data_from_field_class_names(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'class_names'
        sample_id = 0
        sample_field_data = self.manager.data[sample_field_name][sample_id]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_data_from_field_objects(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'object_id'
        sample_id = 0
        sample_field_data = self.manager.data[sample_field_name][sample_id]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_data_from_field_filenames_multiple_ids(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'filenames'
        sample_id_multiple = [0, 1, 2, 3]
        sample_field_data = self.manager.data[sample_field_name][sample_id_multiple]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id_multiple)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_data_from_field_filenames_multiple_ids_sparse(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'filenames'
        sample_id_multiple = [0, 2, 3]
        sample_field_data = self.manager.data[sample_field_name][sample_id_multiple]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id_multiple)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_ids_single_object(self):
        """
        Test retrieving all field ids of an object.
        """
        # sample data
        sample_id = 0
        sample_object_data = self.manager.data['object_id'][sample_id]
        is_value = False

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        self.assertEqual(res.tolist(), sample_object_data.tolist(), 'Lists should be equal')


    def test_get_ids_multiple_object(self):
        """
        Test retrieving all field ids of multiple objects.
        """
        # sample data
        sample_id = [0, 1, 2, 3]
        sample_object_data = self.manager.data['object_id'][sample_id]
        is_value = False

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        self.assertEqual(res.tolist(), sample_object_data.tolist(), 'Lists should be equal')


    def test_get_values_single_object(self):
        """
        Test retrieving all field values of an object.
        """
        # sample data
        sample_id = 0
        sample_object_data = [self.manager.data['filenames'][sample_id], self.manager.data['class_id'][sample_id]]
        is_value = True

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        self.assertEqual(res[0].tolist(), sample_object_data[0].tolist(), 'Lists should be equal')
        self.assertEqual(res[1], sample_object_data[1], 'Vals should be equal')


    def test_get_values_multiple_object(self):
        """
        Test retrieving all field values of multiple object.
        """
        # sample data
        sample_id = [0, 1, 2, 3]
        sample_object_data = [[self.manager.data['filenames'][id], self.manager.data['class_id'][id]] for id in sample_id]
        is_value = True

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        for i in sample_id:
            self.assertEqual(res[i][0].tolist(), sample_object_data[i][0].tolist(), 'Lists should be equal')
            self.assertEqual(res[i][1], sample_object_data[i][1], 'Vals should be equal')


    def test_get_size_field_filenames(self):
        """
        Test retrieving the size (num of elements) of an object and a field.
        """
        # sample data
        sample_field_name = 'filenames'
        sample_size = self.manager.data[sample_field_name].shape[0]

        # get size from loader api
        res = self.manager.size(sample_field_name)

        # check if the sizes are the same
        self.assertEqual(res, sample_size, 'Sizes should be equal')


    def test_get_size_field_class_names(self):
        """
        Test retrieving the size (num of elements) of an object and a field.
        """
        # sample data
        sample_field_name = 'class_names'
        sample_size = self.manager.data[sample_field_name].shape[0]

        # get size from loader api
        res = self.manager.size(sample_field_name)

        # check if the sizes are the same
        self.assertEqual(res, sample_size, 'Sizes should be equal')


    def test_get_size_object(self):
        """
        Test retrieving the size (num of elements) of an object and a field.
        """
        # sample data
        sample_field_name = 'object_id'
        sample_size = self.manager.data[sample_field_name].shape[0]

        # get size from loader api
        res = self.manager.size()

        # check if the sizes are the same
        self.assertEqual(res, sample_size, 'Sizes should be equal')


    def test_list_all_fields(self):
        """
        Test listing all field names.
        """
        # sample data field names
        sample_names = self.data.keys()

        # get list of field names from loader api
        res = self.manager.list()

        # check if the sizes are the same
        self.assertEqual(res, sample_names, 'List should be equal')



class DatasetLoaderTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # sample data
        sample_name = 'cifar10'
        sample_category = 'image_processing'
        sample_task = 'classification'
        sample_data_dir = '/dir1/data'
        sample_cache_file_path = 'dir1/metadata.h5',

        class MockClasses():
            storage = {sample_name: True}
            def __init__(self, name=None, mode=None):
                self.ok = True

        # mock functions
        loader.StorageHDF5 = MockClasses()
        loader.ManagerHDF5 = MockClasses()

        # create a loader object
      #  self.loader = loader.DatasetLoader(
      #      name = sample_name, 
      #      category = sample_category, 
      #      task = sample_task,
      #      data_dir = sample_data_dir,
      #      cache_path = sample_cache_file_path,
      #  )

        # check if the loader object was properly loaded
       # self.assertEqual(self.loader.name, sample_name ,'Values should be the same')
       # self.assertEqual(self.loader.category, sample_category ,'Values should be the same')
       # self.assertEqual(self.loader.task, sample_task ,'Values should be the same')
       # self.assertEqual(self.loader.data_dir, sample_data_dir ,'Values should be the same')
       # self.assertEqual(self.loader.cache_path, sample_cache_file_path ,'Values should be the same')


    
    def test_one(self):
        """
        Test one.
        """
        pass


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
