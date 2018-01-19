"""
Config API class.
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
    value : str, list, tuple, optional
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
    This will NOT remove the file contents in dbcollection/. For that,
    you must set the *delete_cache_dir* argument to True.

    >>> import dbcollection as dbc
    >>> dbc.config_cache(delete_cache_file=True)
    """
    manager = ConfigAPI(field=field,
                        value=value,
                        delete_cache=delete_cache,
                        delete_cache_dir=delete_cache_dir,
                        delete_cache_file=delete_cache_file,
                        reset_cache=reset_cache,
                        verbose=verbose,
                        is_test=is_test)

    manager.run()


class ConfigAPI(object):
    """Cache configuration API class.

    This class contains methods to configure
    the cache registry. Also, itcan remove the
    cache files from disk if needed.

    Parameters
    ----------
    field : str, optional
        Name of the field to update/modify in the cache file.
    value : str, list, tuple, optional
        Value to update the field.
    delete_cache : bool
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool
        Reset the cache file.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    field : str
        Name of the field to update/modify in the cache file.
    value : str, list, tuple
        Value to update the field.
    delete_cache : bool
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool
        Reset the cache file.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, field, value, delete_cache, delete_cache_dir,
                 delete_cache_file, reset_cache, verbose, is_test):
        """Initialize class."""
        assert delete_cache is not None, 'delete_cache cannot be empty'
        assert delete_cache_dir is not None, 'delete_cache_dir cannot be empty'
        assert delete_cache_file is not None, 'delete_cache_file cannot be empty'
        assert reset_cache is not None, 'reset_cache cannot be empty'
        assert verbose is not None, 'verbose cannot be empty'
        assert is_test is not None, 'is_test cannot be empty'

        self.field = field
        self.value = value
        self.delete_cache = delete_cache
        self.delete_cache_dir = delete_cache_dir
        self.delete_cache_file = delete_cache_file
        self.reset_cache = reset_cache
        self.verbose = verbose
        self.is_test = is_test
        self.cache_manager = CacheManager(self.is_test)

        self.set_delete_options()

    def set_delete_options(self):
        """Set cache delete options."""
        if self.delete_cache:
            self.delete_cache_dir = True
            self.delete_cache_file = True

    def run(self):
        """Main method."""
        self.delete_cache_dir_files()
        self.modify_cache_configs()

    def delete_cache_dir_files(self):
        """Remove cache file / dir from disk (if selected)."""
        self.delete_dir()
        self.delete_file()

    def delete_dir(self):
        """Remove cache directory from disk."""
        if self.delete_cache_dir:
            if os.path.exists(self.cache_manager.cache_dir):
                shutil.rmtree(self.cache_manager.cache_dir)
                if self.verbose:
                    print('Deleted {} directory.'.format(self.cache_manager.cache_dir))

    def delete_file(self):
        """Remove the cache .json file from disk."""
        if self.delete_cache_file:
            if os.path.exists(self.cache_manager.cache_filename):
                os.remove(self.cache_manager.cache_filename)
                if self.verbose:
                    print('Deleted {} cache file.'.format(self.cache_manager.cache_filename))

    def modify_cache_configs(self):
        """Modify the cache configurations."""
        if self.reset_cache:
            self.cache_manager.reset_cache(force_reset=True)
        else:
            if self.field is not None:
                output = self.cache_manager.modify_field(self.field, self.value)
                if self.verbose:
                    print(output)
