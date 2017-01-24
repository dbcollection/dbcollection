#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
Class to manage the dbcollection cache file
"""


import os
import json


class CacheManager:
    """ Class to manage the dbcollection cache data """

    def __init__(self):
        """
        Initialize class.
        """

        # setup cache paths
        self.setup_paths()

        # create cache file to disk (if it does not exist)
        if not os.path.exists(self.cache_fname):
            self.create_cache_file_disk(self.cache_fname)


    def setup_paths(self):
        """
        Setup the cache/data directories for storing the cache file.

        This returns two paths for the default cache directory for storing the cache data,
        and the filepath for the dbcollection.json file where the metadata for all datasets
        is stored.

        This paths were designed to work on windows, linx, mac, etc.
        """
         # cache directory path (should work for all platforms)
        self.cache_path = os.path.expanduser("~")

        # cache file path
        self.cache_fname = os.path.join(self.cache_path, 'dbcollection.json')

        # default paths
        self.default_cache_path = os.path.join(self.cache_path, 'dbcollection')
        self.default_data_path = self.default_cache_path


    def read_data_cache(self):
        """
        Load data from the dbcollection cache file.
        """
        # check if file exists
        if os.path.exists(self.cache_fname):
            # open file + load data
            with open(self.cache_fname, 'r') as json_data:
                data = json.load(json_data)
            return data
        else:
            return self.empty_data()


    def write_data_cache(self, data, fname=None):
        """
        Write data to the dbcollection cache file.
        """
        filename = fname or self.cache_fname
        with open(filename, 'w') as file_cache:
            json.dump(data, file_cache, ensure_ascii=False)


    def empty_data(self):
        """
        Returns an empty template of the cache data structure
        """
        return {
            "info": {
                "default_cache_path": self.default_cache_path,
		        "default_data_path": self.default_data_path
            },
            "dataset": {}
        }


    def create_cache_file_disk(self, fname=None):
        """
        Initialize the dbcollection cache file with empty data.
        """
        self.write_data_cache(self.empty_data(), fname)


    def delete_cache_file_disk(self, fname):
        """
        Deletes the cache file from disk.
        """
        if os.path.exists(fname):
            os.remove(fname)


    def check_dataset_name(self, data, name):
        """
        Check if the dataset name exists in the available dictionary keys.
        """
        if any(data):
            if name in data['dataset'].keys():
                return True
            else:
                return False
        else:
            return False


    def get_data_from_field(self, data, name, field):
        """
        Get data from a field of a dataset.
        """
        return data['dataset'][name][field]


    def get_dataset_storage_paths(self, name):
        """
        Get dataset save/load path.
        """
        # load data from the cache file
        data = self.read_data_cache()

        # check if the dataset exists in the cache file
        is_dataset = self.check_dataset_name(data, name)

        # filter data for the input dataset name
        if is_dataset:
            return {
                "cache_path": self.get_data_from_field(data, name, "cache_path"),
                "data_path": self.get_data_from_field(data, name, "data_path")
            }
        else:
            return {
                "cache_path": os.path.join(self.default_cache_path, name, 'cache'),
                "data_path": os.path.join(self.default_data_path, name, 'data')
            }
