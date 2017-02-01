#!/usr/bin/env python3

"""
dbcollection/cache.py unit testing.
"""

# import data.py
import os
import sys
import copy

import unittest
from unittest import mock
from unittest.mock import patch, mock_open


dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
from dbcollection import cache


#-----------------------
# Unit Test definitions
#-----------------------

class CacheManagerTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__.cache.CacheManager.create_cache_file_disk')
    @patch('__main__.cache.CacheManager.read_data_cache')
    @patch('os.path.exists', return_value=True)
    def setUp(self, mock_os, mock_read, mock_file):
        """
        Initialize class.
        """
         # create a sample cache data dictionary
        self.sample_cache_data = {
            "info":{
                "default_cache_dir": "tmp/dir/",
                "default_data_dir": "tmp/dir/",
            },
            "dataset":{
                "image_processing":{
                    "cifar10":{
                        "cache_dir":"tmp/dir/",
                        "data_dir":"tmp/dir/",
                        "task":{
                            "default":"file1.h5",
                            "classific":"file2.h5",
                            "extra":"file3.h5"
                        }
                    }
                }
            }
        }

        # mock function return value
        mock_read.return_value = self.sample_cache_data

        # create class
        self.cache_manager = cache.CacheManager()

        # check if the object is of the same type
        self.assertIsInstance(self.cache_manager, cache.CacheManager, \
                              'Object is not of the same class')

        # check if the mocked functions were called correctly
        self.assertTrue(mock_os.called, 'Function should have been called')
        self.assertTrue(mock_read.called, 'Function should have been called')
        self.assertFalse(mock_file.called, 'Function should have not been called')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.load')
    def test_read_data_cache_file(self, mock_json):
        """
        Test loading data from the json file.
        """
        # sample json file
        json_sample = {"name":"data"}
        sample_mode = 'r'

        # mock json.load return value
        mock_json.return_value = json_sample

        # load data
        res = self.cache_manager.read_data_cache_file()

        # check if open was called with the correct parameters
        open.assert_called_with(self.cache_manager.cache_fname, sample_mode)

        # check if values match
        self.assertDictEqual(res, json_sample, 'Dictionaries should be equal')


    @patch('__main__.cache.CacheManager.read_data_cache_file')
    @patch('__main__.os.path.exists', return_value=True)
    def test_read_data_cache_file_existing(self, mock_path, mock_file):
        """
        Test loading data function.
        """
        # mock json.load return value
        mock_file.return_value = True

        # try load data
        res = self.cache_manager.read_data_cache()

        # check if values match
        self.assertTrue(res, 'Should have returned True')


    @patch('__main__.cache.CacheManager.empty_data')
    @patch('__main__.os.path.exists', return_value=False)
    def test_read_data_cache_non_existing(self, mock_path, mock_empty):
        """
        Test loading data function.
        """
        # sample data
        sample_data = [0, 1, 2]

        # mock json.load return value
        mock_empty.return_value = sample_data

        # try load data
        res = self.cache_manager.read_data_cache()

        # check if values match
        self.assertEqual(res, sample_data, 'Data should be equal')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.dump')
    def test_write_data_cache(self, mock_json):
        """
        Test write the dbcollection file.
        """
        # some data
        dic_sample = {"name1":"data1"}
        sample_mode = 'w'

        # fake write to a file
        self.cache_manager.write_data_cache(dic_sample)

        # check if open was called with the correct parameters
        open.assert_called_with(self.cache_manager.cache_fname, sample_mode)

        # check if the functions were mocked
        self.assertFalse(mock_json.dump.called, 'Failed to mock json.dump()')


    @patch('__main__.cache.CacheManager.write_data_cache')
    @patch('__main__.cache.CacheManager.empty_data')
    def test_create_cache_file_disk(self, mock_empty, mock_write):
        """
        Test initializing the cache with empty data.
        """
        # sample data
        sample_data = [0, 1, 2]
        sample_fname = 'test_fname.h5'

        # mock json.load return value
        mock_empty.return_value = sample_data

        # try load data
        self.cache_manager.create_cache_file_disk(sample_fname)

        # check if the function was called
        self.assertTrue(mock_empty.called, 'Function should have been called')

        # check if the function was called with the right parameters
        mock_write.assert_called_with(sample_data, sample_fname)


    @patch('os.remove', return_value=True)
    def test_os_remove(self, mock_os_remove):
        """
        Test removing a file from disk.
        """
        # sample data
        sample_file_name = 'test.h5'

        # attempt to remove a file
        self.cache_manager.os_remove(sample_file_name)

        # check if the function was called
        self.assertTrue(mock_os_remove.called, 'Function was not called')

        # check if the function was called with the right parameters
        mock_os_remove.assert_called_with(sample_file_name)


    @patch('__main__.cache.CacheManager.get_category')
    @patch('__main__.cache.CacheManager.get_data_from_field')
    @patch('__main__.cache.CacheManager.os_remove')
    @patch('__main__.cache.CacheManager.delete_entry')
    @patch('__main__.cache.CacheManager.write_data_cache')
    def test_delete_dataset_cache(self, mock_write, mock_delete, mock_remove, mock_get_data, mock_category):
        """
        Test deleting the cache data of a dataset.
        """
        # sample data
        sample_name = 'cifar10'
        sample_category = 'image_processing'
        sample_cache_dir_path = '/tmp/cache/dir'

        # mock function return value
        mock_category.return_value = sample_category
        mock_get_data.return_value = sample_cache_dir_path

        # delete the cache file for 'sample_name'
        self.cache_manager.delete_dataset_cache(sample_name)

        # check if the mocked function were called
        self.assertTrue(mock_category.called, 'Function should have been called')
        self.assertTrue(mock_get_data.called, 'Function should have been called')
        self.assertTrue(mock_remove.called, 'Function should have been called')
        self.assertTrue(mock_delete.called, 'Function should have been called')
        self.assertTrue(mock_write.called, 'Function should have been called')

        # check if the functions were called with the correct parameters
        mock_category.assert_called_with(sample_name)
        mock_get_data.assert_called_with(sample_name, 'cache_dir')
        mock_remove.assert_called_with(sample_cache_dir_path)
        mock_delete.assert_called_with(sample_category, sample_name)
        mock_write.assert_called_with(self.cache_manager.data)


    def test_check_dataset_name(self):
        """
        Test if a name string exists in the caches's dictionary.
        """
        # sample data
        sample_name1 = "cifar10"
        sample_name2 = "cifar1000"

        # check if name1 exists in the dictionary
        res1 = self.cache_manager.check_dataset_name(sample_name1)

        # check if it was a successful query
        self.assertTrue(res1, 'Should have given True')

         # check if name1 exists in the dictionary
        res2 = self.cache_manager.check_dataset_name(sample_name2)

        # check if it was a successful query
        self.assertFalse(res2, 'Should have given false')


    def test_get_data_from_field(self):
        """
        Test getting a field from cache data storage.
        """
        # sample data dictionary
        sample_name = 'cifar10'
        sample_field = "cache_dir"
        sample_path = self.cache_manager.data['dataset']['image_processing'][sample_name][sample_field]

        # get data from field
        res = self.cache_manager.get_data_from_field(sample_name, sample_field)

        # check if name matches the result
        self.assertEqual(res, sample_path, 'Paths should be the same')


    def test_change_field(self):
        """
        Test chaning the data of a field.
        """
        # sample data
        sample_name = 'cifar10'
        sample_field = 'cache_dir'
        sample_val = 'val'

        # do a deep copy of the cahce_manager data
        data_copy = copy.deepcopy(self.cache_manager.data)

        self.assertEqual(self.cache_manager.data, data_copy, 'Data should be equal')

        # change the value of a field
        self.cache_manager.change_field(sample_name, sample_field, sample_val)

        # check if data is different after the change of field value
        self.assertNotEqual(self.cache_manager.data, data_copy, 'Data should be different')

        # reset data value
        self.cache_manager.data = data_copy


    @patch('__main__.cache.CacheManager.get_dataset_data')
    def test_add_data(self, mock_get_data):
        """
        Test adding/appending data of a new dataset/category
        """
        # sample data
        sample_name = 'cifar10'
        sample_old_info = {'cached_files': {'data':'val'}}
        sample_new_info = {'cached_files': {'data2':'val2'}}
        reference_result = {'cached_files': {'data':'val', 'data2':'val2'}}

        # mock function return value
        mock_get_data.return_value = sample_old_info

        # append data to the old data
        self.cache_manager.add_data(sample_name, sample_new_info)

        # check if mocked function was called
        self.assertTrue(mock_get_data.called, 'Function should have been called')

        # check if the function was called with the correct parameters
        mock_get_data.assert_called_with(sample_name)

        # check if the appended data matches the reference output
        self.assertEqual(sample_old_info, reference_result, 'Dictionaries should be equal')


    @patch('__main__.cache.CacheManager.get_dataset_storage_paths')
    @patch('__main__.cache.CacheManager.delete_dataset_cache')
    @patch('__main__.cache.CacheManager.os_remove')
    def test_delete_dataset_cache(self, mock_os, mock_delete, mock_paths):
        """
        Test deleting a dataset from disk/cache
        """
        # sample data
        sample_name = 'test'
        sample_dst_paths = {'data_dir':'dir1/data', 'cache_dir':'dir1/cache'}
        sample_is_delete_data = False

        # mock function return values
        mock_paths.return_value = sample_dst_paths

        # delete dataset (preserve the data folder)
        self.cache_manager.delete_dataset(sample_name, sample_is_delete_data)

        # check if the functions where called
        self.assertTrue(mock_paths.called, 'Function should have been called')
        self.assertTrue(mock_delete.called, 'Function should have been called')
        self.assertFalse(mock_os.called, 'Function should have not been called')

        # check if the functions were called with the correct parameters
        mock_paths.assert_called_with(sample_name)
        mock_delete.assert_called_with(sample_name)


    @patch('__main__.cache.CacheManager.get_dataset_storage_paths')
    @patch('__main__.cache.CacheManager.delete_dataset_cache')
    @patch('__main__.cache.CacheManager.os_remove')
    def test_delete_dataset_data(self, mock_os, mock_delete, mock_paths):
        """
        Test deleting a dataset from disk/cache
        """
        # sample data
        sample_name = 'test'
        sample_dst_paths = {'data_dir':'dir1/data', 'cache_dir':'dir1/cache'}
        sample_is_delete_data = True

        # mock function return values
        mock_paths.return_value = sample_dst_paths

        # delete dataset (preserve the data folder)
        self.cache_manager.delete_dataset(sample_name, sample_is_delete_data)

        # check if the functions where called
        self.assertTrue(mock_paths.called, 'Function should have been called')
        self.assertTrue(mock_delete.called, 'Function should have been called')
        self.assertTrue(mock_os.called, 'Function should have been called')

        # check if the functions were called with the correct parameters
        mock_paths.assert_called_with(sample_name)
        mock_delete.assert_called_with(sample_name)
        mock_os.assert_called_with(sample_dst_paths['data_dir'])


    def test_get_category_exists(self):
        """
        Test getting the category name of a dataset.
        """
        # sample data
        sample_name = 'cifar10'
        reference_category = 'image_processing'

        # get the category of a dataset
        res = self.cache_manager.get_category(sample_name)

        # check if the output category name matches the result reference
        self.assertEqual(res, reference_category, 'Category names should be equal')


    def test_get_category_not_exists(self):
        """
        Test getting a category name of a dataset that does not exist.
        """
        # sample data
        sample_name = 'cifar1000'
        reference_category = None

        # get the category of a dataset
        res = self.cache_manager.get_category(sample_name)

        # check if the output category name matches the result reference
        self.assertEqual(res, reference_category, 'Category names should be equal')


    def test_exists_dataset_valid_name(self):
        """
        Test checking if a dataset+task exists.
        """
        # sample data
        sample_name = 'cifar10'

        # check if the dataset name exists
        res = self.cache_manager.exists_dataset(sample_name)

        # validate output result
        self.assertTrue(res, 'Should be True')

    def test_exists_dataset_invalid_name(self):
        """
        Test checking if a dataset+task exists.
        """
        # sample data
        sample_name = 'cifar1000'

        # check if the dataset name exists
        res = self.cache_manager.exists_dataset(sample_name)

        # validate output result
        self.assertFalse(res, 'Should be False')


    def test_exists_task_valid_dataset_valid_task(self):
        """
        Test checking if a dataset+task exists in the cache file.
        """
        # sample data
        sample_name = 'cifar10'
        sample_task = 'default'

        # check if the task exists for this dataset
        res = self.cache_manager.exists_task(sample_name, sample_task)

        # validate output result
        self.assertTrue(res, 'Should be True')


    def test_exists_task_valid_dataset_invalid_task(self):
        """
        Test checking if a dataset+task exists in the cache file.
        """
        # sample data
        sample_name = 'cifar10'
        sample_task = 'detection'

        # check if the task exists for this dataset
        res = self.cache_manager.exists_task(sample_name, sample_task)

        # validate output result
        self.assertFalse(res, 'Should be False')


    @patch('__main__.cache.CacheManager.read_data_cache')
    def test_get_valid_dataset_storage_paths(self, mock_read):
        """
        Test get the cache/data paths for a existing dataset.
        """
        # dataset name
        sample_data = self.sample_cache_data
        sample_name = 'cifar10'
        sample_field_cache = "cache_dir"
        sample_field_data = "data_dir"
        sample_path_cache = sample_data['dataset']['image_processing'][sample_name][sample_field_cache]
        sample_path_data = sample_data['dataset']['image_processing'][sample_name][sample_field_data]

        # set custom return value for the mocked functions
        mock_read.return_value = self.sample_cache_data

        # get path
        res = self.cache_manager.get_dataset_storage_paths(sample_name)

        # check if the paths are the same
        self.assertEqual(res[sample_field_cache], sample_path_cache, 'Paths should be equal')
        self.assertEqual(res[sample_field_data], sample_path_data, 'Paths should be equal')


    @patch('__main__.cache.CacheManager.read_data_cache')
    def test_get_invalid_dataset_storage_paths(self, mock_read):
        """
        Test get the cache/data paths for an invalid dataset.
        """
        # dataset name
        sample_data = self.sample_cache_data
        sample_name = 'dataset'
        sample_field_cache = "cache_dir"
        sample_field_data = "data_dir"
        sample_path_cache = os.path.join(self.cache_manager.default_cache_dir, sample_name, 'cache')
        sample_path_data = os.path.join(self.cache_manager.default_data_dir, sample_name, 'data')

        # set custom return value for the mocked functions
        mock_read.return_value = self.sample_cache_data

        # get path
        res = self.cache_manager.get_dataset_storage_paths(sample_name)

        # check if the paths are the same
        self.assertEqual(res[sample_field_cache], sample_path_cache, 'Paths should be equal')
        self.assertEqual(res[sample_field_data], sample_path_data, 'Paths should be equal')


    def test_get_dataset_data_valid_name(self):
        """
        Test returning the cache data of a existing dataset.
        """
        # sample data
        sample_name = 'cifar10'
        reference_cache_data = self.cache_manager.data['dataset']['image_processing'][sample_name]

        # get dataset data
        res = self.cache_manager.get_dataset_data(sample_name)

        # validate the output data
        self.assertEqual(res, reference_cache_data, 'Dictionaries should be equal')


    #@unittest.skip("Skip testing")
    def test_get_dataset_data_invalid_name(self):
        """
        Test returning the cache data of a existing dataset.
        """
        # sample data
        sample_name = 'cifar1000'

        # get dataset data (should raise an exception)
        with self.assertRaises(self.cache_manager.get_dataset_data(sample_name)):
            self.assertFalse(True, 'Should have given an exception')


    @patch('__main__.cache.CacheManager.get_dataset_data')
    def test_get_cache_path_valid_dataset_valid_task(self, mock_get_data):
        """
        Test fetching the cache path of a specific task.
        """
        # sample data
        sample_name = 'cifar10'
        sample_task = 'default'
        sample_cache_fname = 'file1.h5'
        sample_data = {'task':{sample_task: sample_cache_fname}}

        # mock function return value
        mock_get_data.return_value = sample_data

        # fetch cache path
        res = self.cache_manager.get_cache_path(sample_name, sample_task)

        # validate the output result
        self.assertEqual(res, sample_cache_fname, 'Strings should be equal')

        # check if the functions were called with the correct parameters
        mock_get_data.assert_called_with(sample_name)

    @unittest.skip("Skip testing")
    @patch('__main__.cache.CacheManager.get_dataset_data')
    def test_get_cache_path_valid_dataset_invalid_task(self, mock_get_data):
        """
        Test fetching the cache path of a specific (invalid) task.
        """
        # sample data
        sample_name = 'cifar10'
        sample_task = 'detect'
        sample_data = self.cache_manager.data
        sample_cache_fname = sample_data['dataset']['image_processing']['cifar10']['task'][sample_task]

        # mock function return value
        mock_get_data.return_value = sample_data

        # fetch cache path
        with self.assertRaises(self.cache_manager.get_cache_path(sample_name, sample_task)):
            self.assertFalse(True, 'Should have given an exception')

        # check if the functions were called with the correct parameters
        mock_get_data.assert_called_with(sample_name)


    @patch('__main__.cache.CacheManager.add_data')
    @patch('__main__.cache.CacheManager.write_data_cache')
    def test_update_cache(self, mock_write, mock_add):
        """
        Test updating the cache with new data.
        """
        # sample data
        sample_new_name = 'cifar1000'
        sample_data_dir = 'dir1/cifar1000/data'
        sample_cache_dir = 'dir1/cifar1000/cache'
        sample_cache_info = {}
        reference_new_info = {
            "data_dir": sample_data_dir,
            "cache_dir": sample_cache_dir,
            "task": sample_cache_info
        }

        # update data
        self.cache_manager.update(sample_new_name, sample_data_dir, sample_cache_dir, sample_cache_info)

        # check if functions were called
        self.assertTrue(mock_add.called, 'Function should have been called')
        self.assertTrue(mock_write.called, 'Function should have been called')

        # check if the functions were called with the correct parameters
        mock_add.assert_called_with(sample_new_name, reference_new_info)
        mock_write.assert_called_with(self.cache_manager.data)


#----------------
# Run Test Suite
#----------------

def main(level=2):
    """Main function to start testing"""
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
