"""
Library to load different types of file into memory.
"""


import sys
import json
import scipy.io as scipy
import xmltodict
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


def load_txt(fname, mode='r'):
    """Load a .txt file to memory.

    Parameters
    ----------
    fname : str
        File name + path.
    mode : str, optional
        File open mode.

    Returns
    -------
    list of strings

    """
    with open(fname, mode=mode, encoding="utf-8") as f:
        data = f.read()

    split_lines = data.split('\n')

    return split_lines[:-1]


def load_matlab(fname):
    """Load a matlab file to memory.

    Parameters
    ----------
    fname : str
        File name + path.

    Returns
    -------
    dict/list
        Data structure of the input matlab file.

    Raises
    ------
    IOError, OSError
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
        File name + path.

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
        return json.load(open(fname, mode='r'))
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_pickle(fname):
    """Loads a pickle file to memory.

    Parameters
    ----------
    fname : str
        File name + path.

    Returns
    -------
    dict/list
        Data structure of the input file.

    Raises
    ------
    IOError, OSError
        If the file cannot be opened.
    """
    try:
        if sys.version_info[0] == 2:
            return pickle.load(open(fname, mode='rb'))
        else:
            return pickle.load(open(fname, mode='rb'), encoding='latin1')
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def load_xml(fname):
    """Load+parse a xml file to memory.

    Parameters
    ----------
    fname : str
        File name + path.

    Returns
    -------
    dict
        Dictionary of the input file's data structure.
    """
    return xmltodict.parse(open(fname, mode='r').read())
