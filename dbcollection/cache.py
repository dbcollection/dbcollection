"""
Class to manage the dbcollection.json cache file.
"""


from __future__ import print_function
import os
import shutil
import errno
import json


class CacheManager:
    """ Class to manage the dbcollection cache data """

    def __init__(self):
        """Initialize class.

        Parameters
        ----------
            None
        """

        # setup cache paths
        self.setup_paths()

        # create cache file (if it does not exist)
        if not os.path.exists(self.cache_fname):
            print('Cache file not found. Generating the file: {}'.format(self.cache_fname))
            self.create_cache_file_disk(self.cache_fname)
            print('Done.')

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
        self.default_data_dir = os.path.join(self.default_cache_dir, 'data')


    def read_data_cache_file(self):
        """Read the cache file data to memory.

        Parameters
        ----------
            None

        Returns
        -------
        dict
            Data structure of the cache (file).

        Raises
        ------
        IOError
            If the file cannot be opened.
        """
        try:
            with open(self.cache_fname, 'r') as json_data:
                return json.load(json_data)
        except IOError:
            raise IOError('Unable to open file: ' + self.cache_fname)


    def read_data_cache(self):
        """Load data from the dbcollection cache file.

        Parameters
        ----------
            None

        Returns
        -------
        dict
            Data structure of the cache (file).

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
        """Write data to the dbcollection cache file.

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
            raise IOError('Unable to open file: ' + filename)


    def empty_data(self):
        """Returns an empty template of the cache data structure.

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
            "dataset": {},
            "category": {}
        }


    def create_cache_file_disk(self, fname=None):
        """Initialize the dbcollection cache file with empty data.

        Parameters
        ----------
        fname : str
            File name+path on disk.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        self.write_data_cache(self.empty_data(), fname)


    def os_remove(self, fname):
        """Remove a file/directory from disk.

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
            if os.path.isdir(fname):
                shutil.rmtree(fname, ignore_errors=True)
            else:
                os.remove(fname)
        except OSError as err:
            if err.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise OSError('Unable to remove: {}'.format(fname))


    def delete_entry(self, name):
        """Delete a dataset entry from a category dictionary.

        Parameters
        ----------
        name : str
            Dataset name.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        self.data['dataset'].pop(name)


    def delete_dataset_cache(self, name):
        """Delete the cache data from disk of a dataset.

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
        # get cache dir path
        cache_dir_path = os.path.join(self.default_cache_dir, name)

        # remove cache dir
        self.os_remove(cache_dir_path)

        # remove entry from the data
        self.delete_entry(name)

        # write updated data to file
        self.write_data_cache(self.data)


    def delete_cache_all(self):
        """Delete all datasets from cache.

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
        for name in self.data['dataset'].keys():
            self.delete_dataset_cache(name)

        # remove dataset names/categories from the list
        self.data['dataset'] = {}
        self.data['category'] = {}


    def check_dataset_name(self, name):
        """Check if the dataset name exists in the available dictionary keys.

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
            None
        """
        return name in self.data['dataset'].keys()


    def add_data(self, name, new_info, is_append=False):
        """Adds/appends a new category/dataset to the cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.
        new_info : dict
            New data.
        is_append : bool
            Appends the task cache data to existing ones.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        if is_append:
            if name in self.data['dataset']:
                self.data['dataset'][name]['tasks'].update(new_info['tasks'])
        self.data['dataset'][name] = new_info


    def delete_dataset(self, name, delete_data=False):
        """Delete a dataset from disk/cache.

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
        if delete_data:
            self.os_remove(dset_paths['data_dir'])


    def is_empty(self):
        """Checks if the cache data has any dataset.

        Parameters
        ----------
            None

        Returns
        -------
        bool
            True if it is empty.
            Otherwise, False.

        Raises
        ------
            None
        """
        return any(self.data['dataset'])


    def is_task(self, name, task):
        """Check if the task exists for the dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        task : str
            Name of the classification.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        try:
            return task in self.data['dataset'][name]['tasks'].keys()
        except expression as identifier:
            return False



    def exists_dataset(self, name):
        """Check if a dataset exists for loading.

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
            None
        """
        # check if the dataset exists in the cache file
        return name in self.data['dataset'].keys()


    def exists_task(self, name, task):
        """Check if a task of a dataset exists in the cache file.

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
            None
        """
        try:
            return task in self.data['dataset'][name]['tasks'].keys()
        except KeyError:
            return False


    def get_dataset_storage_paths(self, name):
        """Get dataset save/load path.

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
            data_dir = self.data['dataset'][name]["data_dir"]
        else:
            data_dir = os.path.join(self.default_data_dir, name, 'data')

        return {
            "data_dir": data_dir,
            "cache_dir": os.path.join(self.default_cache_dir, name)
        }


    def get_cache_path(self, name, task):
        """Return the cache path of the metadata file of a specific task.

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
        KeyError
            In case the dataset name
        """
        try:
            return self.data['dataset'][name]['tasks'][task]
        except KeyError:
            raise KeyError('Dataset name/task cache data is empty or does not exist: {}/{}'.format(name, task))


    def add_keywords(self, name, keywords):
        """Add keywords to the category dictionary for the dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        keywords : list
            Keyword categories of the dataset.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        if not isinstance(keywords, list):
            keywords = [keywords]

        for keyword in keywords:
            if keyword in self.data['category']:
                if not name in self.data['category'][keyword]:
                    self.data['category'][keyword].append(name)
            else:
                self.data['category'][keyword] = [name]


    def update(self, name, data_dir, cache_tasks, cache_keywords, is_append=True):
        """Update the cache file with new/updated data for a dataset.

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
        is_append : bool
            Overrides existing cache info data with new data.

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
            "tasks": cache_tasks,
            "keywords" : cache_keywords
        }

        # add/update data with the new info to the dataset dictionary
        self.add_data(name, new_info_dict, is_append)

        # add/update the keyword list of the category dictionary
        if any(cache_keywords):
            self.add_keywords(name, cache_keywords)

        # write to file
        self.write_data_cache(self.data)
