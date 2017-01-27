"""
Utility functions for data download/extraction/loading
"""


from __future__ import print_function
from clint.textui import progress
import urllib
import requests
import tarfile
import zipfile
import os
import errno
import hashlib
import scipy.io
import json
import sys
import numpy as np
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


#---------------------------------------------------------
# directory/file os management
#---------------------------------------------------------

def create_dir(dir_name, verbose=False):
    """
    Create directory if not existing.
    """
    if verbose:
        print('Creating directory: {}'.format(dir_name))
    os.makedirs(dir_name)


def remove_file(fname):
    """
    Check if the path exists and remove the file.
    """
    try:
        os.remove(fname)
    except OSError as err:
        if err.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise


#---------------------------------------------------------
# Download functions
#---------------------------------------------------------

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

    # join strings and return them
    return os.path.join(dir_save, url_fname)


def download_file(url, dir_name, fname_save, verbose=False):
    """
    Download a single file to disk.
    """
    # save file
    file_save_name = fname_save

    # check if the filename already exists
    if os.path.exists(file_save_name):
        return True

    # check if the path exists
    if not os.path.exists(dir_name):
        create_dir(dir_name, verbose)

    # download the file
    if verbose:
        download_single_file_progressbar(url, file_save_name)
    else:
        download_single_file_nodisplay(url, file_save_name)

    return True


def get_hash_value(fname):
    """
    Retrieve the checksum of a file.
    """
    return hashlib.md5(open(fname, 'rb').read()).hexdigest()


def check_file_integrity_md5(fname, md5sum):
    """
    Check the integrity of a file using md5 hash.
    """
    if not get_hash_value(fname) == md5sum:
        raise_exception('File check sum is invalid')


#---------------------------------------------------------
# Extraction functions (file extension)
#---------------------------------------------------------

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

    try:
        return methods[ext]
    except KeyError:
        raise_exception('Undefined file extension: ' + ext)


def extract_file(path, fname, verbose=False):
    """
    Extract a compressed file to disk.
    """
    file_name = path + fname

    if verbose:
        print('Extracting file to disk: ' + file_name)

    # check filename extension
    extension = get_file_extension(fname)

    # get extraction method
    extractor = get_extractor_method(extension)

    # extract file
    extractor(fname, path)


#---------------------------------------------------------
# Download + extract to disk
#---------------------------------------------------------

def download_extract_all(urls, md5sum, dir_save, clean_cache=False,verbose=True):
    """
    Download + extract all url files to disk.
    If clean_cache is true, it removes the download files.
    """
    # Check if urls is a str
    if isinstance(urls, str):
        urls = [urls]

    # download + extract data and remove temporary files
    for i, url in enumerate(urls):
        if verbose:
            print('Download url ' + str(i+1) + '/' + str(len(urls)))

        # get download save filename
        fname_save = url_get_filename(url, dir_save)

        # download file
        download_file(url, dir_save, fname_save, verbose)

        # check md5 sum (if available)
        if any(md5sum):
            check_file_integrity_md5(fname_save, md5sum)

        # extract file
        extract_file(dir_save, fname_save, verbose)

        # remove downloaded file (if triggered by the user)
        if clean_cache:
            remove_file(fname_save)


#---------------------------------------------------------
# File loading (.mat, .json, etc.)
#---------------------------------------------------------

def load_matlab(fname):
    """
    Load a matlab file to memory.
    """
    try:
        return scipy.io.loadmat(fname)
    except IOError:
        raise


def load_json(fname):
    """
    Loads a json file to memory.
    """
    try:
        with open(fname) as data_file:
            return json.load(data_file)
    except IOError:
        raise


def load_pickle(fname):
    """
    Loads a pickle file to memory.
    """
    # open file
    fo = open(fname, 'rb')

    # convert to dictionary
    data = pickle.load(fo, encoding='latin1')

    # close file
    fo.close()

    # return dictionary
    return data


#---------------------------------------------------------
# String manipulation
#---------------------------------------------------------

def str_to_ascii(s):
    """
    Convert string to ascii list
    """
    return np.array([ord(c) for c in s], dtype=np.uint8)


def ascii_to_str(a):
    """
    Convert ascii list to a string
    """
    return "".join([chr(item) for item in a])


def convert_str_ascii(inp_str):
    """
    Convert a list of strings into a numpy array (uint8)
    """
    # check if list
    if isinstance(inp_str, list):
        # get max size of the list strings
        max_size = max([len(a) for a in inp_str])

        # allocate array
        ascii_array = np.zeros([len(inp_str), max_size+1], dtype=np.uint8)

        # iteratively copy data to the array
        for i, val in enumerate(inp_str):
            ascii_array[i, :len(val)] = str_to_ascii(val)

        return ascii_array
    else:
        return str_to_ascii(inp_str)


def convert_ascii_str(np_array):
    """
    Convert a numpy array to a string (or a list of strings)
    """
    list_str = np_array.tolist()
    if np_array.ndim == 1:
        return ascii_to_str(list_str)
    else:
        return [ascii_to_str(list(filter(lambda x: x > 0, str_))) for str_ in list_str]


