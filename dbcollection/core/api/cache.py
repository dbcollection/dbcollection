"""
Cache API class.
"""


from __future__ import print_function

from dbcollection.core.cache import CacheManager


def cache(query='', delete_cache=False, delete_cache_dir=False, delete_cache_file=False,
          reset_cache=False, reset_path_cache=False, reset_path_downloads=False,
          set_cache_dir=None, set_downloads_dir=None, verbose=True):
    """Configures the cache file.

    This method allows to configure some options of the cache file. The
    available options are only a subset of all possible parameters/registries
    of the cache file. These provides the most common operations one may need
    to perform. For more specific configurations, manually modifying the cache
    file or using the cache manager methods is the best procedure.

    The most common operations one might need to perform are setting, deleting
    or reseting the cache file itself and/or the existing data. (The input args
    for these operations should be self-explanatory just by looking at their
    name description.)

    Additionally, performing basic queries to the cache is supported via the
    'query' input arg. To search for a particular pattern (e.g., a dataset or
    task) just assign the 'query' to the pattern you are looking for.

    Parameters
    ----------
    delete_cache : bool, optional
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool, optional
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool, optional
        Delete/remove the dbcollection.json cache file.
    query : str/list, optional
        Pattern or list of patterns to search for in the cache file.
    reset_cache : bool, optional
        Reset the cache file.
    reset_cache_dir_path : bool, optional
        Reset the cache dir path to the default path.
    reset_cache_downloads_path : bool, optional
        Reset the downloads dir path to the default path.
    set_cache_dir_path : str, optional
        New path for the cache dir.
    set_downloads_dir : str, optional
        New path for the downloads dir.
    verbose : bool, optional
        Displays text information (if true).

    Returns
    -------
    str/list
        Pattern or list of patterns matching the input query pattern.

    Examples
    --------
    Delete the cache by removing the dbcollection.json cache file.
    This will NOT remove the file contents in dbcollection/. For that,
    you must set the *delete_cache_dir* argument to True.

    >>> import dbcollection as dbc
    >>> dbc.cache(delete_cache_file=True)

    """
    cache = CacheAPI(query=query,
                     delete_cache=delete_cache,
                     delete_cache_dir=delete_cache_dir,
                     delete_cache_file=delete_cache_file,
                     reset_cache=reset_cache,
                     reset_path_cache=reset_path_cache,
                     reset_path_downloads=reset_path_downloads,
                     set_cache_dir=set_cache_dir,
                     set_downloads_dir=set_downloads_dir,
                     verbose=verbose)

    return cache.run()


class CacheAPI(object):
    """Cache configuration API class.

    This class contains methods to configure the
    cache registry. Also, it can remove the cache
    files from disk if needed.

    Parameters
    ----------
    delete_cache : bool, optional
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool, optional
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool, optional
        Delete/remove the dbcollection.json cache file.
    query : str/list, optional
        Pattern or list of patterns to search for in the cache file.
    reset_cache : bool, optional
        Reset the cache file.
    reset_cache_dir_path : bool, optional
        Reset the cache dir path to the default path.
    reset_cache_downloads_path : bool, optional
        Reset the downloads dir path to the default path.
    set_cache_dir_path : str, optional
        New path for the cache dir.
    set_downloads_dir : str, optional
        New path for the downloads dir.
    verbose : bool, optional
        Displays text information (if true).

    Attributes
    ----------

    """

    def __init__(self, delete_cache, delete_cache_dir, delete_cache_file,
                 reset_cache, reset_path_cache, reset_path_downloads,
                 set_cache_dir, set_downloads_dir, query, verbose):
        pass

    def run(self):
        pass
