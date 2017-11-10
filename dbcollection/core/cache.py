"""
Class to manage the dbcollection.json cache file.
"""


from __future__ import print_function
import os
import shutil
import errno
import json
import warnings


class CacheManager:
    """Class to manage the dbcollection cache data

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

    def __init__(self, is_test=False):
        """Initialize class."""
        self.is_test = is_test

        # setup cache file path+name
        if self.is_test:
            self.cache_filename = os.path.join(os.path.expanduser("~"), 'dbcollection_test.json')
        else:
            self.cache_filename = os.path.join(os.path.expanduser("~"), 'dbcollection.json')
        if not os.path.exists(self.cache_filename):
            print('Generating the dbcollection\'s package cache file on disk: {}'
                  .format(self.cache_filename))
            self.write_data_cache(self._empty_data(), self.cache_filename)

        # load cache data file
        self.data = self.read_data_cache()
        self._cache_dir = self._get_cache_dir()

    def _set_cache_dir(self, path):
        """Set the default cache dir to store all metadata files"""
        # assert path, 'Must input a directory path'
        self._cache_dir = path
        self.data['info']['default_cache_dir'] = self._cache_dir
        self.write_data_cache(self.data)

    def _get_cache_dir(self):
        """Get the default cache dir path."""
        return self.data['info']['default_cache_dir']

    cache_dir = property(_get_cache_dir, _set_cache_dir)

    def _default_cache_dir_path(self):
        """Returns the pre-defined path of the cache_dir."""
        if self.is_test:
            default_cache_dir = os.path.join(os.path.expanduser("~"), 'tmp', 'dbcollection')
        else:
            default_cache_dir = os.path.join(os.path.expanduser("~"), 'dbcollection')
        return default_cache_dir

    def reset_cache_dir(self):
        """Reset the default cache directory path."""
        self._set_cache_dir(self._default_cache_dir_path())

    def create_os_home_dir(self):
        """Create the main dir to store all metadata files."""
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)

    def _set_download_dir(self, path):
        """Set the default save dir path for downloaded data."""
        assert path, 'Must input a non-empty path.'
        self.data['info']['default_download_dir'] = path
        self.write_data_cache(self.data)

    def _get_download_dir(self):
        """Get the default save dir path."""
        return self.data['info']['default_download_dir']

    def reset_download_dir(self):
        """Reset the default download dir."""
        return self._set_download_dir('')

    download_dir = property(_get_download_dir, _set_download_dir)

    def clear(self):
        """Delete the cache file + directory from disk."""
        # cache file
        if os.path.exists(self.cache_filename):
            self._os_remove(self.cache_filename)

        # cache dir
        if os.path.exists(self._cache_dir):
            self._os_remove(self._cache_dir)

    def read_data_cache_file(self):
        """Read the cache file data to memory.

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
            with open(self.cache_filename, 'r') as json_data:
                return json.load(json_data)
        except IOError:
            raise IOError('Unable to open file: ' + self.cache_filename)

    def read_data_cache(self):
        """Load data from the dbcollection cache file.

        Returns
        -------
        dict
            Data structure of the cache (file).

        """
        # check if file exists
        if os.path.exists(self.cache_filename):
            return self.read_data_cache_file()
        else:
            return self._empty_data()

    def write_data_cache(self, data, fname=None):
        """Write data to the cache file (dbcollection.json).

        Parameters
        ----------
        name : str
            Name of the dataset.
        fname : str, optional
            File path+name to store the cache data.

        Raises
        ------
        IOError
            If the file cannot be opened.

        """
        assert data, 'Must input a non-empty dictionary'
        filename = fname or self.cache_filename
        with open(filename, 'w') as file_cache:
            json.dump(data, file_cache, sort_keys=True, indent=4, ensure_ascii=False)
        self.reload_cache()  # reload the data

    def _empty_data(self):
        """Returns an empty (dummy) template of the cache data structure."""
        default_cache_path = self._default_cache_dir_path()
        default_download_path = os.path.join(default_cache_path, 'downloaded_data')
        return {
            "info": {
                "default_cache_dir": default_cache_path,
                "default_download_dir": default_download_path,
            },
            "dataset": {},
            "category": {}
        }

    def _os_remove(self, fname):
        """Remove a file/directory from disk.

        Parameters
        ----------
        fname : str
            File name+path on disk.

        Raises
        ------
        OSError
            If an error occurred when deleting a file.

        """
        try:
            if os.path.exists(fname):
                if os.path.isdir(fname):
                    shutil.rmtree(fname)
                else:
                    os.remove(fname)
        except OSError as err:
            if err.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                raise OSError('Unable to remove: {}'.format(fname))

    def delete_entry(self, name):
        """Delete a dataset entry from a category dictionary.

        Parameters
        ----------
        name : str
            Dataset name.

        """
        try:
            self.data['dataset'].pop(name)

            # remove the dataset name from the category list
            self.delete_category_entry(name)

            # update cache file on disk
            self.write_data_cache(self.data)
        except KeyError:
            print('Dataset \'{}\' not found in cache.'.format(name))

    def delete_category_entry(self, name):
        """Delete all entries in the category keywords list where 'name' exists.

        Parameters
        ----------
        name : str
            Name of the dataset.

        """
        keywords = []
        for keyword in self.data['category']:
            if name in self.data['category'][keyword]:
                self.data['category'][keyword].remove(name)
                if not any(self.data['category'][keyword]):
                    keywords.append(keyword)  # add keyword name to the list

        # remove empty keyword
        if any(keywords):
            for keyword in keywords:
                self.data['category'].pop(keyword)

        # update cache file on disk
        self.write_data_cache(self.data)

    def delete_task(self, name, task):
        """Delete a task of a dataset in cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        task : str
            Name of the task

        """
        try:
            task_filename = self.data['dataset'][name]['tasks'][task]
            self.data['dataset'][name]['tasks'].pop(task)

            # update cache file on disk
            self.write_data_cache(self.data)

            # remove file from disk
            self._os_remove(task_filename)

            return True
        except KeyError:
            print('Task \'{}\' not found in cache for {}.'.format(task, name))
            return False

    def delete_dataset_cache(self, name):
        """Delete the cache data from disk of a dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.

        """
        # get cache dir path
        cache_dir_path = os.path.join(self._cache_dir, name)

        # remove cache dir
        self._os_remove(cache_dir_path)

        # remove entry from the data
        self.delete_entry(name)

        # remove dataset from the category keywords
        self.delete_category_entry(name)

        # write updated data to file
        self.write_data_cache(self.data)

    def reset_cache(self, force_reset=False):
        """Resets all datasets/categories from cache.

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
            self.write_data_cache(self._empty_data(), self.cache_filename)
        else:
            msg = 'All information about stored datasets will be lost if you proceed! ' + \
                  'Set \'force_reset=True\' to proceed with the reset of dbcollection.json.'
            warnings.warn(msg, UserWarning, stacklevel=2)

    def check_dataset_name(self, name):
        """Check if the dataset name exists in the available dictionary keys.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        bool
            The dataset exists (True) or not (False).

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
        is_append : bool, optional
            Appends the task cache data to existing ones.

        """
        if is_append:
            if name in self.data['dataset']:
                self.data['dataset'][name]['tasks'].update(new_info['tasks'])
            else:
                self.data['dataset'][name] = new_info
        else:
            self.data['dataset'][name] = new_info

    def delete_dataset(self, name, delete_data=False):
        """Delete a dataset from disk/cache.

        Parameters
        ----------
        name : str
            Name of the dataset.
        delete_data : bool, optional
            Flag indicating if the data's directory has to be deleted (or skip it).

        """
        dset_paths = self.get_dataset_storage_paths(name)

        # remove cache directory
        self.delete_dataset_cache(name)

        # delete data from disk
        if delete_data:
            self._os_remove(dset_paths['data_dir'])

    def is_empty(self):
        """Checks if the cache data has any dataset."""
        return any(self.data['dataset'])

    def exists_dataset(self, name):
        """Check if a dataset exists in cache for loading.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Returns
        -------
        bool
            Return true if the category exists, else return False.

        """
        return name in self.data['dataset']

    def exists_task(self, name, task):
        """Check if a task of a dataset exists in cache.

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

        """
        try:
            return task in self.data['dataset'][name]['tasks']
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
        KeyError
            If the dataset name does not exist in cache.

        """
        try:
            return {
                "data_dir": self.data['dataset'][name]["data_dir"],
                "cache_dir": os.path.join(self._cache_dir, name)
            }
        except KeyError:
            raise KeyError('Dataset name does not exist in cache: {}'.format(name))

    def get_task_cache_path(self, name, task):
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
            In case the dataset name.

        """
        try:
            return self.data['dataset'][name]['tasks'][task]
        except KeyError:
            raise KeyError('Dataset name/task cache data is empty or does not exist: {}/{}'
                           .format(name, task))

    def add_keywords(self, name, keywords):
        """Add keywords to the category dictionary for the dataset.

        Parameters
        ----------
        name : str
            Name of the dataset.
        keywords : list
            Keyword categories of the dataset.

        """
        if isinstance(keywords, list):
            keywords = tuple(keywords)
        elif not isinstance(keywords, tuple):
            keywords = (keywords,)

        for keyword in keywords:
            if any(keyword):
                if keyword not in self.data["dataset"][name]["keywords"]:
                    self.data["dataset"][name]["keywords"].append(keyword)

                if keyword in self.data['category']:
                    if name not in self.data['category'][keyword]:
                        self.data['category'][keyword].append(name)
                else:
                    self.data['category'][keyword] = [name]

    def update(self, name, data_dir, cache_tasks, cache_keywords, is_append=True):
        """Modify/add data of a dataset in the cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.
        data_dir : str
            Dataset directory on disk where all data is stored.
        cache_tasks : dict
            A table of tasks.
        cache_keywords : str
            A list of keywords caracterizing the dataset.
        is_append : bool
            Overrides existing cache info data with new data.

        """
        new_info_dict = {
            "data_dir": data_dir,
            "tasks": cache_tasks,
            "keywords": cache_keywords
        }

        # add/update data with the new info to the dataset dictionary
        self.add_data(name, new_info_dict, is_append)

        # add/update the keyword list of the category dictionary
        if any(cache_keywords):
            self.add_keywords(name, cache_keywords)

        # write to file
        self.write_data_cache(self.data)

    def modify_field(self, field=None, value=None):
        """Assign/Modify a field value to the cache data.

        This method allows to change/assign a value to any field
        by referencing only the name of the field.

        Parameters
        ----------
        field : str
            Name of the field of the cache file.
        value : str/list/dict
            New content to modify the field with.

        Returns
        -------
        bool
            Return True if a valid field was inserted.

        Raises
        ------
        Exception
            If the input field is not valid.

        """
        assert field, 'Invalid field: {}'.format(field)
        assert value, 'Invalid value: {}'.format(value)

        # check info / dataset lists first
        if field in self.data:
            self.data[field] = value
            self.write_data_cache(self.data)
            return True

        # match default paths
        if field in self.data['info']:
            self.data['info'][field] = value
            self.write_data_cache(self.data)
            return True

        # match datasets/tasks
        if field in self.data['dataset']:
            self.data['dataset'][field] = value
            self.write_data_cache(self.data)
            return True

        # match datasets/tasks
        if field in self.data['category']:
            self.data['category'][field] = value
            self.write_data_cache(self.data)
            return True

        raise Exception('Field name not existing: {}'.format(field))

    def info(self, name=None, show_paths=True, show_datasets=True, show_categories=True):
        """Display the cache contents in a digestible format.

        Parameters
        ----------
        name : str
            Name of the dataset.
        show_paths : bool, optional
            Displays the paths information.
        show_datasets : bool, optional
            Displays the dataset contents.
        show_categories : bool, optional
            Displays the categories information.

        """
        # print info header
        if show_paths:
            print('--------------')
            print('  Paths info ')
            print('--------------')
            print(json.dumps(self.data['info'], sort_keys=True, indent=4))
            print('')

        # print datasets
        if show_datasets:
            if name:
                print('---------------------')
                print('  Dataset info: {} '.format(name))
                print('---------------------')
                print(json.dumps(self.data['dataset'][name], sort_keys=True, indent=4))
            else:
                print('---------------------')
                print('  Dataset info: all ')
                print('---------------------')
                print(json.dumps(self.data['dataset'], sort_keys=True, indent=4))
            print('')

        if show_categories:
            if name:
                print('------------------------')
                print('  Categories: {} '.format(name))
                print('------------------------\n')
                max_size_name = max([len(n) for n in self.data['category'][name]]) + 7
                for name in self.data['category']:
                    print("{:{}}".format('   > {}: '.format(name), max_size_name) +
                          "{}".format(sorted(self.data['category'][name])))
            else:
                print('------------------------')
                print('  Categories: all ')
                print('------------------------\n')
                max_size_name = max([len(category) for category in self.data['category']]) + 7
                for category in self.data['category']:
                    print("{:{}}".format('   > {}: '.format(category), max_size_name) +
                          "{}".format(sorted(self.data['category'][category])))

    def reload_cache(self):
        """Reload the cache file contents."""
        self.data = self.read_data_cache()
        self._cache_dir = self._get_cache_dir()
