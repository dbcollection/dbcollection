"""
Download functions.
"""


from __future__ import print_function
import os
import urllib
import wget


def download_single_file_progressbar(url, file_save_name):
    """Download a file (displays a progress bar).

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
    wget.download(url, out=file_save_name)
    print('')


def download_single_file_nodisplay(url, file_save_name):
    """Download a file (no display text).

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


def download_file(url, dir_path, fname_save, verbose=False):
    """Download a single url data into a file.

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
        os.makedirs(dir_path)

    # download the file
    if verbose:
        download_single_file_progressbar(url, file_save_name)
    else:
        download_single_file_nodisplay(url, file_save_name)
