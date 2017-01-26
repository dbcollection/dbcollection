"""
dbcollection/cache.py unit testing.
"""

# import data.py
import os
import sys

import unittest
from unittest import mock
from unittest.mock import patch, mock_open


dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', 'dbcollection'))
sys.path.append(lib_path)
import cache


#-----------------------
# Unit Test definitions
#-----------------------

class CacheManagerTest(unittest.TestCase):
    """
    Test class.
    """

    @patch('cache.CacheManager.create_cache_file_disk')
    def setUp(self, mock_file):
        """
        Initialize class.
        """
        # create class
        self.cache_manager = cache.CacheManager()

        # check if the object is of the same type
        self.assertIsInstance(self.cache_manager, cache.CacheManager, 'Object is not of the same class')

        # create a sample cache data dictionary
        self.sample_cache_data = {
            "info":{
                "default_cache_path": "tmp/dir/",
                "default_data_path": "tmp/dir/",
            },
            "dataset":{
                "image_processing":{
                    "cifar10":{
                        "cache_path":"tmp/dir/",
                        "data_path":"tmp/dir/",
                        "task":{
                            "default":"file1.h5",
                            "classific":"file2.h5"
                        }
                    }
                }
            }
        }


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.load')
    def test_read_data_cache(self, mock_json):
        """
        Test loading data from the json file.
        """
        # sample json file
        json_sample = {"name":"data"}

        # mock json.load return value
        mock_json.return_value = json_sample

        # load data
        res = self.cache_manager.read_data_cache()

        # check if open was called with the correct parameters
        open.assert_called_with(self.cache_manager.cache_fname, 'r')

        # check if values match
        self.assertDictEqual(res, json_sample, 'Dictionaries should be equal')


    @patch('builtins.open', mock_open(read_data='1'))
    @patch('json.dump')
    def test_write_data_cache(self, mock_json):
        """
        Test write the dbcollection file.
        """
        # some data
        dic_sample = {"name1":"data1"}

        # fake write to a file
        self.cache_manager.write_data_cache(dic_sample)

        # check if open was called with the correct parameters
        open.assert_called_with(self.cache_manager.cache_fname, 'w')

        # check if the functions were mocked
        self.assertFalse(mock_json.dump.called, 'Failed to mock json.dump()')


    @patch('data.os.path')
    @patch('data.os.remove')
    def test_delete_cache_file(self, mock_os, mock_path):
        """
        Test delete the dbcollection file.
        """
        # set paths.exists to True
        mock_path.exists.return_value = True
        mock_os.remove = mock.Mock()

        # fake delete file
        self.cache_manager.delete_cache_file_disk('filename')

        # check if the function was correctly mocked
        self.assertFalse(mock_os.remove.called, 'Failed to mock os.remove()')



    def test_check_dataset_name(self):
        """
        Test if a name string exists in the caches's dictionary.
        """
        # sample data
        sample_data = {"dataset":{"name1":"val1"}}
        sample_name1 = "name1"
        sample_name2 = "name2"

        # check if name1 exists in the dictionary
        res1 = self.cache_manager.check_dataset_name(sample_data, sample_name1)

        # check if it was a successful query
        self.assertTrue(res1, 'Should have given True')

         # check if name1 exists in the dictionary
        res2 = self.cache_manager.check_dataset_name(sample_data, sample_name2)

        # check if it was a successful query
        self.assertFalse(res2, 'Should have given false')


    def test_get_data_from_field(self):
        """
        Test getting a field from cache data storage.
        """
        # sample data dictionary
        sample_data = self.sample_cache_data
        sample_name = 'cifar10'
        sample_field = "cache_path"
        sample_path = sample_data['dataset'][sample_name][sample_field]

        # get data from field
        res = self.cache_manager.get_data_from_field(sample_data, sample_name, sample_field)

        # check if name matches the result
        self.assertEqual(res, sample_path, 'Paths should be the same')


    @patch('cache.CacheManager.read_data_cache')
    def test_get_valid_dataset_storage_paths(self, mock_read):
        """
        Test get the cache/data paths for a existing dataset.
        """
        # dataset name
        sample_data = self.sample_cache_data
        sample_name = 'cifar10'
        sample_field_cache = "cache_path"
        sample_field_data = "data_path"
        sample_path_cache = sample_data['dataset'][sample_name][sample_field_cache]
        sample_path_data = sample_data['dataset'][sample_name][sample_field_data]
        
        # set custom return value for the mocked functions
        mock_read.return_value = self.sample_cache_data

        # get path
        res = self.cache_manager.get_dataset_storage_paths(sample_name)

        # check if the paths are the same
        self.assertEqual(res[sample_field_cache], sample_path_cache, 'Paths should be equal')
        self.assertEqual(res[sample_field_data], sample_path_data, 'Paths should be equal')


    @patch('cache.CacheManager.read_data_cache')
    def test_get_invalid_dataset_storage_paths(self, mock_read):
        """
        Test get the cache/data paths for an invalid dataset.
        """
        # dataset name
        sample_data = self.sample_cache_data
        sample_name = 'dataset'
        sample_field_cache = "cache_path"
        sample_field_data = "data_path"
        sample_path_cache = os.path.join(self.cache_manager.default_cache_path, sample_name, 'cache')
        sample_path_data = os.path.join(self.cache_manager.default_data_path, sample_name, 'data')

        # set custom return value for the mocked functions
        mock_read.return_value = self.sample_cache_data

        # get path
        res = self.cache_manager.get_dataset_storage_paths(sample_name)

        # check if the paths are the same
        self.assertEqual(res[sample_field_cache], sample_path_cache, 'Paths should be equal')
        self.assertEqual(res[sample_field_data], sample_path_data, 'Paths should be equal')



#----------------
# Run Test Suite
#----------------

def main(level=1):
    """Main function to start testing"""
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
