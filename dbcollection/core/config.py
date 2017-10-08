"""
API methods for configurating the cache.
"""

from __future__ import print_function
import os
import shutil

from dbcollection.core.cache import CacheManager


def config_cache(field=None, value=None, delete_cache=False, delete_cache_dir=False,
                 delete_cache_file=False, reset_cache=False, verbose=True, is_test=False):
    """Configure the cache file.

    This method allows to configure the cache file directly by selecting
    any data field/value. The user can also manually configure the file
    if he/she desires.

    To modify any entry in the cache file, simply input the field name
    you want to change along with the new data you want to insert. This
    applies to any field/data in the file.

    Another thing available is to reset/clear the entire cache paths/configs
    from the file by simply enabling the 'reset_cache' flag to true.

    Also, there is an option to completely remove the cache file+folder
    from the disk by enabling 'delete_cache' to True. This will remove the
    cache dbcollection.json and the dbcollection/ folder from disk.

    Parameters
    ----------
	field : str, optional
        Name of the field to update/modify in the cache file.
    value : str, list, table, optional
        Value to update the field.
    delete_cache : bool, optional
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool, optional
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool, optional
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool, optional
        Reset the cache file.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Delete the cache by removing the dbcollection.json cache file.
    This will NOT remove the contents of the dbcollection/. For that,
    just set the *delete_cache_dir* flag to True.

    >>> import dbcollection as dbc
    >>> dbc.config_cache(delete_cache_file=True)
    """

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if delete_cache:
        delete_cache_dir = True
        delete_cache_file = True

    if delete_cache_dir:
        # delete cache dir
        if os.path.exists(cache_manager.cache_dir):
            shutil.rmtree(cache_manager.cache_dir)
            if verbose:
                print('Deleted {} directory.'.format(cache_manager.cache_dir))

    if delete_cache_file:
        # delete the entire cache
        if os.path.exists(cache_manager.cache_filename):
            os.remove(cache_manager.cache_filename)
            if verbose:
                print('Deleted {} cache file.'.format(cache_manager.cache_filename))
    else:
        if reset_cache:
            # reset the cache file
            cache_manager.reset_cache()
        else:
            if not field is None:
                if verbose:
                    print(cache_manager.modify_field(field, value))
