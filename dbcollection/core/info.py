"""
Info API class.
"""


from __future__ import print_function
import json

from dbcollection.core.cache import CacheManager

from .list_datasets import fetch_list_datasets


class InfoCacheAPI(object):
    """Cache info display API class.

    This class contains methods to display to screen
    the contents of the cache registry.

    Parameters
    ----------
    name : str/list/tuple, optional
        Name or list of names of datasets to be selected for print.
    paths_info : bool
        Print the paths info to screen.
    datasets_info : bool
        Print the datasets info to screen.
    categories_info : bool
        Print the categories keywords info to screen.
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    name : str/list/tuple, optional
        Name or list of names of datasets to be selected for print.
    paths_info : bool
        Print the paths info to screen.
    datasets_info : bool
        Print the datasets info to screen.
    categories_info : bool
        Print the categories keywords info to screen.
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.
    _max_size_name : int
        Maximum length of the biggest dataset name.

    """

    def __init__(self, name, paths_info, datasets_info, categories_info, verbose, is_test):
        """Initialize class."""
        assert paths_info is not None, 'paths_info cannot be empty.'
        assert datasets_info is not None, 'datasets_info cannot be empty.'
        assert categories_info is not None, 'categories_info cannot be empty.'
        assert verbose is not None, 'verbose cannot be empty.'
        assert is_test is not None, 'is_test cannot be empty.'

        self.name = name
        self.paths_info = paths_info
        self.datasets_info = datasets_info
        self.categories_info = categories_info
        self.verbose = verbose
        self.is_test = is_test
        self.cache_manager = CacheManager(self.is_test)
        self._max_size_name = 0

        self.parse_input_name()

    def parse_input_name(self):
        """Check if name type is valid."""
        if self.name:
            if isinstance(self.name, str):
                names = (self.name,)
            elif isinstance(self.name, list):
                names = tuple(self.name)
            elif isinstance(self.name, tuple):
                names = self.name
            else:
                raise TypeError('Input \'name\' must be either a string or a list/tuple.')
        else:
            names = None
        self.names = names

    def run(self):
        """<stuff>.

        ** Main method **

        """
        self.display_paths_info()
        self.display_datasets_info()
        self.display_categories_info()

    def display_paths_info(self):
        """Display paths in the cache's info section."""
        if self.verbose:
            print('--------------')
            print('  Paths info ')
            print('--------------')
            print(json.dumps(self.cache_manager.data['info'], sort_keys=True, indent=4))
            print('')

    def display_datasets_info(self):
        """Display paths in the cache's dataset section."""
        if self.verbose:
            print('----------------')
            print('  Dataset info ')
            print('----------------')
            if self.names:
                self.display_selected_names_dataset()
            else:
                self.display_all_names_dataset()
            print('')

    def display_selected_names_dataset(self):
        """Display selected names from all dataset names."""
        for name in sorted(self.names):
            data = {name: self.cache_manager.data['dataset'][name]}
            print(json.dumps(data, sort_keys=True, indent=4))

    def display_all_names_dataset(self):
        """Display all dataset names."""
        print(json.dumps(self.cache_manager.data['dataset'], sort_keys=True, indent=4))

    def display_categories_info(self):
        """Display paths in the cache's category section."""
        if self.verbose:
            if any(self.cache_manager.data['category']):
                print('------------------------')
                print('  Datasets by category ')
                print('------------------------\n')
                if self.names:
                    self.display_selected_names_category()
                else:
                    self.display_all_names_category()
                print('')

    def display_selected_names_category(self):
        """Display selected names from all category names."""
        for category in self.cache_manager.data['category']:
            list_datasets = self.get_list_dataset_names_in_category(category)
            if any(list_datasets):
                data = sorted(list_datasets)
                self.print_with_offset(category, data)

    def get_list_dataset_names_in_category(self, category):
        """Get list of dataset names from a category."""
        list_datasets = []
        for name in self.names:
            if name in self.cache_manager.data['category'][category]:
                list_datasets.append(name)
        return list_datasets

    def print_with_offset(self, name, data):
        """Print the category names + data with an equal offset between prints."""
        if self._max_size_name == 0:
            self._max_size_name = self.get_max_size_names_category()
        print("{:{}}".format('   > {}: '.format(name), self._max_size_name) + "{}".format(data))

    def get_max_size_names_category(self):
        """Get maximum length of all category names."""
        offset = 7
        return max([len(name) for name in self.cache_manager.data['category']]) + offset

    def display_all_names_category(self):
        """Display all category names."""
        for name in self.cache_manager.data['category']:
            data = sorted(self.cache_manager.data['category'][name])
            self.print_with_offset(name, data)


class InfoDatasetAPI(object):
    """Datasets info display API class.

    This class contains methods to display to screen
    a list of available datasets for load/download in
    dbcollection.

    Parameters
    ----------
    db_pattern : str
        String for matching dataset names available for downloading in the database.
    show_downloaded : bool
        Print the downloaded datasets stored in cache.
    show_available : bool
        Print the available datasets for load/download with dbcollection.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    db_pattern : str
        String for matching dataset names available for downloading in the database.
    show_downloaded : bool
        Print the downloaded datasets stored in cache.
    show_available : bool
        Print the available datasets for load/download with dbcollection.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, db_pattern, show_downloaded, show_available, verbose, is_test):
        """Initialize class."""
        assert db_pattern is not None, 'db_pattern cannot be empty.'
        assert show_downloaded is not None, 'show_downloaded cannot be empty.'
        assert show_available is not None, 'show_available cannot be empty.'
        assert verbose is not None, 'verbose cannot be empty.'
        assert is_test is not None, 'is_test cannot be empty.'

        self.db_pattern = db_pattern
        self.show_downloaded = show_downloaded
        self.show_available = show_available
        self.verbose = verbose
        self.is_test = is_test
        self.cache_manager = CacheManager(self.is_test)

    def run(self):
        """<stuff>.

        ** Main method **

        """
        self.display_downloaded_datasets()
        self.display_available_datasets()

    def display_downloaded_datasets(self):
        """Display information about the available datasets in cache for loading."""
        if self.show_downloaded:
            if self.verbose:
                print('----------------------------------------')
                print('  Available datasets in cache for load ')
                print('----------------------------------------')
                for name in sorted(self.cache_manager.data['dataset']):
                    tasks = list(sorted(self.cache_manager.data['dataset'][name]['tasks'].keys()))
                    print('  - {}  {}'.format(name, tasks))
                print('')

    def display_available_datasets(self):
        """Display information about the available datasets for download."""
        if self.show_available:
            if self.verbose:
                print('-----------------------------------')
                print('  Available datasets for download  ')
                print('-----------------------------------')
                if any(self.db_pattern):
                    self.display_datasets_match_pattern()
                else:
                    self.display_datasets_all()

    def display_datasets_match_pattern(self):
        """Display only datasets that match the pattern."""
        available_datasets_list = fetch_list_datasets()
        for name in sorted(available_datasets_list):
            if self.db_pattern in name:
                tasks = list(sorted(available_datasets_list[name]['tasks'].keys()))
                print('  - {}  {}'.format(name, tasks))

    def display_datasets_all(self):
        """Display all datasets."""
        available_datasets_list = fetch_list_datasets()
        for name in sorted(available_datasets_list):
            tasks = list(sorted(available_datasets_list[name]['tasks'].keys()))
            print('  - {}  {}'.format(name, tasks))
