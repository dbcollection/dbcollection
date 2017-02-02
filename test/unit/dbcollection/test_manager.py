#!/usr/bin/env python3


"""
dbcollection/manager.py unit testing.
"""

import os
import sys

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
from dbcollection import manager


#-----------------------
# Unit Test definitions
#-----------------------

class ManagerTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        # sample data
        self.default_cache_dir = 'dir1'
        self.default_data_dir = 'dir1'
        self.sample_name = 'cifar10'
        self.sample_category = 'image_processing'
        self.sample_data_path = 'dir1/cifar10/data'
        self.sample_cache_path = 'dir1/cifar10/cache'
        self.sample_cache_file_path = os.path.join(self.sample_cache_path, 'class.h5')
        self.sample_task = 'default'

        # common data structure used for these tests
        self.sample_dict = {
            'info': {},
            'dataset':{
                self.sample_category: {
                    self.sample_name : {
                        'data_dir': self.sample_data_path,
                        'cache_dir': self.sample_cache_path,
                        'task': {
                            'default': self.sample_cache_file_path
                        }
                    }
                }
            }
        }


    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.CacheManager.exists_task', return_value=True)
    @patch('__main__.manager.CacheManager.get_cache_path', return_value=True)
    @patch('__main__.manager.CacheManager.get_dataset_storage_paths')
    @patch('__main__.manager.DatasetLoader', return_value=True)
    @patch('__main__.os.path.exists', return_value=True)
    def test_load__existing_dataset(self, mock_path, mock_loader, mock_get_paths, mock_get_cache, mock_exists, mock_cache):
        """
        Test fetching a dataset Loader of a non-existing dataset (requried download).
        """
        # sample data
        sample_name = self.sample_name
        #sample_category = self.sample_category
        sample_data_path = self.sample_data_path
        #sample_cache_path = self.sample_cache_path
        #sample_cache_file_path = self.sample_cache_file_path
        sample_save_name = None
        sample_task = self.sample_task
        sample_download = False
        sample_verbose = False
        sample_organize_list = None
        sample_select = None
        sample_filter = None

        # mock function values
        mock_cache.return_value = self.sample_dict
        mock_get_paths.return_value = {'data_dir':'str1'}

        # execute the loading fun
        res = manager.load(sample_name, sample_data_path, sample_save_name, \
                         sample_task, sample_download, sample_verbose, \
                         sample_organize_list, sample_select, sample_filter)

        # check if a loader was returned
        self.assertTrue(res, 'Should have returned a True value')

        # check if the mocked functions were correctly called
        self.assertTrue(mock_path.called, 'Should have been called')
        self.assertTrue(mock_exists.called, 'Should have been called')
        self.assertTrue(mock_get_cache.called, 'Should have been called')
        self.assertTrue(mock_get_paths.called, 'Should have been called')

        # check if the functions were called with the correct parameters
        mock_exists.assert_called_with(sample_name, sample_task)
        mock_get_cache.assert_called_with(sample_name, sample_task)
        mock_get_paths.assert_called_with(sample_name)


    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.CacheManager.exists_task', return_value=False)
    @patch('__main__.manager.CacheManager.get_cache_path', return_value=True)
    @patch('__main__.manager.CacheManager.get_dataset_storage_paths')
    @patch('__main__.manager.dataset.download')
    @patch('__main__.manager.dataset.process')
    @patch('__main__.manager.DatasetLoader', return_value=True)
    @patch('__main__.os.path.exists', return_value=True)
    def test_load__non_existing_dataset__download_process(self, mock_path, mock_loader, mock_process, mock_download, \
                                                          mock_get_paths, mock_get_cache, mock_exists, mock_read_cache):
        """
        Test fetching a dataset Loader of a non-existing dataset (requried download).
        """
        # sample data
        sample_name = self.sample_name
        sample_category = self.sample_category
        sample_data_dir = self.sample_data_path
        sample_cache_path = self.sample_cache_path
        sample_default_cache_path = os.path.join(os.path.expanduser("~"), 'dbcollection')
        sample_save_name = None
        sample_task = self.sample_task
        sample_download = True
        sample_verbose = False
        sample_organize_list = None
        sample_select = None
        sample_filter = None
        sample_cache_info = {
            'data_dir' : sample_data_dir,
            'cache_dir' : sample_cache_path,
            'task' : {sample_task:'val'},
            'category' : sample_category
        }

        # mock function values
        mock_read_cache.return_value = self.sample_dict
        mock_get_paths.return_value = {'data_dir':'str1'}
        mock_process.return_value = sample_cache_info

        # execute the loading fun
        res = manager.load(sample_name, sample_data_dir, sample_save_name, \
                         sample_task, sample_download, sample_verbose, \
                         sample_organize_list, sample_select, sample_filter)

        # check if a loader was returned
        self.assertTrue(res, 'Should have returned a True value')

        # check if the mocked functions were correctly called
        self.assertTrue(mock_path.called, 'Should have been called')
        self.assertTrue(mock_exists.called, 'Should have been called')
        self.assertTrue(mock_get_cache.called, 'Should have been called')
        self.assertTrue(mock_get_paths.called, 'Should have been called')
        self.assertTrue(mock_process.called, 'Should have been called')
        self.assertTrue(mock_download.called, 'Should have been called')


        # check if the functions were called with the correct parameters
        mock_exists.assert_called_with(sample_name, sample_task)
        mock_get_cache.assert_called_with(sample_name, sample_task)
        mock_get_paths.assert_called_with(sample_name)
        mock_download.assert_called_with(sample_name, sample_data_dir, sample_verbose)
        mock_process.assert_called_with(sample_name, sample_data_dir, sample_default_cache_path, sample_verbose)



    @patch('__main__.manager.CacheManager.update', return_value=True)
    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.os.path.exists', return_value=True)
    def test_add__custom_dataset__to_cache(self, mock_path, mock_cache, mock_update):
        """
        Test adding a custom dataset to the cache file info.
        """
        # sample data
        sample_dic = self.sample_dict
        sample_new_name = 'cifar1000'
        sample_data_dir = 'dir1/cifar1000/data'
        sample_cache_dir = 'dir1/cifar1000/cache'
        sample_cache_file_path = os.path.join(sample_cache_dir,'class.h5')
        sample_task = 'default'

        # mock function values
        mock_cache.return_value = self.sample_dict

        # add a custom dataset
        manager.add(sample_new_name, sample_data_dir, sample_cache_file_path, sample_task)

        # test that the update function was called
        self.assertTrue(mock_update.called, "Failed to update the cache file.")

        # check if the function was called with the right parameters
        mock_update.assert_called_with(sample_new_name, 'custom', sample_data_dir, \
                                       sample_cache_dir, {sample_task:sample_cache_file_path})


    @patch('__main__.os.path.exists', return_value=True)
    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.CacheManager.exists_dataset')
    @patch('__main__.manager.CacheManager.delete_dataset')
    def test_delete__existing_dataset(self, mock_delete, mock_exists, mock_cache, mock_path):
        """
        Test deleting a dataset from disk.
        """
        # sample data
        sample_name = self.sample_name

        # mock function return value
        mock_cache.return_value = self.sample_dict

        # do dataset deletion
        manager.delete(sample_name)

        # check if functions were called successfully
        self.assertTrue(mock_exists.called, 'function not called')
        self.assertTrue(mock_delete.called, 'function not called')

        # check if the function was called with the right parameters
        mock_delete.assert_called_with(sample_name, True)


    @patch('__main__.os.path.exists', return_value=True)
    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.CacheManager.exists_dataset')
    @patch('__main__.manager.CacheManager.delete_dataset')
    def test_reset__dataset_metadata__from_disk_cache(self, mock_delete, mock_exists, mock_cache, mock_path):
        """
        Test removing all metadata files and cache information from the disk/cache info.
        """
        # sample data
        sample_name = self.sample_name

        # mock function return value
        mock_cache.return_value = self.sample_dict

        # do dataset deletion
        manager.reset(sample_name)

        # check if functions were called successfully
        self.assertTrue(mock_exists.called, 'function not called')
        self.assertTrue(mock_delete.called, 'function not called')

        # check if the function was called with the right parameters
        mock_delete.assert_called_with(sample_name, False)


    @patch('__main__.os.path.exists', return_value=True)
    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.CacheManager.exists_dataset')
    @patch('__main__.manager.CacheManager.change_field')
    def test_config_cache(self, mock_change, mock_exists, mock_cache, mock_path):
        """
        Test configurating the cache file info.
        """
        # sample data
        sample_name = self.sample_name
        sample_data_field = 'data_dir'
        sample_new_data_dir = 'data/newdir/'
        sample_field = {sample_data_field : sample_new_data_dir}
        sample_cache_dir_default = None
        sample_data_dir_default = None


        # mock function return value
        mock_cache.return_value = self.sample_dict

        # configure the cache
        manager.config(sample_name, sample_field, sample_cache_dir_default, sample_data_dir_default)

        # check if functions were called successfully
        self.assertTrue(mock_exists.called, 'function not called')
        self.assertTrue(mock_change.called, 'function not called')

        # check if the function was called with the right parameters
        mock_exists.assert_called_with(sample_name)
        mock_change.assert_called_with(sample_name, sample_data_field, sample_new_data_dir)


    @patch('__main__.manager.CacheManager.read_data_cache')
    @patch('__main__.manager.dataset.download')
    @patch('__main__.os.path.exists', return_value=True)
    def test_download_dataset(self, mock_exists, mock_download, mock_cache):
        """
        Test downloading a dataset to disk.
        """
        #sample data
        sample_name = self.sample_name
        sample_data_path = 'data/store'
        sample_cache_save_dir = '/home/mf/dbcollection'
        sample_verbose = True

        # mock function return value
        mock_cache.return_value = self.sample_dict

        # download a dataset
        manager.download(sample_name, sample_data_path, sample_verbose)

        # check if functions were called successfully
        self.assertTrue(mock_download.called, 'function not called')

        # check if the function was called with the right parameters
        mock_download.assert_called_with(sample_name, sample_data_path, sample_cache_save_dir, sample_verbose)


    @patch('__main__.os.path.exists', return_value=True)
    @patch('__main__.manager.CacheManager.read_data_cache')
    def test_query_cache(self, mock_cache, mock_path):
        """
        Test performing some queries from the cache info.
        """
        # sample data
        sample_query_pattern = 'cifar10'
        sample_query_output = self.sample_dict['dataset']['image_processing']['cifar10']

        # mock function return value
        mock_cache.return_value = self.sample_dict

        # query the data with a dataset name
        res = manager.query(sample_query_pattern)

        # check if the output is the same as the predicted query data
        self.assertEqual(res, sample_query_output, 'Dictionaries should be the same')


    def test_list(self):
        """
        Test printing all information of the cache info.
        """
        pass



#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
