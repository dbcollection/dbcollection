#!/usr/bin/env python3


"""
dbcollection/storage.py unit testing.
"""


# import data.py
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
from dbcollection import storage

import unittest
from unittest import mock
from unittest.mock import patch, mock_open


#-----------------------
# Unit Test definitions
#-----------------------

class StorageHDF5Test(unittest.TestCase):
    """
    Test class.
    """

    @patch("__main__.storage.StorageHDF5.open_file")
    @patch("__main__.storage.StorageHDF5.add_group")
    def setUp(self, mock_group, mock_file):
        """
        Initialize class.
        """
        # dummy file name
        sample_file_name = 'dir/myfile.h5'
        sample_mode = 'w'

        # create a fake hdf5 storage dictionary
        class mydict(dict):
            def create_group(self, name):
                return True

            def create_dataset(self, field_name, data):
                return True

        self.sample_data = mydict({
            'train': {},
            'test': {'test_field':'test_val'},
            'val': {},
        })

        # mock function
        mock_file.return_value = self.sample_data
        mock_group.return_value = True

        # Load a hdf5 file manager
        self.hdf5storage = storage.StorageHDF5(sample_file_name, sample_mode)

        # check if the filenames are the same
        self.assertEqual(self.hdf5storage.fname, sample_file_name, 'File names should be equal')
        self.assertEqual(self.hdf5storage.mode, sample_mode, 'Mode string/char should be equal')


    @patch("__main__.storage.h5py.File")
    def test_open_file(self, mock_h5file):
        """
        Test opening a hdf5 file.
        """
        # some dummy file name
        sample_file_name = 'myfile.h5'
        sample_mode = "w"

        # mock function (modify output)
        mock_h5file.return_value = True

        # open the file
        res = self.hdf5storage.open_file(sample_file_name, sample_mode)

        # check if the file open successfuly
        self.assertTrue(res, 'Should have given True')


    def test_is_group__valid_group_name(self):
        """
        Test checking if a group exists.
        """
        # sample data
        sample_name = 'test'

        # check if the name exists in the group data
        res = self.hdf5storage.is_group(sample_name)

        # check if the output is correct
        self.assertTrue(res, 'Should have given True')


    def test_is_group__invalid_group_name(self):
        """
        Test checking if a group exists.
        """
        # sample data
        sample_name = 'testxyz'

        # check if the name exists in the group data
        res = self.hdf5storage.is_group(sample_name)

        # check if the output is correct
        self.assertFalse(res, 'Should have given False')


    @patch('__main__.setattr')
    def test_add_group__non_existing(self, mock_set):
        """
        Test creating groups in the hdf5 file.
        """
        # some dummy groups
        sample_name = 'test_group'

        # create groups
        self.hdf5storage.add_group(sample_name)


    @patch("__main__.storage.StorageHDF5.is_group", return_value=True)
    def test_delete_group(self, mock_is_group):
        """
        Test deleting a group.
        """
        # sample data
        sample_group = 'val'

        # delete a group
        self.hdf5storage.delete_group(sample_group)

        # check if the storage dictionary still has the field
        self.assertFalse(sample_group in self.hdf5storage.storage.keys(), 'Should have given False')

        # check if the function was correctly called
        self.assertTrue(mock_is_group.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_is_group.assert_called_with(sample_group)


    @patch("__main__.storage.StorageHDF5.is_group", return_value=True)
    def test_is_data__existing_group_existing_field(self, mock_is_group):
        """
        Test check if a field name exists.
        """
        # sample data
        sample_group = 'test'
        sample_field_name = 'test_field'

        # check if the sample field name exists
        res = self.hdf5storage.is_data(sample_group, sample_field_name)

        # check if the field exists
        self.assertTrue(res, 'Should have given True')

        # check if the function was correctly called
        self.assertTrue(mock_is_group.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_is_group.assert_called_with(sample_group)


    @patch("__main__.storage.StorageHDF5.parse_str")
    def test_add_data(self, mock_parse):
        """
        Test adding data to a hdf5 file.
        """
        # sample data
        sample_group = 'test'
        sample_field_name = 'test_field'
        sample_dtype = None
        sample_concat_str = sample_group + '/' + sample_field_name

        # mock function return value
        mock_parse.return_value = sample_concat_str

        # add data to the group
        self.hdf5storage.add_data(sample_group, sample_field_name, sample_dtype)

        # check if the mocked function was correctly called
        self.assertTrue(mock_parse.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_parse.assert_called_with(sample_group, sample_field_name)


    @patch("__main__.storage.StorageHDF5.is_data", return_value=True)
    @patch("__main__.storage.StorageHDF5.parse_str")
    def test_delete_data(self, mock_parse, mock_is_data):
        """
        Test deleting data from a hdf5 file.
        """
        # sample data
        sample_group = 'test'
        sample_field_name = 'test_field'
        sample_concat_str = 'train' # small work arround (cheat) to simulate an access to a h5py file

        # mock function return value
        mock_parse.return_value = sample_concat_str

        # delete data field
        self.hdf5storage.delete_data(sample_group, sample_field_name)

        # check if data field still exists
        self.assertFalse(sample_concat_str in self.sample_data.keys(), \
                        'Should have given False')

        # check if the mocked function was correctly called
        self.assertTrue(mock_is_data.called, 'Function should have been called')
        self.assertTrue(mock_parse.called, 'Function should have been called')

        # check if functions were called with the right parameters
        mock_is_data.assert_called_with(sample_group, sample_field_name)
        mock_parse.assert_called_with(sample_group, sample_field_name)


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
