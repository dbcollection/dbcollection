"""
Info API class.
"""


from __future__ import print_function
import json

from dbcollection.core.manager import CacheManager
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
    Display the information contained in the cache of
    the dbcollection package:

    >>> dbc.info()

    Show the available datasets for download with dbcollection:

    >>> dbc.info(show_available=True)

    Or show the registered datasets in the system:

    >>> dbc.info(show_system=True)

    """
    if isinstance(by_dataset, str):
        by_dataset = (by_dataset, )
    else:
        by_dataset = tuple(by_dataset)
    if isinstance(by_task, str):
        by_task = (by_task, )
    else:
        by_task = tuple(by_task)
    if isinstance(by_category, str):
        by_category = (by_category, )
    else:
        by_category = tuple(by_category)

    db_info = InfoAPI(by_dataset=by_dataset,
                      by_task=by_task,
                      by_category=by_category,
                      show_info=show_info,
                      show_datasets=show_datasets,
                      show_categories=show_categories,
                      show_system=show_system,
                      show_available=show_available)

    db_info.run()


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
        self.cache_manager.dataset.info(
            datasets=self.by_dataset,
            tasks=self.by_task
        )

    def display_category_section_from_cache(self):
        self.cache_manager.category.info(
            categories=self.by_category
        )

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
