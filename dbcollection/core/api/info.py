"""
Info API class.
"""


from __future__ import print_function
import json

from dbcollection.core.cache import CacheManager
from dbcollection.utils import print_text_box

from .metadata import fetch_list_datasets


def info(by_dataset=(), by_task=(), by_category=(),
         show_info=True, show_datasets=True, show_categories=True,
         show_system=False, show_available=False):
    """Prints the cache contents and other information.

    This method displays to screen the contents of the 'dbcollection.json'
    cache file. Furthermore, users can select which information is shown
    on screen by enabling/disabling the 'show_info', 'show_datasets' and
    'show_categories' args.

    Also, information about available and downloaded datasets is
    available via the 'show_available' and 'show_system' args,
    recpectively.

    For cases where the user wants to display a subset of the information
    contained in the cache file or list of system datasets, there are three
    input args that can filter the output information by dataset, task and/or
    category names.

    Parameters
    ----------
    by_dataset : str/list/tuple, optional
        List of dataset names to display to the screen.
    by_task : str/list/tuple, optional
        List of task names to display to the screen.
    by_category : str/list/tuple, optional
        List of category names to display to the screen.
    show_info : bool, optional
        Prints the cache file's info's data to screen.
    show_datasets : bool, optional
        Prints the cache file's dataset's data to screen.
    show_categories : bool, optional
        Prints the cache file's category's data to screen.
    show_system : bool, optional
        Prints the downloaded datasets stored in the cache file.
    show_available : bool, optional
        Prints the available datasets for load/download in the
        dbcollection package.

    Examples
    --------
    """
    if isinstance(by_dataset, str):
        by_dataset = (by_dataset, )
    if isinstance(by_task, str):
        by_task = (by_task, )
    if isinstance(by_category, str):
        by_category = (by_category, )

    db_info = InfoAPI(by_dataset=tuple(by_dataset),
                      by_task=tuple(by_task),
                      by_category=tuple(by_category),
                      show_info=show_info,
                      show_datasets=show_datasets,
                      show_categories=show_categories,
                      show_system=show_system,
                      show_available=show_available)

    db_info.run()


def info_cache(name=None, paths_info=True, datasets_info=True, categories_info=True,
               verbose=True, is_test=False):
    """Prints the cache contents and other information.

    Parameters
    ----------
    name : str/list/tuple, optional
        Name or list of names of datasets to be selected for print.
    paths_info : bool, optional
        Print the paths info to screen.
    datasets_info : bool, optional
        Print the datasets info to screen.
    categories_info : bool, optional
        Print the categories keywords info to screen.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Raises
    ------
    TypeError
        If input arg name is not a string or list/tuple.
    """
    printer = InfoCacheAPI(name=name,
                           paths_info=paths_info,
                           datasets_info=datasets_info,
                           categories_info=categories_info,
                           verbose=verbose,
                           is_test=is_test)

    printer.run()


def info_datasets(db_pattern='', show_downloaded=True, show_available=True,
                  verbose=True, is_test=False):
    """Prints information about available and downloaded datasets.

    Parameters
    ----------
    db_pattern : str
        String for matching dataset names available for downloading in the database.
    show_downloaded : bool, optional
        Print the downloaded datasets stored in cache.
    show_available : bool, optional
        Print the available datasets for load/download with dbcollection.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    """
    printer = InfoDatasetAPI(db_pattern=db_pattern,
                             show_downloaded=show_downloaded,
                             show_available=show_available,
                             verbose=verbose,
                             is_test=is_test)

    printer.run()


class InfoAPI(object):
    """Info display API class.

    This class contains methods to display to screen
    the contents of the cache registry.

    Also, it contains methods to display to screen
    a list of available datasets for load/download in
    dbcollection.

    Parameters
    ----------
    by_dataset : tuple
        List of dataset names to display to the screen.
    by_task : tuple
        List of task names to display to the screen.
    by_category : tuple
        List of category names to display to the screen.
    show_info : bool
        Prints the cache file's info's data to screen.
    show_datasets : bool
        Prints the cache file's dataset's data to screen.
    show_categories : bool
        Prints the cache file's category's data to screen.
    show_system : bool
        Prints the downloaded datasets stored in the cache file.
    show_available : bool
        Prints the available datasets for load/download in the
        dbcollection package.

    Attributes
    ----------
    by_dataset : tuple
        List of dataset names to display to the screen.
    by_task : tuple
        List of task names to display to the screen.
    by_category : tuple
        List of category names to display to the screen.
    show_info : bool
        Prints the cache file's info's data to screen.
    show_datasets : bool
        Prints the cache file's dataset's data to screen.
    show_categories : bool
        Prints the cache file's category's data to screen.
    show_system : bool
        Prints the downloaded datasets stored in the cache file.
    show_available : bool
        Prints the available datasets for load/download in the
        dbcollection package.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, by_dataset, by_task, by_category, show_info, show_datasets,
                 show_categories, show_system, show_available):
        assert isinstance(by_dataset, tuple), "Must input a valid dataset name."
        assert isinstance(by_task, tuple), "Must input a valid task name."
        assert isinstance(by_category, tuple), "Must input a valid category name."
        assert isinstance(show_info, bool), "Must input a valid boolean for show_info."
        assert isinstance(show_datasets, bool), "Must input a valid boolean for show_datasets."
        assert isinstance(show_categories, bool), "Must input a valid boolean for show_categories."
        assert isinstance(show_system, bool), "Must input a valid boolean for show_system."
        assert isinstance(show_available, bool), "Must input a valid boolean for show_available."

        self.by_dataset = by_dataset
        self.by_task = by_task
        self.by_category = by_category
        self.show_info = show_info
        self.show_datasets = show_datasets
        self.show_categories = show_categories
        self.show_system = show_system
        self.show_available = show_available
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        if self.show_system or self.show_available:
            if self.show_system:
                self.display_registered_datasets_in_cache()

            if self.show_available:
                self.display_available_datasets_supported_by_dbcollection()
        else:
            if self.show_info:
                self.display_info_section_from_cache()

            if self.show_datasets:
                self.display_dataset_section_from_cache()

            if self.show_categories:
                self.display_category_section_from_cache()

    def display_info_section_from_cache(self):
        self.cache_manager.info.info()

    def display_dataset_section_from_cache(self):
        self.cache_manager.dataset.info()

    def display_category_section_from_cache(self):
        self.cache_manager.category.info()

    def display_registered_datasets_in_cache(self):
        print_text_box('Available datasets in cache for load')
        datasets = self.get_datasets_from_cache()
        for name in sorted(datasets):
            tasks = list(sorted(datasets[name]['tasks'].keys()))
            print('  - {}  {}'.format(name, tasks))
        print('')

    def get_datasets_from_cache(self):
        return self.cache_manager.manager.data["dataset"]

    def display_available_datasets_supported_by_dbcollection(self):
        print_text_box('Available datasets for download')
        available_datasets_list = fetch_list_datasets()
        for name in sorted(available_datasets_list):
            tasks = list(sorted(available_datasets_list[name]['tasks'].keys()))
            print('  - {}  {}'.format(name, tasks))
        print('')


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
        """Main method."""
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
        """Main method."""
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
