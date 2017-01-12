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


def download_file(url, dir_name, fname_save, verbose=False):
    """
    Download a single file to disk.
    """
    # save file
    file_save_name = dir_name+fname_save

    # check if the path exists
    if not os.path.exists(dir_name):
        create_dir(dir_name, verbose)

    # download the file
    if verbose:
        print('Downloading {} to: {}'.format(url, file_save_name))
        r = requests.get(url, stream=True)
        with open(file_save_name, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
    else:
        with urllib.request.urlopen(url) as response, open(file_save_name, 'wb') as out_file:
          data = response.read() # a `bytes` object
          out_file.write(data)


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


def extract_file(path, fname, verbose=False):
    """
    Extract a file to disk.
    """
    file_name = path + fname

    if verbose:
        print('Extracting file to disk: {}'.format(file_name))

    # check filename extension
    extension = get_file_extension(fname)

    if extension == 'zip':
        extract_file_zip(file_name, path)
    elif extension == 'tar' or extension == 'gz':
        extract_file_tar(file_name, path)
    else:
        raise Exception('Undefined extension: {}'.format(extension))

def remove_file(fname):
    """
    Check if the path exists.
    """
    if os.path.exists(fname):
        os.remove(fname)
