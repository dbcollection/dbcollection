"""
Class to manage the dbcollection.json cache file.
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

        # create cache file (if it does not exist)
        if not os.path.exists(self.cache_fname):
            self.create_cache_file_disk(self.cache_fname)

        # load cache data file
        self.data = self.read_data_cache()


    def setup_paths(self):
        """Setup the cache/data directories for storing the cache file.

        This returns two paths for the default cache directory for storing the cache data,
        and the filepath for the dbcollection.json file where the metadata for all datasets
        is stored.

        This paths were designed to work on windows, linx, mac, etc.
        """
         # cache directory path (should work for all platforms)
        self.cache_path = os.path.expanduser("~")

        # cache file path
        self.cache_fname = os.path.join(self.cache_path, '.dbcollection.json')

        # default paths
        self.default_cache_path = os.path.join(self.cache_path, 'dbcollection')
        self.default_data_path = self.default_cache_path


    def read_data_cache_file(self):
        """
        Read cache file to memory.
        """
        try:
            with open(self.cache_fname, 'r') as json_data:
                data = json.load(json_data)
            return data
        except IOError:
            raise


    def read_data_cache(self):
        """
        Load data from the dbcollection cache file.
        """
        # check if file exists
        if os.path.exists(self.cache_fname):
            # open file + load data
            return self.read_data_cache_file()
        else:
            return self.empty_data()


    def write_data_cache(self, data, fname=None):
        """
        Write data to the dbcollection cache file.
        """
        filename = fname or self.cache_fname
        try:
            with open(filename, 'w') as file_cache:
                json.dump(data, file_cache, ensure_ascii=False)
        except IOError:
            raise


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


    def check_dataset_name(self, name):
        """
        Check if the dataset name exists in the available dictionary keys.
        """
        try:
            return name in self.data['dataset'].keys()
        except KeyError:
            return False


    def get_data_from_field(self, name, field):
        """
        Get data from a field of a dataset.
        """
        category = self.get_category(name)
        try:
            return self.data['dataset'][category][name][field]
        except KeyError:
            raise


    def add_data(self, category, name, new_info):
        """
        Adds/appends a new category/dataset to the data file.
        """
        # check if category already exists
        if category in self.data['dataset'].keys():
            # check if the dataset already exists
            if name in self.data['dataset'][category].keys():
                # update the old info with the new data
                old_info = self.data['dataset'][category][name]
                cache_files = old_info['cached_files']
                cache_files.update(new_info['cached_files'])
                new_info['cached_files'] = cache_files
        else:
            self.data['dataset'][category] = {}

        # add the new info to the dictionary
        self.data['dataset'][category][name] = new_info


    def get_category(self, name):
        """
        Returns the dataset category name of a dataset.
        """
        for category in self.data['dataset'].keys():
            if name in self.data['dataset'][category].keys():
                return category
        return None

    def exists_dataset(self, name):
        """
        Check if a dataset exists for loading.
        """
        # check if the dataset exists in the cache file
        try:
            return name in self.data['dataset'][self.get_category(name)]
        except KeyError:
            return False


    def exists(self, name, task):
        """
        Check if a dataset+task exists in the cache file.
        """
        try:
            return task in self.data['dataset'][self.get_category(name)][name]['cache_files']
        except KeyError:
            return False


    def get_dataset_storage_paths(self, name):
        """
        Get dataset save/load path.
        """
        if self.exists_dataset(name):
            return {
                "cache_path": self.get_data_from_field(name, "cache_path"),
                "data_path": self.get_data_from_field(name, "data_path")
            }
        else:
            return {
                "cache_path": os.path.join(self.default_cache_path, name, 'cache'),
                "data_path": os.path.join(self.default_data_path, name, 'data')
            }


    def get_dataset_data(self, name):
        """
        Fetches the cache data of a dataset.
        """
        try:
            return self.data['dataset'][self.get_category(name)][name]
        except KeyError:
            raise Exception('Dataset '+str(name)+' does not exist in the cache file.')


    def get_cache_path(self, name, task):
        """
        Return the cache path of a specific task.
        """
        # fetch cache data of the dataset
        cache_data = self.get_dataset_data(name)

        # fetch the path of the metadata file for this task
        cache_path = cache_data['cache_files'][task]

        return cache_path


    def update(self, name, category, data_path, cache_info):
        """
        Update the cache file with new/updated data for a dataset.
        """
        # build info dictionary
        new_info_dict = {
            "data_path": data_path,
            "cache_path": os.path.join(self.default_cache_path, name),
            "cache_files": cache_info
        }

        # update data with the new info
        self.add_data(category, name, new_info_dict)

        # write to file
        self.write_data_cache(self.data)

