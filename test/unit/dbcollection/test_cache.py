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
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', 'dbcollection'))
sys.path.append(lib_path)
from cache import CacheManager


#-----------------------
# Unit Test definitions
#-----------------------

class CacheManagerTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('__main__.CacheManager.create_cache_file_disk')
    @patch('__main__.CacheManager.read_data_cache')
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
                "cifar10":{
                    "cache_dir" : "tmp/dir/",
                    "data_dir" : "tmp/dir/",
                    "tasks":{
                        "default" : "file1.h5",
                        "classific" : "file2.h5",
                        "extra" : "file3.h5"
                        },
                    "keywords" : ['image_processing', 'classification']
                },
                "cifar100": {}
            },
            "category":{
                'image_processing': ['cifar10'],
                'classification': ['cifar10']
            }
        }

        # mock function return value
        mock_read.return_value = self.sample_cache_data

        # create class
        self.cache_manager = CacheManager()

        # check if the object is of the same type
        self.assertIsInstance(self.cache_manager, CacheManager, 'Object: CacheManager')

        # check if the mocked functions were called correctly
        self.assertTrue(mock_os.called, 'os.path.exists')
        self.assertTrue(mock_read.called, 'CacheManager.read_data_cache')
        self.assertFalse(mock_file.called, 'CacheManager.create_cache_file_disk')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.load')
    def test_read_data_cache_file__return_valid_data(self, mock_json):
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


    @patch('__main__.CacheManager.empty_data')
    @patch('__main__.CacheManager.read_data_cache_file')
    @patch('__main__.os.path.exists')
    def test_read_data_cache_file__valid_existing_file(self, mock_path, mock_file, mock_empty_data):
        """
        Test loading data function.
        """
        # sample data
        sample_data = {'data':'val'}
        sample_empty_data = {'data1':'val1'}
        sample_is_file = True

        # mock functions return value
        mock_path.return_value = sample_is_file
        mock_file.return_value = sample_data
        mock_empty_data.return_value = sample_empty_data

        # try load data
        res = self.cache_manager.read_data_cache()

        # check if values match
        self.assertEqual(res, sample_data, 'Dictionaries should be equal')

        # check if mocked functions were correctly called
        self.assertTrue(mock_path.called, 'Function should have been called')
        self.assertTrue(mock_file.called, 'Function should have been called')
        self.assertFalse(mock_empty_data.called, 'Function should have not been called')


    @patch('__main__.CacheManager.empty_data')
    @patch('__main__.CacheManager.read_data_cache_file')
    @patch('__main__.os.path.exists')
    def test_read_data_cache_file__non_existing_file(self, mock_path, mock_file, mock_empty_data):
        """
        Test loading data function.
        """
        # sample data
        sample_data = {'data':'val'}
        sample_empty_data = {'data1':'val1'}
        sample_is_file = False

        # mock functions return value
        mock_path.return_value = sample_is_file
        mock_file.return_value = sample_data
        mock_empty_data.return_value = sample_empty_data

        # try load data
        res = self.cache_manager.read_data_cache()

        # check if values match
        self.assertEqual(res, sample_empty_data, 'Dictionaries should be equal')

        # check if mocked functions were correctly called
        self.assertTrue(mock_path.called, 'Function should have been called')
        self.assertFalse(mock_file.called, 'Function should have been called')
        self.assertTrue(mock_empty_data.called, 'Function should have not been called')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.dump')
    def test_write_data_cache__valid_open_file(self, mock_json):
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


    @patch('__main__.CacheManager.write_data_cache')
    @patch('__main__.CacheManager.empty_data')
    def test_create_cache_file_disk__dont_raise_exception(self, mock_empty, mock_write):
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
    def test_os_remove__fake_remove_file(self, mock_os_remove):
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


    def test_delete_entry__valid_dataset(self):
        """
        Test removing a dataset entry from the cache.
        """
        # sample data
        sample_name = 'cifar10'
        sample_data_copy = copy.deepcopy(self.cache_manager.data)

        # remove the dataset
        self.cache_manager.delete_entry(sample_name)

        # check if the cache's data dictionary is different
        self.assertNotEqual(self.cache_manager.data, sample_data_copy, \
                            'Dictionaries should be different')

        # recover the default data dictionary
        self.cache_manager.data = sample_data_copy


    @patch('__main__.CacheManager.os_remove')
    @patch('__main__.CacheManager.delete_entry')
    @patch('__main__.CacheManager.write_data_cache')
    def test_delete_dataset_cache__fake_remove_cachedir_from_disk(self, mock_write, mock_delete, mock_remove):
        """
        Test deleting the cache data of a dataset.
        """
        # sample data
        name = 'cifar10'
        cache_dir_path = self.sample_cache_data['dataset'][name]['cache_dir']

        # delete the cache file for 'sample_name'
        self.cache_manager.delete_dataset_cache(name)

        # check if the mocked function were called
        self.assertTrue(mock_remove.called, 'Function should have been called')
        self.assertTrue(mock_delete.called, 'Function should have been called')
        self.assertTrue(mock_write.called, 'Function should have been called')

        # check if the functions were called with the correct parameters
        mock_remove.assert_called_with(cache_dir_path)
        mock_delete.assert_called_with(name)
        mock_write.assert_called_with(self.cache_manager.data)

    

    def test_check_dataset_name__exists(self):
        """
        Test if a name string exists in the caches's dictionary.
        """
        # sample data
        sample_name = "cifar10"

        # check if name1 exists in the dictionary
        res = self.cache_manager.check_dataset_name(sample_name)

        # check if it was a successful query
        self.assertTrue(res, 'Should have given True')


    def test_check_dataset_name__dont_exist(self):
        """
        Test if a name string exists in the caches's dictionary.
        """
        # sample data
        sample_name = "cifar1000"

         # check if name1 exists in the dictionary
        res = self.cache_manager.check_dataset_name(sample_name)

        # check if it was a successful query
        self.assertFalse(res, 'Should have given false')


    def test_add_data__valid_dataset(self):
        """
        Test adding/appending data of a new dataset/category
        """
        # sample data
        name = 'cifar10'
        old_info = self.sample_cache_data['dataset'][name]['tasks']
        new_task = {'data2':'val2'}
        old_info.update(new_task)
        new_info = {'tasks': new_task}
        reference_result = {'tasks': old_info}
        is_append = True

        # append data to the old data
        self.cache_manager.add_data(name, new_info, is_append)

        # check if the appended data matches the reference output
        self.assertEqual(self.cache_manager.data['dataset'][name]['tasks'], reference_result['tasks'], \
                        'Dictionaries should be equal')


    def test_add_data__nonexisting_dataset(self):
        """
        Test adding/appending data of a new dataset/category
        """
        # sample data
        name = 'cifar1000'
        new_info = {'task': {'data2':'val2'}}
        is_append = False

        # append data to the old data (should raise an exception)
        self.cache_manager.add_data(name, new_info, is_append)

        # check if the data was added to the dictionary
        self.assertEqual(self.cache_manager.data['dataset'][name], new_info)


    @patch('__main__.CacheManager.get_dataset_storage_paths')
    @patch('__main__.CacheManager.delete_dataset_cache')
    @patch('__main__.CacheManager.os_remove')
    def test_delete_dataset_cache__valid_dataset__keep_data_dir(self, mock_os, mock_delete, mock_paths):
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


    @patch('__main__.CacheManager.get_dataset_storage_paths')
    @patch('__main__.CacheManager.delete_dataset_cache')
    @patch('__main__.CacheManager.os_remove')
    def test_delete_dataset_data__valid_dataset__delete_data_dir(self, mock_os, mock_delete, mock_paths):
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


    def test_is_empty(self):
        """
        Test to see if the cache data has any dataset.
        """
        self.assertTrue(self.cache_manager.is_empty())


    def test_exists_dataset__valid_dataset(self):
        """
        Test checking if a dataset+task exists.
        """
        # sample data
        sample_name = 'cifar10'

        # check if the dataset name exists
        res = self.cache_manager.exists_dataset(sample_name)

        # validate output result
        self.assertTrue(res, 'Should be True')

    def test_exists_dataset__invalid_dataset(self):
        """
        Test checking if a dataset+task exists.
        """
        # sample data
        sample_name = 'cifar1000'

        # check if the dataset name exists
        res = self.cache_manager.exists_dataset(sample_name)

        # validate output result
        self.assertFalse(res, 'Should be False')


    def test_exists_task__valid_dataset_valid_task(self):
        """
        Test checking if a dataset+task exists in the cache file.
        """
        # sample data
        name = 'cifar10'
        task = 'default'

        # check if the task exists for this dataset
        res = self.cache_manager.exists_task(name, task)

        # validate output result
        self.assertTrue(res, 'Should be True')


    def test_exists_task__valid_dataset_invalid_task(self):
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


    def test_get_dataset_storage_paths__valid_dataset(self):
        """
        Test get the cache/data paths for a existing dataset.
        """
        # dataset name
        name = 'cifar10'
        reference_dirs = {
            "data_dir": self.sample_cache_data['dataset'][name]['data_dir'],
            "cache_dir": self.sample_cache_data['dataset'][name]['cache_dir']
        }

        # get path
        res = self.cache_manager.get_dataset_storage_paths(name)

        # check if the paths are the same
        self.assertEqual(res['data_dir'], reference_dirs['data_dir'], 'data_dir')
        self.assertEqual(res['cache_dir'], reference_dirs['cache_dir'], 'cache_dir')


    @patch('__main__.CacheManager.read_data_cache')
    def test_get_dataset_storage_paths__invalid_dataset(self, mock_read):
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


    def test_get_cache_path__valid_dataset_valid_task(self):
        """
        Test fetching the cache path of a specific task.
        """
        # sample data
        name = 'cifar10'
        task = 'default'
        reference_data = self.cache_manager.data['dataset'][name]['tasks'][task]

        # fetch cache path
        res = self.cache_manager.get_cache_path(name, task)

        # validate the output result
        self.assertEqual(res, reference_data, 'task: {}'.format(task))



    def test_get_cache_path__valid_dataset_invalid_task(self):
        """
        Test fetching the cache path of a specific (invalid) task.
        """
        # sample data
        sample_name = 'cifar10'
        sample_task = 'detect'
        sample_data = self.cache_manager.data

        # fetch cache path (should raise an exception)
        with self.assertRaises(KeyError):
            self.cache_manager.get_cache_path(sample_name, sample_task)


    def test_add_keywords_category(self):
        """
        Test adding keywords of a dataset.
        """
        # sample data
        name = 'cifar10'
        keywords = ['custom']

        # add keywords to the dictionary
        self.cache_manager.add_keywords(name, keywords)

        # check if the keywords were introduced correctly
        self.assertTrue(any(self.cache_manager.data['category'][keywords[0]]))
        self.assertEqual(self.cache_manager.data['category'][keywords[0]], [name], 'equal string')


    @patch('__main__.CacheManager.add_data')
    @patch('__main__.CacheManager.add_keywords')
    @patch('__main__.CacheManager.write_data_cache')
    def test_update_cache__not_existing_dataset(self, mock_write, mock_keywords, mock_add):
        """
        Test updating the cache with new data.
        """
        # sample data
        new_name = 'cifar1000'
        new_data_dir = 'dir1/cifar1000/data'
        new_cache_dir = 'dir1/cifar1000/cache'
        new_cache_tasks = {}
        new_keywords = []
        reference_new_info = {
            "data_dir": new_data_dir,
            "cache_dir": new_cache_dir,
            "tasks": new_cache_tasks,
            "keywords": new_keywords
        }
        is_append = False

        # update data
        self.cache_manager.update(new_name, new_data_dir, new_cache_dir, \
                                  new_cache_tasks, new_keywords, is_append)

        # check if functions were called
        self.assertTrue(mock_add.called, 'Mock function: CacheManager.add_data')
        self.assertTrue(mock_keywords, 'Mock function: CacheManager.add_keywords')
        self.assertTrue(mock_write.called, 'Mock function: CacheManager.write_data_cache')

        # check if the functions were called with the correct parameters
        mock_add.assert_called_with(new_name, reference_new_info, is_append)
        mock_keywords.assert_called_with(new_name, new_keywords)
        mock_write.assert_called_with(self.cache_manager.data)


    @patch('__main__.CacheManager.delete_dataset_cache')
    def test_delete_cache_all(self, mock_delete):
        """
        Test deleting all datasets from the cache.
        """
        self.cache_manager.delete_cache_all()

        self.assertTrue(mock_delete.called, 'Call mock function: CacheManager.delete_dataset_cache')

        self.assertFalse(any(self.cache_manager.data['dataset']))
        self.assertFalse(any(self.cache_manager.data['category']))

#----------------
# Run Test Suite
#----------------

def main(level=1):
    """Main function to start testing"""
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
