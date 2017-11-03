"""
String-to-ascii and ascii-to-string convertion methods.
"""


import numpy as np


def str_to_ascii(input_str):
    """Converts a string to an ascii encoded numpy array.

    Converts a single string of characters into a numpy array
    coded as ascii.

    Parameters
    ----------
    input_str : str
        String data.

    Returns
    -------
    np.ndarray
        Uni-dimensional array of char values encoded in ASCII format.

    Examples
    --------
    Convert a string to numpy array.

    >>> from dbcollection.utils.string_ascii import str_to_ascii
    >>> str_to_ascii('string1')
    array([115, 116, 114, 105, 110, 103,  49], dtype=uint8)

    """
    return np.array([ord(c) for c in input_str], dtype=np.uint8)


def ascii_to_str(input_array):
    """Converts an ascii encoded numpy array to a string.

    Parameters
    ----------
    input_array : np.ndarray
        Input array vector (should be of type dtype=numpy.uint8)

    Returns
    -------
    str
       Single string.

    Examples
    --------
    Convert a numpy array to string.

    >>> import numpy as np
    >>> from dbcollection.utils.string_ascii import ascii_to_str
    >>> ascii_to_str(np.array([115, 116, 114, 105, 110, 103,  49], dtype=uint8))
    'string1'

    """
    return "".join([chr(item) for item in input_array])


def convert_str_to_ascii(inp_str):
    """Convert a list of strings into an ascii encoded numpy array.

    Converts a string or list of strings to a numpy array. The array size is
    defined by the size of string plus one. This is needed for ascii to str
    convertion in lua using ffi.string() which expects a 0 at the end of an
    array.

    If a list of strings is used, the size of the array is defined by the size
    of the longest string (plus one), and zero padded to maitain the array
    shape.

    Parameters
    ----------
    inp_str : str/list
        String or list of strings to convert to an ascii array.

    Returns
    -------
    np.ndarray
        Single/multi-dimensional array of ASCII encoded strings.

    Examples
    --------
    Example1: Convert a string to a numpy array encoded into ASCII values.

    >>> from dbcollection.utils.string_ascii import convertstr_to_ascii
    >>> convertstr_to_ascii('string1')
    array([115, 116, 114, 105, 110, 103,  49,   0], dtype=uint8)

    Example2: Convert a list of lists into an ASCII array.

    >>> from dbcollection.utils.string_ascii import convertstr_to_ascii
    >>> convertstr_to_ascii(['string1', 'string2', 'string3'])
    array([[115, 116, 114, 105, 110, 103,  49,   0],
        [115, 116, 114, 105, 110, 103,  50,   0],
        [115, 116, 114, 105, 110, 103,  51,   0]], dtype=uint8)

    """
    # check if list
    if not isinstance(inp_str, list):
        inp_str = [inp_str]

    # get max size of the list strings
    max_size = max([len(a) for a in inp_str])

    # allocate array
    ascii_array = np.zeros([len(inp_str), max_size + 1], dtype=np.uint8)

    # iteratively copy data to the array
    for i, val in enumerate(inp_str):
        ascii_array[i, :len(val)] = str_to_ascii(val)

    if len(inp_str) > 1:
        return ascii_array
    else:
        return ascii_array[0]


def convert_ascii_to_str(input_array):
    """Convert a numpy array to a string (or a list of strings)

    Parameters
    ----------
    input_array : np.ndarray
        Array of strings encoded in ASCII format.

    Returns
    -------
    str/list
        String or list of strings.

    Examples
    --------
    Convert a numpy array to a string.

    >>> from dbcollection.utils.string_ascii import convert_ascii_to_str
    >>> import numpy as np
    >>> # ascii format of 'string1'
    >>> tensor = np.array([[115, 116, 114, 105, 110, 103, 49, 0]], dtype=np.uint8)
    >>> convert_ascii_to_str(tensor)
    ['string1']

    """
    list_str = input_array.tolist()
    if input_array.ndim > 1:
        return [ascii_to_str(list(filter(lambda x: x > 0, str_))) for str_ in list_str]
    else:
        return ascii_to_str(list(filter(lambda x: x > 0, list_str)))
