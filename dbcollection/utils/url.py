"""
Download functions.
"""


from __future__ import print_function
import os
import urllib
import wget
import hashlib

from dbcollection.utils.file_extraction import extract_file


def get_hash_value(fname):
    """Retrieve the checksum of a file.

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
    try:
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


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



def download_extract_all(urls, md5sum, dir_save, clean_cache=False, verbose=True):
    """Download urls + extract files to disk.

    Download + extract all url files to disk. If clean_cache is
    True, it removes the download files.

    Parameters
    ----------
    urls : list
        List of URL paths.
    md5sum : list
        List of md5 checksum strings for each url.
    dir_save : str
        Directory path to store the data.
    clean_cache : bool
        Remove downloaded files and keep only the extracted data.
    verbose : bool
        Display messages on screen.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Check if urls is a str
    if isinstance(urls, str):
        urls = [urls]

    # check if the save directory exists
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)

    # download + extract data and remove temporary files
    for i, url in enumerate(urls):
        if verbose:
            print('Download url ({}/{}): {}'.format(i+1, len(urls), url))

        # get download save filename
        fname_save = os.path.join(dir_save, os.path.basename(url))

        # download file
        if download_file(url, dir_save, fname_save, verbose) and verbose:
            print('File already exists, skip downloading this url.')
            continue

        # check md5 sum (if available)
        if any(md5sum):
            file_hash = get_hash_value(fname_save)
            if not file_hash == md5sum:
                print('**WARNING**: md5 checksum does not match for file: {}'.format(fname_save))
                print('Checksum expected: {}, got: {}'.format(md5sum, file_hash))

        # extract file
        extract_file(fname_save, dir_save, verbose)

        # remove downloaded file (if triggered by the user)
        if clean_cache:
            os.remove(fname_save)
