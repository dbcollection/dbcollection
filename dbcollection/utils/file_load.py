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
    """Loads a .txt file to memory.

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
    assert fname, 'Must input a valid file name.'
    with open(fname, mode=mode, encoding="utf-8") as f:
        data = f.read()
    split_lines = data.split('\n')
    return split_lines[:-1]


def load_matlab(fname):
    """Loads a matlab file to memory.

    Parameters
    ----------
    fname : str
        File name + path.

    Returns
    -------
    dict/list
        Data structure of the input matlab file.

    """
    assert fname, 'Must input a valid file name.'
    return scipy.loadmat(fname)


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

    """
    assert fname, 'Must input a valid file name.'
    return json.load(open(fname, mode='r'))


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

    """
    assert fname, 'Must input a valid file name.'
    if sys.version_info[0] == 2:
        return pickle.load(open(fname, mode='rb'))
    else:
        return pickle.load(open(fname, mode='rb'), encoding='latin1')


def load_xml(fname):
    """Loads and parses a xml file to a dictionary.

    Parameters
    ----------
    fname : str
        File name + path.

    Returns
    -------
    dict
        Dictionary of the input file's data structure.
    """
    assert fname, 'Must input a valid file name.'
    return xmltodict.parse(open(fname, mode='r').read())
