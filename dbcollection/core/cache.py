"""
Class to manage the dbcollection.json cache file.
"""


from __future__ import print_function
import os
import shutil
import json
import warnings
import pprint
from glob import glob

from dbcollection.utils import print_text_box


class CacheManager:
    """Manage dbcollection configurations and stores them inside a cache file stored in disk.

    Parameters
    ----------
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    is_test : bool
        Flag used for tests.
    cache_filename : str
        Cache file path + name.
    cache_dir : str
        Default directory to store all dataset's metadata files.
    download_dir : str
        Default save dir path for downloaded data.
    data : dict
        Cache contents.

    """

    def __init__(self):
        """Initializes the class."""
        self.manager = CacheDataManager()
        self.info = CacheManagerInfo(self.manager)
        self.dataset = CacheManagerDataset(self.manager)
        self.category = CacheManagerCategory(self.manager)


class CacheDataManager:
    """Cache's data write/read methods."""

    def __init__(self):
        """Initialize class."""
        self.cache_filename = self._get_cache_filename()
        self.data = self.read_data_cache()
        self._cache_dir = self._get_cache_dir()
        self.info = CacheManagerInfo(self.data["info"])

    def _get_cache_filename(self):
        """Return the cache file name + path."""
        home_dir = os.path.expanduser("~")
        filename = 'dbcollection.json'
        return os.path.join(home_dir, filename)

    def read_data_cache(self):
        """Loads data from the cache file.

        Returns
        -------
        dict
            Data containing information of all datasets and categories.

        """
        if os.path.exists(self.cache_filename):
            return self.read_data_cache_file()
        else:
            data = self._empty_data()
            self.write_data_cache(data)
            return data

    def read_data_cache_file(self):
        """Read the cache file data to memory.

        Returns
        -------
        dict
            Data structure of the cache (file).

        """
        with open(self.cache_filename, 'r') as json_data:
            return json.load(json_data)

    def _empty_data(self):
        """Returns an empty (dummy) template of the cache data structure."""
        return {
            "info": {
                "root_cache_dir": self._get_default_cache_dir(),
                "root_downloads_dir": self._get_default_downloads_dir(),
            },
            "dataset": {},
            "category": {}
        }

    def _get_default_cache_dir(self):
        """Returns the pre-defined path of the cache's root directory."""
        default_cache_dir = os.path.join(os.path.expanduser("~"), 'dbcollection')
        return default_cache_dir

    def _get_default_downloads_dir(self):
        """Returns the pre-defined path of the cache's downloads directory."""
        default_downloads_dir = os.path.join(self._get_default_cache_dir(), 'downloads')
        return default_downloads_dir

    def write_data_cache(self, data):
        """Writes data to the cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Raises
        ------
        IOError
            If the file cannot be opened.

        """
        assert data, 'Must input a non-empty dictionary.'
        with open(self.cache_filename, 'w') as file_cache:
            json.dump(data, file_cache, sort_keys=True, indent=4, ensure_ascii=False)
        self.data = data  # must assign the new data or risk problems

    def _set_cache_dir(self, path):
        """Set the root cache dir to store all metadata files"""
        assert path, 'Must input a directory path'
        self._cache_dir = path
        self.data['info']['root_cache_dir'] = self._cache_dir
        self.write_data_cache(self.data)

    def _get_cache_dir(self):
        """Get the root cache dir path."""
        return self.data['info']['root_cache_dir']

    cache_dir = property(_get_cache_dir, _set_cache_dir)

    def reset_cache_dir(self):
        """Reset the root cache dir path."""
        self._set_cache_dir(self._get_default_cache_dir())

    def _set_download_dir(self, path):
        """Set the root save dir path for downloaded data."""
        assert path, 'Must input a non-empty path.'
        self.data['info']['root_downloads_dir'] = path
        self.write_data_cache(self.data)

    def _get_download_dir(self):
        """Get the root save dir path."""
        return self.data['info']['root_downloads_dir']

    download_dir = property(_get_download_dir, _set_download_dir)

    def reset_download_dir(self):
        """Reset the root download dir path."""
        self._set_download_dir(self._get_default_downloads_dir())

    def reset_cache(self, force_reset=False):
        """Resets the cache file contents.

        Resets the cache file by removing all info about
        the datasets/categories/info from the cache file.
        Basically, it empties the cache contents.

        Parameters
        ----------
        force_reset : bool, optional
            Forces the cache to be reset (emptied) if True.

        Warning
        -------
        UserWarning
            If force_reset is False, display a warning to the user.

        """
        if force_reset:
            self.write_data_cache(self._empty_data())
        else:
            msg = 'All information about stored datasets will be lost if you proceed! ' + \
                  'Set \'force_reset=True\' to proceed with the reset of dbcollection.json.'
            warnings.warn(msg, UserWarning, stacklevel=2)

    def delete_cache(self, force_delete_file=False, force_delete_metadata=False):
        """Deletes the cache file and/or metadata dir from disk.

        Deletes the dbcollection.json file from disk if enabled.
        By default this option is disabled and a warning is displayed
        instead. Only by selecting the 'force_delete_file' option will
        the cache file be deleted.

        Also, there is an option to delete the cache's metadata files
        by selecting the 'force_delete_metadata'. This will remove the
        every dataset's metadata dir and its contents, but it will not
        delete the downloads directory.

        Parameters
        ----------
        force_delete_file : bool, optional
            Forces the cache file to be deleted if True.
        force_delete_metadata : bool, optional
            Forces the cache metadata to be deleted if True.

        Warning
        -------
        UserWarning
            If force_delete_file is False, display a warning to the user.

        """
        self._delete_cache_file(force_delete_file)
        if force_delete_metadata:
            self._delete_cache_metadata(force_delete_file)

    def _delete_cache_file(self, force_delete_file):
        """Deletes the cache file from disk."""
        if force_delete_file:
            if os.path.exists(self.cache_filename):
                os.remove(self.cache_filename)
        else:
            msg = 'All information about stored datasets will be lost if you proceed! ' + \
                  'Set \'force_delete_file=True\' to proceed with the deletion of ' + \
                  'dbcollection.json.'
            warnings.warn(msg, UserWarning, stacklevel=2)

    def _delete_cache_metadata(self, force_delete_file):
        """Deletes the cache metadata files from disk."""
        if force_delete_file:
            self._delete_dirs_datasets_in_cache_dir_except_downloads()
        else:
            msg = 'All metadata files of all datasets will be lost if you proceed! ' + \
                'Set both \'force_delete_file=True\' and \'force_delete_metadata=True\' ' + \
                'to proceed with the deletion of dbcollection.json and all metadata files.'
            warnings.warn(msg, UserWarning, stacklevel=2)

    def _delete_dirs_datasets_in_cache_dir_except_downloads(self):
        """Deletes all directories from the root cache dir except the downloads dir."""
        dirs = glob("{}/*/".format(self.cache_dir))
        try:
            dirs.remove(self.download_dir)
        except ValueError:
            pass
        for dir_path in dirs:
            shutil.rmtree(dir_path)

    def add_data(self, name, cache_dir, data_dir, tasks):
        """Adds a new dataset to the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        cache_dir : str
            Path of the dataset's metadata directory.
        data_dir : str
            Path of the dataset's data files.
        tasks : dict
            List of tasks.

        """
        assert name, "Must input a valid dataset name."
        assert cache_dir, "Must input a valid directory (cache_dir)."
        assert data_dir, "Must input a valid directory (data_dir)."
        assert tasks, "Must input a valid tasks."

        new_data = {
            "cache_dir": cache_dir,
            "data_dir": data_dir,
            "keywords": self._get_keywords_from_tasks(tasks),
            "tasks": tasks
        }
        self.data["dataset"][name] = new_data
        self.update_categories()
        self.write_data_cache(self.data)

    def _get_keywords_from_tasks(self, tasks):
        """Fetch a list of categories from a tasks' dictionary."""
        keywords = []
        for task in tasks:
            keywords.extend(tasks[task]["categories"])
        return tuple(sorted(set(keywords)))

    def update_categories(self):
        """Updates the category list of all categories."""
        categories = {}
        datasets = self.data['dataset']
        used_categories = self._get_list_categories_used(datasets)
        for category in used_categories:
            categories.update({
                category: self._get_datasets_tasks_by_category(datasets, category)
            })
        self.data["category"] = categories

    def _get_list_categories_used(self, datasets):
        """Returns a list of all categories available in the datasets data."""
        categories_used = []
        for dataset in datasets:
            categories_used.extend(datasets[dataset]['keywords'])
        return list(sorted(set(categories_used)))

    def _get_datasets_tasks_by_category(self, datasets, category):
        """Returns a list of all datasets and tasks that have the category name."""
        list_datasets_tasks = {}
        for dataset in datasets:
            list_datasets_tasks.update({
                dataset: self._get_tasks_by_category(datasets[dataset]["tasks"], category)
            })
        return list_datasets_tasks

    def _get_tasks_by_category(self, tasks, category):
        """Returns a list of tasks that contains the category name"""
        categories = self._get_keyword_list(tasks)
        return [c for c in categories if category in c]

    def _get_keyword_list(self, tasks):
        """Returns a list of unique task categories."""
        keywords = []
        for task in tasks:
            keywords.extend(tasks[task]["categories"])
        return list(set(keywords))

    def get_data(self, name):
        """Retrieves the data of a dataset from the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        dict
            Information about the dataset.

        """
        assert name, "Must input a valid dataset name."
        try:
            return self.data["dataset"][name]
        except KeyError:
            raise KeyError("The dataset \'{}\' does not exist in the cache.".format(name))

    def update_data(self, name, cache_dir=None, data_dir=None, tasks=None):
        """Updates the data of a dataset in the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        cache_dir : str, optional
            Path of the dataset's metadata directory.
        data_dir : str, optional
            Path of the dataset's data files.
        tasks : dict, optional
            List of tasks.

        """
        assert name, "Must input a valid dataset name."
        assert name in self.data["dataset"], "The dataset \'{}\' does not exist in the cache." \
                                             .format(name)
        if cache_dir:
            self.data["dataset"][name]["cache_dir"] = cache_dir
        if data_dir:
            self.data["dataset"][name]["data_dir"] = data_dir
        if tasks:
            self.data["dataset"][name]["tasks"] = tasks
            self.data["dataset"][name]["keywords"] = self._get_keywords_from_tasks(tasks)
        if cache_dir or data_dir or tasks:
            self.update_categories()
            self.write_data_cache(self.data)

    def delete_data(self, name):
        """Deletes a dataset from the cache data.

        Parameters
        ----------
        name : str
            Name of the dataset.

        """
        assert name, "Must input a valid dataset name."
        try:
            self.data["dataset"].pop(name)
            self.update_categories()
            self.write_data_cache(self.data)
        except KeyError:
            raise KeyError("The dataset \'{}\' does not exist in the cache.".format(name))


class CacheManagerDataset:
    """Manage the cache's dataset configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager

    def add(self, name, cache_dir, data_dir, tasks):
        """Adds a new dataset to the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        cache_dir : str
            Path of the dataset's metadata directory.
        data_dir : str
            Path of the dataset's data files.
        tasks : dict
            List of tasks.

        """
        assert name, "Must input a valid dataset name."
        assert cache_dir, "Must input a valid directory (cache_dir)."
        assert data_dir, "Must input a valid directory (data_dir)."
        assert tasks, "Must input a valid tasks."

        self.manager.add_data(name, cache_dir, data_dir, tasks)

    def get(self, name):
        """Retrieves the data of a dataset from the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        dict
            Information about the dataset.

        """
        assert name, "Must input a valid dataset name."
        return self.manager.get_data(name)

    def update(self, name, cache_dir=None, data_dir=None, tasks=None):
        """Updates the data of a dataset in the cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        cache_dir : str, optional
            Path of the dataset's metadata directory.
        data_dir : str, optional
            Path of the dataset's data files.
        tasks : dict, optional
            List of tasks.

        """
        assert name, "Must input a valid dataset name."
        self.manager.update_data(name, cache_dir, data_dir, tasks)

    def delete(self, name):
        """Deletes a dataset from the cache data.

        Parameters
        ----------
        name : str
            Name of the dataset.

        """
        assert name, "Must input a valid dataset name."
        self.manager.delete_data(name)

    def exists(self, name):
        """Checks if a dataset name exists in the cache..

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        bool
            Returns True if the name exists in the dataset names.
            Otherwise, returns False.

        """
        assert name, "Must input a valid dataset name."
        return name in self.manager.data["dataset"]

    def list(self):
        """Returns a list of all dataset names."""
        return list(sorted(self.manager.data["dataset"].keys()))

    def info(self):
        """Prints the dataset information contained in the cache."""
        pp = pprint.PrettyPrinter(indent=4)
        print_text_box('Dataset')
        pp.pprint(self.manager.data["dataset"])
        print('')


class CacheManagerCategory:
    """Manage the cache's category configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager

    def get(self, category):
        """Retrieves the data of a category from the cache.

        Parameters
        ----------
        category : str
            Name of the category.

        Returns
        -------
        dict
            Information about the dataset.

        """
        assert category, "Must input a valid category name."
        return self.manager.data["category"][category]


class CacheManagerInfo:
    """Manage the cache's information configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager

    def _set_cache_dir(self, path):
        """Set the root cache dir to store all metadata files"""
        assert path, 'Must input a directory path'
        self.manager.cache_dir = path

    def _get_cache_dir(self):
        """Get the root cache dir path."""
        return self.manager.cache_dir

    cache_dir = property(_get_cache_dir, _set_cache_dir)

    def reset_cache_dir(self):
        """Reset the root cache dir path."""
        self.manager.reset_cache_dir()

    def _set_download_dir(self, path):
        """Set the root save dir path for downloaded data."""
        assert path, 'Must input a non-empty path.'
        self.manager.download_dir = path

    def _get_download_dir(self):
        """Get the root save dir path."""
        return self.manager.download_dir

    download_dir = property(_get_download_dir, _set_download_dir)

    def reset_download_dir(self):
        """Reset the root download dir path."""
        self.manager.reset_download_dir()

    def reset(self):
        """Resets the cache and download dirs to default."""
        self.reset_cache_dir()
        self.reset_download_dir()

    def info(self):
        """Prints the cache and download data dir paths of the cache."""
        pp = pprint.PrettyPrinter(indent=4)
        print_text_box('Info')
        pp.pprint(self.manager.data["info"])
        print('')
