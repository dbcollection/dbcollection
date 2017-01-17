#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Class to manage the dbcollection cache file
"""


import sys
import os
from os.path import expanduser
import json


class CacheManager:
    """ Class to manage the dbcollection cache data """

    def __init__(self):
        """
        Initialize class.
        """

        # cache directory path
        self.cache_path = expanduser("~")

        # cache file path
        if sys.platform == 'win32':
            self.cache_fname = self.cache_path + '\\' + 'dbcollection.json'
        else:
            self.cache_fname = self.cache_path + '/' + 'dbcollection.json'

        # create cache file to disk (if it does not exist)
        if not os.path.exists(self.cache_fname):
            self.create_cache_file_disk(self.cache_fname)


    def read_data_cache(self):
        """
        Load data from the dbcollection cache file.
        """
        # open file + load data
        with open(self.cache_fname, 'r') as json_data:
            data = json.load(json_data)

        return data


    def write_data_cache(self, data):
        """
        Write data to the dbcollection cache file.
        """
        with open(self.cache_fname, 'w') as file_cache:
            json.dump(data, file_cache, ensure_ascii=False)


    def create_cache_file_disk(self, fname):
        """
        Initialize the dbcollection cache file with empty data.
        """
        self.write_data_cache({})


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
        if name in data['dataset'].keys():
            return True
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
            return {}
