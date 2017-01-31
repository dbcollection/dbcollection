"""
Class to manage the dbcollection.json cache file.
"""


import os
import errno
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

        Parameters
        ----------
            None

        Returns
        -------
            None

        Raises
        ------
            None
        """
         # cache directory path (should work for all platforms)
        self.cache_dir = os.path.expanduser("~")

        # cache file path
        self.cache_fname = os.path.join(self.cache_dir, '.dbcollection.json')

        # default paths
        self.default_cache_dir = os.path.join(self.cache_dir, 'dbcollection')
        self.default_data_dir = self.default_cache_dir


    def read_data_cache_file(self):
        """
        Read the cache file data to memory.

        Parameters
        ----------
            None

        Returns
        -------
        dict
            Cache's data structure.

        Raises
        ------
        IOError
            If the file cannot be opened.
        """
        try:
            with open(self.cache_fname, 'r') as json_data:
                return json.load(json_data)
        except IOError:
            raise


    def read_data_cache(self):
        """
        Load data from the dbcollection cache file.

        Parameters
        ----------
            None

        Returns
        -------
        dict
            Cache's data structure.

        Raises
        ------
            None
        """
        # check if file exists
        if os.path.exists(self.cache_fname):
            return self.read_data_cache_file()
        else:
            return self.empty_data()


    def write_data_cache(self, data, fname=None):
        """
        Write data to the dbcollection cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.
        fname : str
            File path+name to store the cache data.

        Returns
        -------
            None

        Raises
        ------
        IOError
            If the file cannot be opened.
        """
        filename = fname or self.cache_fname
        try:
            with open(filename, 'w') as file_cache:
                json.dump(data, file_cache, ensure_ascii=False)
        except IOError:
            raise


    def empty_data(self):
        """
        Returns an empty template of the cache data structure.

        Parameters
        ----------
            None

        Returns
        -------
        dict
            Dummy data structure.

        Raises
        ------
            None
        """
        return {
            "info": {
                "default_cache_dir": self.default_cache_dir,
		        "default_data_dir": self.default_data_dir
            },
            "dataset": {}
        }


    def create_cache_file_disk(self, fname=None):
        """
        Initialize the dbcollection cache file with empty data.
        """
        self.write_data_cache(self.empty_data(), fname)


    def os_remove(self, fname):
        """
        Remove a file/directory from disk.

        Parameters
        ----------
        fname : str
            File name+path on disk.

        Returns
        -------
            None

        Raises
        ------
        OSError
            If the file does not exist.
        """
        try:
            os.remove(fname)
        except OSError as err:
            if err.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise


    def delete_entry(self, category, name):
        """
        Delete a dataset entry from a category dictionary.

        Parameters
        ----------
        category : str
            Category's name.
        namefname : str
            Dataset's name.

        Returns
        -------
            None

        Raises
        ------
        KeyError
            If the category or the dataset name don't exist.
        """
        try:
            self.data['dataset'][category].pop(name)
        except KeyError:
            raise


    def delete_dataset_cache(self, name):
        """
        Delete the cache data from disk of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        # category name
        category = self.get_category(name)

        # get cache dir path
        cache_dir_path = self.get_data_from_field(name, 'cache_dir')
        #cache_dir_path = self.data['dataset'][category][name]['cache_dir']

        # remove cache dir
        self.os_remove(cache_dir_path)

        # remove entry from the data
        self.delete_entry(category, name)

        # write updated data to file
        self.write_data_cache(self.data)


    def check_dataset_name(self, name):
        """
        Check if the dataset name exists in the available dictionary keys.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        bool
            If the dataset exists, returns True.
            Else return False.

        Raises
        ------
        KeyError
            If the dataset name doesn't exist.
        """
        try:
            return name in self.data['dataset'][self.get_category(name)].keys()
        except KeyError:
            return False


    def get_data_from_field(self, name, field):
        """
        Get data from a field of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        field : str
            Field name identifier.

        Returns
        -------
        dict
            Cache's data structure.

        Raises
        ------
        KeyError
            If the dataset name doesn't exist.
        """
        try:
            return self.data['dataset'][self.get_category(name)][name][field]
        except KeyError:
            raise


    def change_field(self, name, field, val):
        """
        Change the data of a field of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        field : str
            Field name identifier.
        val : <any>
            New value.

        Returns
        -------
        dict
            Cache's data structure.

        Raises
        ------
        KeyError
            If the dataset/field name doesn't exist.
        """
        try:
            self.data['dataset'][self.get_category(name)][name][field] = val
        except KeyError:
            raise


    def add_data(self, category, name, new_info):
        """
        Adds/appends a new category/dataset to the cache file.

        Parameters
        ----------
        category : str
            Name of the category.
        name : str
            Name of the dataset.
        new_info : dict
            New data.

        Returns
        -------
            None

        Raises
        ------
            None
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


    def delete_dataset(self, name, delete_data=False):
        """
        Delete a dataset from disk/cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        delete_data : bool
            Flag indicating if the data's directory has to be deleted (or skip it).

        Returns
        -------
            None

        Raises
        ------
            None
        """
        dset_paths = self.get_dataset_storage_paths(name)

        # remove cache directory
        self.delete_dataset_cache(name)

        # delete data from disk
        if delete_data is True:
            self.os_remove(dset_paths['data_dir'])


    def get_category(self, name):
        """
        Returns the dataset category name of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        str
            Returns the category name if found, else returns None.

        Raises
        ------
            None
        """
        for category in self.data['dataset'].keys():
            if name in self.data['dataset'][category].keys():
                return category
        return None


    def exists_dataset(self, name):
        """
        Check if a dataset exists for loading.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        bool
            Return true if the category exists, else return False.

        Raises
        ------
        KeyError
            If the category name does not exist in the dictionary.
        """
        # check if the dataset exists in the cache file
        try:
            return name in self.data['dataset'][self.get_category(name)]
        except KeyError:
            return False


    def exists(self, name, task):
        """
        Check if a dataset+task exists in the cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.
        task : str
            Name of the task.

        Returns
        -------
        bool
            Return true if the task exists, else return False.

        Raises
        ------
        KeyError
            If the task does not exist in the dictionary.
        """
        try:
            return task in self.data['dataset'][self.get_category(name)][name]['cache_files']
        except KeyError:
            return False


    def get_dataset_storage_paths(self, name):
        """
        Get dataset save/load path.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        dict
            Dataset's data+cache paths.

        Raises
        ------
            None
        """
        if self.exists_dataset(name):
            return {
                "cache_dir": self.get_data_from_field(name, "cache_dir"),
                "data_dir": self.get_data_from_field(name, "data_dir")
            }
        else:
            return {
                "cache_dir": os.path.join(self.default_cache_dir, name, 'cache'),
                "data_dir": os.path.join(self.default_data_dir, name, 'data')
            }


    def get_dataset_data(self, name):
        """
        Fetches the cache data of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        dict
            Cache data structure of a particular dataset.

        Raises
        ------
        KeyError
            If the dataset name does not exist in the dictionary.
        """
        try:
            return self.data['dataset'][self.get_category(name)][name]
        except KeyError:
            raise Exception('Dataset '+str(name)+' does not exist in the cache file.')


    def get_cache_path(self, name, task):
        """
        Return the cache path of a specific task.

        Parameters
        ----------
        name : str
            Name of the dataset.
        task : str
            Name of the task.

        Returns
        -------
        str
            Cache name+path of a specific task.

        Raises
        ------
            None
        """
        # fetch cache data of the dataset
        cache_data = self.get_dataset_data(name)

        # fetch the path of the metadata file for this task
        cache_path = cache_data['cache_files'][task]

        return cache_path


    def update(self, name, category, data_dir, cache_dir, cache_info):
        """
        Update the cache file with new/updated data for a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        category : str
            Name of the category.
        data_dir : str
            Dataset directory on disk where all data is stored.
        cache_dir : str
            Cache's directory on disk where the metadata files are store.
        cache_info : dict
            New task + path information.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        # build info dictionary
        new_info_dict = {
            "data_dir": data_dir,
            "cache_dir": cache_dir,
            "cache_files": cache_info
        }

        # update data with the new info
        self.add_data(category, name, new_info_dict)

        # write to file
        self.write_data_cache(self.data)

