"""
Data loading functions from files.
"""

import sys
import json
import scipy.io as scipy
import xmltodict
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


def open_read_file(fname, mode='r'):
    """Opens a file and returns the data.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    mode : str
        File open mode.

    Returns
    -------
    <any>
        File data.

    Raises
    ------
        None
    """
    try:
        return open(fname, mode)
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_txt(fname, mode='r'):
    """Load a .txt file to memory.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    mode : str
        File open mode.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    with open(fname, mode, encoding="utf-8") as f:
        data = f.read()

    return data.split('\n')


def load_matlab(fname):
    """Load a matlab file to memory.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    dict/list
        Data structure of the input matlab file.

    Raises
    ------
    IOError
        If the file cannot be opened.
    """
    try:
        return scipy.loadmat(fname)
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_json(fname):
    """Loads a json file to memory.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    dict/list
        Data structure of the input json file.

    Raises
    ------
    IOError
        If the file cannot be opened.
    """
    try:
        return json.load(open_read_file(fname))
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_pickle(fname):
    """Loads a pickle file to memory.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    dict/list
        Data structure of the input file.

    Raises
    ------
    IOError
        If the file cannot be opened.
    """
    try:
        if sys.version_info[0] == 2:
            return pickle.load(open_read_file(fname, 'rb'))
        else:
            return pickle.load(open_read_file(fname, 'rb'), encoding='latin1')
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_xml(fname):
    """Load+parse a xml file to memory.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    with open(fname) as fd:
        return xmltodict.parse(fd.read())