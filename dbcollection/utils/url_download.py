"""
Download functions.
"""


from __future__ import print_function
import os
import sys
import errno
import hashlib
import urllib
import requests
from clint.textui import progress


#---------------------------------------------------------
# directory/file os management
#---------------------------------------------------------

def create_dir(dir_path, verbose=False):
    """
    Create directory if not existing.

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
    """
    Check if the path exists and remove the file.

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


#---------------------------------------------------------
# md5 functions
#---------------------------------------------------------

def get_hash_value(fname):
    """
    Retrieve the checksum of a file.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    str
        Checksum string.

    Raises
    ------
        None
    """
    return hashlib.md5(open(fname, 'rb').read()).hexdigest()


def check_file_integrity_md5(fname, md5sum):
    """
    Check the integrity of a file using md5 hash.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    md5sum : str
        MD5 checksum.

    Returns
    -------
        None

    Raises
    ------
    Exception

    """
    if not get_hash_value(fname) == md5sum:
        raise Exception('File check sum is invalid.')


#---------------------------------------------------------
# Download functions
#---------------------------------------------------------

def download_single_file_progressbar(url, file_save_name):
    """
    Download a file (display a progress bar).

    Parameters
    ----------
    url : str
        URL location.
    file_save_name : str
        File name + path to store on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    print('Downloading {} to: {}'.format(url, file_save_name))
    r = requests.get(url, stream=True)
    with open(file_save_name, 'wb') as (f, err):
        if err:
            raise IOError('Error opening file: {}'.format(file_save_name))
        else:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), \
                                      expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()


def download_single_file_nodisplay(url, file_save_name):
    """
    Download a file (no display text).

    Parameters
    ----------
    url : str
        URL location.
    file_save_name : str
        File name + path to store on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    with urllib.request.urlopen(url) as response, open(file_save_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)


def url_get_filename(url, dir_save):
    """
    Extract filename from the url string

    Parameters
    ----------
    url : str
        URL location.
    dir_save : str
        Directory path to store the url file on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # split url string
    if sys.platform == 'win32':
        url_fname = url.rsplit('\\', 1)[1]
    else:
        url_fname = url.rsplit('/', 1)[1]

    # join strings and return them
    return os.path.join(dir_save, url_fname)


def download_file(url, dir_path, fname_save, verbose=False):
    """
    Download a single url data into a file.

    Parameters
    ----------
    url : str
        URL location.
    dir_path : str
        Directory path to store the file.
    fname_save : str
        File name + path.
    verbose : bool
        Display messages + progress bar on screen when downloading the file.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # save file
    file_save_name = fname_save

    # check if the filename already exists
    if os.path.exists(file_save_name):
        return True

    # check if the path exists
    if not os.path.exists(dir_path):
        create_dir(dir_path, verbose)

    # download the file
    if verbose:
        download_single_file_progressbar(url, file_save_name)
    else:
        download_single_file_nodisplay(url, file_save_name)
