"""
Utility functions used for url download, file extract, data parsing, etc.
"""

from __future__ import print_function
from .string_ascii import str_to_ascii, ascii_to_str, convert_str_to_ascii, convert_ascii_to_str
from .file_extraction import extract_file
from .file_load import load_matlab, load_json, load_pickle, load_xml, load_txt
from .md5hash import check_file_integrity_md5, get_hash_value
from .os_funs import *
from .download_url import download_file


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
            print('({}/{}) Download url: {}'.format(i+1, len(urls), url))

        # get download save filename
        fname_save = os.path.join(dir_save, os.path.basename(url))

        # download file
        if download_file(url, dir_save, fname_save, verbose) and verbose:
            print('File already exists, skip downloading this url.')
            continue

        # check md5 sum (if available)
        if any(md5sum):
            if not check_file_integrity_md5(fname_save, md5sum):
                print('**WARNING**: md5 checksum does not match for file: {}'.format(fname_save))
                print('MD5 checksum(File/reference): {} - {}'.format(get_hash_value(fname_save), md5sum))

        # extract file
        extract_file(fname_save, dir_save, verbose)

        # remove downloaded file (if triggered by the user)
        if clean_cache:
            delete_file(fname_save)
