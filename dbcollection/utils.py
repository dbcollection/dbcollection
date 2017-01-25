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
import hashlib
import scipy.io
import json
import sys
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
    if os.path.exists(fname):
        os.remove(fname)


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
    file_save_name = fname_save

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


#---------------------------------------------------------
# Download + extract to disk
#---------------------------------------------------------

def download_extract_all(urls, md5sum, dir_save, clean_cache,verbose):
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
    data = pickle.load(fo)

    # close file
    fo.close()

    # return dictionary
    return data



