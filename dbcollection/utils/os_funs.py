"""
OS functions.
"""

from __future__ import print_function
import os
import errno

def create_dir(dir_path, verbose=False):
    """Create directory if not existing.

    Parameters
    ----------
    dir_path : str
        Directory path on disk to create the new directory.
    verbose : bool
        Prints a message to the screen if True.

    Returns
    -------
        None

    Raises
    ------
    OSError
        If directory cannot be created.
    """
    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno != errno.EEXIST: # errno.ENOENT = no such file or directory
            raise OSError('Unable to create dir: ' + dir_path)

        if verbose:
            print('Skip creating directory (already exists on disk).')
    else:
        if verbose:
            print('Created directory: {}'.format(dir_path))


def remove_file(fname):
    """Check if the path exists and remove the file.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
        None

    Raises
    ------
    OSError
        If file cannot be removed.
    """
    try:
        os.remove(fname)
    except OSError as err:
        if err.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise
