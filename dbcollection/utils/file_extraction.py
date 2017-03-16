"""
File extraction functions for common file types: matlab, json, etc.
"""


from __future__ import print_function
import os
import tarfile
import zipfile


def extract_file_zip(fname, dir_path):
    """Extract zip file.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    dir_path : str
        Directory path on disk to extract the file.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(dir_path)


def extract_file_tar(fname, dir_path):
    """Extract .tar file.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    dir_path : str
        Directory path on disk to extract the file.

    Returns
    -------
        None

    Raises
    ------
    IOError
        In case the file cannot be opened.
    """
    with tarfile.open(fname) as tar:
        tar.extractall(dir_path)


def get_extractor_method(ext):
    """Fetch extractor method from list.

    A method based on the input extension is returned based on an
    input string. An exception is raised if the method is not defined.

    Parameters
    ----------
    ext : str
        Extension string.

    Returns
    -------
    function object
        Method to extract files with the given extension.

    Raises
    ------
        None
    """
    methods = {
        "zip":extract_file_zip, ".zip":extract_file_zip,
        "tar":extract_file_tar, ".tar":extract_file_tar,
        "gz":extract_file_tar, ".gz":extract_file_tar
    }

    try:
        return methods[ext]
    except KeyError:
        raise KeyError('Undefined file extension: ' + ext)


def extract_file(fname, dir_path, verbose=False):
    """Extract a compressed file to disk.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    dir_path : str
        Directory path on disk to extract the file.
    verbose : bool
        Displays a message on the screen.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    if verbose:
        print('Extracting file to disk: {}'.format(dir_path))

    # check filename extension
    extension = os.path.splitext(fname)[1]

    # get extraction method
    extractor = get_extractor_method(extension)

    # extract file
    extractor(fname, dir_path)
