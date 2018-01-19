"""
API methods for managing datasets.

This module contains several methods for easy management of datasets. These include methods for:

- downloading datasets' data files from online sources (urls)
- processing/parsing data files + annotations into a HDF5 file to store metadata information
- loading dataset's metadata into a data loader object
- add/remove datasets to/from cache
- managing the cache file
- querying the cache file for some dataset/keyword
- displaying information about available datasets in cache or for download

These methods compose the core API for dealing with dataset management.
Users should be able to take advantage of most functionality by using only these
functions to manage and query their datasets in a simple and easy way.
"""


from __future__ import print_function

from .download import download
from .process import process
from .load import load
from .add import add
from .remove import remove
from .config_cache import config_cache
from .query import QueryAPI
from .info import InfoCacheAPI, InfoDatasetAPI


def query(pattern='info', verbose=True, is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess.

    Parameters
    ----------
    pattern : str, optional
        Field name used to search for a matching pattern in cache data.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    """
    assert isinstance(pattern, str), 'Must insert a string value as input. ' + \
                                     'Expected "str", got "{}"'.format(pattern)

    query = QueryAPI(pattern=pattern,
                     verbose=verbose,
                     is_test=is_test)

    return query.run()


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
