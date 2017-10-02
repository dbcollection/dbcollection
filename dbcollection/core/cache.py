"""
Class to manage the dbcollection.json cache file.
"""


from __future__ import print_function
import os
import shutil
import errno
import json


class CacheManager:
    """ Class to manage the dbcollection cache data

    Attributes
    ----------
    is_test : bool, optional
        Flag used for tests.
    """

    def __init__(self, is_test=False):
        """Initialize class.

        Parameters
        ----------
        is_test : bool
            Flag used for tests.
        """
        self.is_test = is_test

        self.home_dir = self._set_home_dir(is_test)

        # setup cache paths
        self._setup_paths()

        # create cache file (if it does not exist)
        if not os.path.exists(self.cache_fname):
            print('Generating the dbcollection\'s package cache file on disk: {}'.format(self.cache_fname))
            self.write_data_cache(self.empty_data(), self.cache_fname)

        # load cache data file
        self.data = self.read_data_cache()


    def _setup_paths(self):
        """Setup the cache/data directories for storing the cache file.

        Creates two paths for the default cache directory for storing the cache data,
        and the filepath for the dbcollection.json file where the metadata for all datasets
        is stored.
        """
        # cache directory path (should work for all platforms)
        self.default_cache_dir = os.path.join(self.home_dir, 'dbcollection')
        self.cache_fname = os.path.join(self.home_dir, 'dbcollection.json')

        # create dir
        if not os.path.exists(self.default_cache_dir):
            print('Create cache dir: {}'.format(self.default_cache_dir))
            os.makedirs(self.default_cache_dir)


    def _set_home_dir(self, is_test=None):
        """Sets the home directory folder for the cache."""
        home_dir = os.path.expanduser("~")
        if is_test is None:
            if self.is_test:
                home_dir = os.path.join(home_dir, 'tmp')
        else:
            if is_test:
                home_dir = os.path.join(home_dir, 'tmp')
        return home_dir


    def _default_cache_dir(self):
        """Return the default cache directory."""
        return os.path.join(self.home_dir, 'dbcollection')


    def create_root_dir(self):
        """Create the main dir to store all metadata files."""
        if not os.path.exists(self.default_cache_dir):
            os.makedirs(self.default_cache_dir)


    def clear(self):
        """Delete the cache file + directory from disk."""
        # cache file
        if os.path.exists(self.cache_fname):
            self.os_remove(self.cache_fname)

        # cache dir
        if os.path.exists(self.default_cache_dir):
            self.os_remove(self.default_cache_dir)


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
            with open(self.cache_fname, 'r') as json_data:
                return json.load(json_data)
        except IOError:
            raise IOError('Unable to open file: ' + self.cache_fname)


    def read_data_cache(self):
        """Load data from the dbcollection cache file.

        Returns
        -------
        dict
            Data structure of the cache (file).

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
        fname : str, optional
            File path+name to store the cache data.

        Raises
        ------
        IOError
            If the file cannot be opened.

        """
        filename = fname or self.cache_fname
        with open(filename, 'w') as file_cache:
            json.dump(data, file_cache, sort_keys=True, indent=4, ensure_ascii=False)


    def empty_data(self):
        """Returns an empty (dummy) template of the cache data structure."""
        return {
            "info": {
                "default_cache_dir": self.default_cache_dir
            },
            "dataset": {},
            "category": {}
        }


    def os_remove(self, fname):
        """Remove a file/directory from disk.

        Parameters
        ----------
        fname : str
            File name+path on disk.

        Raises
        ------
        OSError
            If the file does not exist.

        """
        try:
            if os.path.exists(fname):
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
            self.data['dataset'][name]['tasks'].pop(task)

            # update cache file on disk
            self.write_data_cache(self.data)

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
        cache_dir_path = os.path.join(self.default_cache_dir, name)

        # remove cache dir
        self.os_remove(cache_dir_path)

        # remove entry from the data
        self.delete_entry(name)

        # remove dataset from the category keywords
        self.delete_category_entry(name)

        # write updated data to file
        self.write_data_cache(self.data)


    def reset_cache(self):
        """Resets all datasets/categories from cache."""
        self.data['dataset'] = {}
        self.data['category'] = {}
        self.write_data_cache(self.data)


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
            self.os_remove(dset_paths['data_dir'])


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
                "cache_dir": os.path.join(self.default_cache_dir, name)
            }
        except KeyError:
            raise KeyError('Dataset name does not exist in cache: {}'.format(name))


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

        """
        if not isinstance(keywords, list):
            keywords = [keywords]

        for keyword in keywords:
            if any(keyword):

                if keyword not in self.data["dataset"][name]["keywords"]:
                    self.data["dataset"][name]["keywords"].append(keyword)

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
            "keywords" : cache_keywords
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

        #print('*** Datasets by category ***\n')
        if show_categories:
            if name:
                print('------------------------')
                print('  Categories: {} '.format(name))
                print('------------------------\n')
                max_size_name = max([len(n) for n in self.data['category'][name]]) + 7
                for name in self.data['category']:
                    print("{:{}}".format('   > {}: '.format(name), max_size_name)
                        + "{}".format( sorted(self.data['category'][name])))
            else:
                print('------------------------')
                print('  Categories: all ')
                print('------------------------\n')
                for cat_name in self.data['category']:
                    if name in self.data['category'][cat_name]:
                        print('   > {}: '.format(cat_name))