"""
Data loading functions from files.
"""

import sys
import json
import scipy.io as scipy
if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


def load_matlab(fname):
    """
    Load a matlab file to memory.

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
        If the file cannot be oppened.
    """
    try:
        return scipy.loadmat(fname)
    except IOError:
        raise IOError('Error opening file: {}'.format(fname))


def load_json(fname):
    """
    Loads a json file to memory.

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
        If the file cannot be oppened.
    """
    with open(fname) as (data_file, err):
        if err:
            raise IOError(err)
        else:
            return json.load(data_file)


def load_pickle(fname):
    """
    Loads a pickle file to memory.

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
        If the file cannot be oppened.
    """
    with open(fname, 'rb') as (data_file, err):
        if err:
            raise IOError(err)
        else:
            return pickle.load(data_file, encoding='latin1')
