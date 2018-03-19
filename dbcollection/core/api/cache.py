"""
Cache API class.
"""


from __future__ import print_function
import os
import shutil

from dbcollection.core.manager import CacheManager
from dbcollection.utils import nested_lookup


def cache(query=(), delete_cache=False, delete_cache_dir=False, delete_cache_file=False,
          reset_cache=False, reset_path_cache=False, reset_path_downloads=False,
          set_cache_dir='', set_downloads_dir='', verbose=True):
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
    query : str/list/tuple, optional
        Pattern or list of patterns to search for in the cache file.
    delete_cache : bool, optional
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool, optional
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool, optional
        Delete/remove the dbcollection.json cache file.
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
    if isinstance(query, str):
        query = (query, )
    else:
        query = tuple(query)

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
    query : tuple
        List of patterns to search for in the cache file.
    delete_cache : bool
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool
        Reset the cache file.
    reset_cache_dir_path : bool
        Reset the cache dir path to the default path.
    reset_cache_downloads_path : bool
        Reset the downloads dir path to the default path.
    set_cache_dir_path : str
        New path for the cache dir.
    set_downloads_dir : str
        New path for the downloads dir.
    verbose : bool
        Displays text information (if true).

    Attributes
    ----------
    query : tuple
        List of patterns to search for in the cache file.
    delete_cache : bool
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool
        Reset the cache file.
    reset_cache_dir_path : bool
        Reset the cache dir path to the default path.
    reset_cache_downloads_path : bool, optional
        Reset the downloads dir path to the default path.
    set_cache_dir_path : str
        New path for the cache dir.
    set_downloads_dir : str
        New path for the downloads dir.
    verbose : bool
        Displays text information (if true).
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, query, delete_cache, delete_cache_dir, delete_cache_file,
                 reset_cache, reset_path_cache, reset_path_downloads,
                 set_cache_dir, set_downloads_dir, verbose):
        """Initialize class."""
        assert isinstance(query, tuple), "Must input a valid query."
        assert isinstance(delete_cache, bool), "Must input a valid boolean for delete_cache."
        assert isinstance(delete_cache_dir, bool), "Must input a valid boolean for delete_cache_dir."
        assert isinstance(delete_cache_file, bool), "Must input a valid boolean for delete_cache_file."
        assert isinstance(reset_cache, bool), "Must input a valid boolean for reset_cache."
        assert isinstance(reset_path_cache, bool), "Must input a valid boolean for reset_path_cache."
        assert isinstance(reset_path_downloads, bool), "Must input a valid boolean for reset_path_downloads."
        assert isinstance(set_cache_dir, str), "Must input a valid string for set_cache_dir."
        assert isinstance(set_downloads_dir, str), "Must input a valid string for set_downloads_dir."
        assert isinstance(verbose, bool), "Must input a valid boolean for verbose."

        self.query = query
        self.delete_cache = delete_cache
        self.delete_cache_dir = delete_cache_dir
        self.delete_cache_file = delete_cache_file
        self.reset_cache = reset_cache
        self.reset_path_cache = reset_path_cache
        self.reset_path_downloads = reset_path_downloads
        self.set_cache_dir = set_cache_dir
        self.set_downloads_dir = set_downloads_dir
        self.verbose = verbose
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        if any(self.query):
            result = self.get_matching_metadata_from_cache(self.query)
            if self.verbose:
                print('==> Patterns found in cache:')
                for i, pattern in enumerate(self.query):
                    print('    - {}: {} found'.format(pattern, len(result[i])))
            return result

        if self.delete_cache_dir or self.delete_cache:
            self.remove_cache_dir_from_disk()
            if self.verbose:
                print('Deleted {} directory.'.format(self.get_cache_dir()))

        if self.delete_cache_file or self.delete_cache:
            self.remove_cache_file_from_disk()
            if self.verbose:
                print('Deleted {} cache file.'.format(self.get_cache_filename()))

        if self.reset_cache:
            self.reset_cache_file()
            if self.verbose:
                print('Cache reseted.')

        if self.reset_path_cache and not self.reset_cache:
            self.reset_cache_dir_path()
            if self.verbose:
                print('Reseted the cache dir path: {}.'.format(self.get_cache_dir()))

        if self.reset_path_downloads and not self.reset_cache:
            self.reset_download_dir_path()
            if self.verbose:
                print('Reseted the download dir path: {}.'.format(self.get_download_dir()))

        if any(self.set_cache_dir):
            self.set_cache_dir_path()
            if self.verbose:
                print('New cache dir path: {}.'.format(self.get_cache_dir()))

        if any(self.set_downloads_dir):
            self.set_download_dir_path()
            if self.verbose:
                print('New download dir path: {}.'.format(self.get_download_dir()))

    def get_matching_metadata_from_cache(self, patterns):
        """Returns a list of matching patterns from the cache."""
        found = []
        for pattern in patterns:
            if any(pattern):
                result = self.get_matching_pattern_from_cache(pattern)
            else:
                result = []
            found.append(result)
        return found

    def get_matching_pattern_from_cache(self, pattern):
        """Returns data from cache that matches the pattern."""
        data = self.get_cache_data()
        results = self.find_pattern_in_dict(data, pattern)
        out = self.add_key_to_results(results, pattern)
        return out

    def get_cache_data(self):
        return self.cache_manager.manager.data

    def find_pattern_in_dict(self, data, pattern):
        return list(nested_lookup(key=pattern, document=data, wild=True))

    def add_key_to_results(self, results, pattern):
        return [{pattern: result} for result in results]

    def remove_cache_dir_from_disk(self):
        cache_dir = self.get_cache_dir()
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

    def get_cache_dir(self):
        return self.cache_manager.manager.cache_dir

    def remove_cache_file_from_disk(self):
        cache_filename = self.get_cache_filename()
        if os.path.exists(cache_filename):
            os.remove(cache_filename)

    def get_cache_filename(self):
        return self.cache_manager.manager.cache_filename

    def reset_cache_file(self):
        self.cache_manager.manager.reset_cache(force_reset=True)

    def reset_cache_dir_path(self):
        self.cache_manager.manager.reset_cache_dir()

    def reset_download_dir_path(self):
        self.cache_manager.manager.reset_download_dir()

    def get_download_dir(self):
        return self.cache_manager.manager.download_dir

    def set_cache_dir_path(self):
        self.cache_manager.manager.cache_dir = self.set_cache_dir

    def set_download_dir_path(self):
        self.cache_manager.manager.download_dir = self.set_downloads_dir
