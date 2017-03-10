#!/usr/bin/env python3


"""
dbcollection/loader.py unit testing.
"""

import os
import sys
import numpy as np
import h5py

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
            'filenames': ['dir1/fname1.jpg', 'dir1/fname2.jpg',
                          'dir1/fname3.jpg', 'dir1/fname4.jpg'],
            'class_names': ['banana', 'orange', 'apple'],
            'object_fields': ['filenames', 'class_id'],
            'object_ids': [[0,0], [1,1], [2,2], [3,1]],
            'class_id': [0, 1, 2, 1]
        }

        # write data to file
        self.save_path = os.path.join(os.path.expanduser("~"), 'tmp', 'tests')
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.filename_hdf5 = os.path.join(self.save_path, 'unittest_loader_file.h5')
        if os.path.exists(self.filename_hdf5):
            os.remove(self.filename_hdf5)
        
        self.hdf5_file_handler = h5py.File(self.filename_hdf5 , 'w', libver='latest')

        self.hdf5_file_handler['filenames'] = utils.convert_str_to_ascii(self.data['filenames'])
        self.hdf5_file_handler['class_names'] = utils.convert_str_to_ascii(self.data['class_names'])
        self.hdf5_file_handler['object_fields'] = utils.convert_str_to_ascii(self.data['object_fields'])
        self.hdf5_file_handler['object_ids'] = np.array(self.data['object_ids'])
        self.hdf5_file_handler['class_id'] = np.array(self.data['class_id'])

        # setup the loader class
        self.manager = loader.ManagerHDF5(self.hdf5_file_handler)


    def test_get_data__from_field__filenames(self):
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


    def test_get_data__from_field__class_names(self):
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


    def test_get_data__from_field__objects(self):
        """
        Test retrieving data from a field.
        """
        # sample data
        sample_field_name = 'object_ids'
        sample_id = 0
        sample_field_data = self.manager.data[sample_field_name][sample_id]

        # fetch data using the loader api
        res = self.manager.get(sample_field_name, sample_id)

        # check if the data is the same for both cases
        self.assertEqual(sample_field_data.tolist(), res.tolist(), 'Data should be equal')


    def test_get_data__from_field__filenames__multiple_ids(self):
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


    def test_get_data__from_field__filenames__multiple_ids_sparse(self):
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


    def test_get_ids__single_object(self):
        """
        Test retrieving all field ids of an object.
        """
        # sample data
        sample_id = 0
        sample_object_data = self.manager.data['object_ids'][sample_id]
        is_value = False

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        self.assertEqual(res.tolist(), sample_object_data.tolist(), 'Lists should be equal')


    def test_get_ids__multiple_object(self):
        """
        Test retrieving all field ids of multiple objects.
        """
        # sample data
        sample_id = [0, 1, 2, 3]
        sample_object_data = self.manager.data['object_ids'][sample_id]
        is_value = False

        # fetch data using the loader api
        res = self.manager.object(sample_id, is_value)

        # check if the data is the same for both cases
        self.assertEqual(res.tolist(), sample_object_data.tolist(), 'Lists should be equal')


    def test_get_values__single_object(self):
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


    def test_get_values__multiple_object(self):
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


    def test_get_size__field__filenames(self):
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


    def test_get_size__field__class_names(self):
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


    def test_get_size__object(self):
        """
        Test retrieving the size (num of elements) of an object and a field.
        """
        # sample data
        sample_field_name = 'object_ids'
        sample_size = self.manager.data[sample_field_name].shape[0]

        # get size from loader api
        res = self.manager.size()

        # check if the sizes are the same
        self.assertEqual(res, sample_size, 'Sizes should be equal')


    def test_get_size__invalid_field(self):
        """
        Test retrieving the size (num of elements) of an object and a field.
        """
        # sample data
        sample_field_name = 'non_existing_field'

        # get size from loader api (should raise an exception)
        with self.assertRaises(KeyError):
            res = self.manager.size(sample_field_name)


    def test_list_all_fields(self):
        """
        Test listing all field names.
        """
        # sample data field names
        sample_names = list(self.data.keys())
        sample_names.sort() # order list to make comparison easier

        # get list of field names from loader api
        res = self.manager.list()
        res.sort() # order list to make comparison easier

        # check if the sizes are the same
        self.assertEqual(res, sample_names, 'List should be equal')


    def tearDown(self):
        """
        Remove setup files.
        """
        self.hdf5_file_handler.close()
        os.remove(self.filename_hdf5)


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
