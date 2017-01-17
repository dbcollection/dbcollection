#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from clint.textui import progress
import urllib
import requests
import tarfile
import zipfile
import os


def create_dir(dir_name, verbose=False):
    """
    Create directory if not existing.
    """
    if verbose:
        print('Creating directory: {}'.format(dir_name))
    os.makedirs(dir_name)


def download_single_file_progressbar(url, file_save_name):
    """
    Download a file (display a progress bar).
    """
    print('Downloading {} to: {}'.format(url, file_save_name))
    r = requests.get(url, stream=True)
    with open(file_save_name, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def download_single_file_nodisplay(url, file_save_name):
    """
    Download a file (no display text).
    """
    with urllib.request.urlopen(url) as response, open(file_save_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)


def url_get_filename(url, dir_save):
    """
    Extract filename from the url string
    """
    # split url string
    url_fname = url.split('/')[-1]

    # save file
    if dir_save[-1] == '/':
        file_save_name = dir_save + url_fname
    else:
        file_save_name = dir_save + '/' + url_fname

    return file_save_name


def download_file(url, dir_name, fname_save, verbose=False):
    """
    Download a single file to disk.
    """
    # save file
    file_save_name = url_get_filename(url, dir_name)

    # check if the path exists
    if not os.path.exists(dir_name):
        create_dir(dir_name, verbose)

    # download the file
    if verbose:
        download_single_file_progressbar(url, file_save_name)
    else:
        download_single_file_nodisplay(url, file_save_name)

    return True



def get_file_extension(fname):
    """
    Retrieve filename extension.
    """
    str_split = fname.split('.')
    return str_split[-1]


def extract_file_zip(fname, path):
    """
    Extract zip file.
    """
    zip_ref = zipfile.ZipFile(fname, 'r')
    zip_ref.extractall(path)
    zip_ref.close()


def extract_file_tar(fname, path):
    """
    Extract .tar file.
    """
    tar = tarfile.open(fname)
    tar.extractall(path)
    tar.close()


def raise_exception(str):
    """
    Raise an exception.
    """
    raise Exception(str)


def get_extractor_method(ext):
    """
    Returns a method based on the input extension. Raises
    an exception if the method is not defined.
    """
    methods = {
        "zip":extract_file_zip,
        "tar":extract_file_tar,
        "gz":extract_file_tar
    }

    if ext in methods.keys():
        return methods[ext]
    else:
        raise_exception('Undefined file extension: ' + ext)


def extract_file(path, fname, verbose=False):
    """
    Extract a compressed file to disk.
    """
    file_name = path + fname

    if verbose:
        print('Extracting file to disk: {}'.format(file_name))

    # check filename extension
    extension = get_file_extension(fname)

    # get extraction method
    extractor = get_extractor_method(extension)

    # extract file
    extractor(fname, path)


def remove_file(fname):
    """
    Check if the path exists and remove the file.
    """
    if os.path.exists(fname):
        os.remove(fname)


def download_extract_all(urls, dir_save, clean_cache,verbose):
    """
    Download + extract all url files to disk.
    If clean_cache is true, it removes the download files.
    """
     # download + extract data and remove temporary files
    for url in urls:
        # get download save filename
        fname_save = url_get_filename(url, dir_save)

        # download file
        download_file(url, dir_save, fname_save, verbose)

        # extract file
        extract_file(dir_save, fname_save, verbose)

        # remove downloaded file (if triggered by the user)
        if clean_cache:
            remove_file(fname_save)