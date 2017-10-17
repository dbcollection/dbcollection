"""
Library of methods for padding/unpadding lists or
lists of lists with fill values.
"""


import itertools


def pad_list(listA, val=-1, length=None):
    """Pad list of lists with 'val' such that all lists have the same length.

    Parameters
    ----------
    listA : list
        List of lists of different sizes.
    val : number, optional
        Value to pad the lists.
    length : number, optional
        Total length of the list.

    Returns
    -------
    list
        A list of lists with the same same.

    Examples
    --------
    Pad an uneven list of lists with a value.

    >>> from dbcollection.utils.pad import pad_list
    >>> pad_list([[0,1,2,3],[45,6],[7,8],[9]])  # pad with -1 (default)
    [[0, 1, 2, 3], [4, 5, 6, -1], [7, 8, -1, -1], [9-1, -1, -1]]
    >>> pad_list([[1,2],[3,4]])  # does nothing
    [[1, 2], [3, 4]]
    >>> pad_list([[],[1],[3,4,5]], 0)  # pad lists with 0
    [[0, 0, 0], [1, 0, 0], [3, 4, 5]]
    >>> pad_list([[],[1],[3,4,5]], 0, 6)  # pad lists with 0 of size 6
    [[0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [3, 4, 5, 0, 0, 0]]

    """
    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, expected {}' \
                                    .format(type(listA), type(list))

    # get size of the biggest list
    if length:
        max_size = length
    else:
        max_size = len(max(listA, key=len))

    # pad all lists with the a padding value
    return [l + [val] * int(max_size - len(l)) for l in listA]


def unpad_list(listA, val=-1):
    """Unpad list of lists with which has values equal to 'val'.

    Parameters
    ----------
    listA : list
        List of lists of equal sizes.
    val : number, optional
        Value to unpad the lists.

    Returns
    -------
    list
        A list of lists without the padding values.

    Examples
    --------
    Remove the padding values of a list of lists.

    >>> from dbcollection.utils.pad import unpad_list
    >>> unpad_list([[1,2,3,-1,-1],[5,6,-1,-1,-1]])
    [[1, 2, 3], [5, 6]]
    >>> unpad_list([[5,0,-1],[1,2,3,4,5]], 5)
    [[0, -1], [1, 2, 3, 4]]

    """
    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, expected {}' \
                                    .format(type(listA), type(list))

    if isinstance(listA[0], list):
        return [list(filter(lambda x: x != val, l)) for i, l in enumerate(listA)]
    else:
        return list(filter(lambda x: x != val, listA))


def squeeze_list(listA, val=-1):
    """ Compact a list of lists into a single list.

    Squeezes (spaghettify) a list of lists into a single list.
    The lists are concatenated into a single one, and to separate
    them it is used a separating value to mark the split location
    when unsqueezing the list.

    Parameters
    ----------
    listA : list
        List of lists.
    val : number, optional
        Value to separate the lists.

    Returns
    -------
    list
        A list with all lists concatenated into one.

    Examples
    --------
    Compact a list of lists into a single list.

    >>> from dbcollection.utils.pad import squeeze_list
    >>> squeeze_list([[1,2], [3], [4,5,6]], -1)
    [1, 2, -1, 3, -1, 4, 5, 6]

    """
    concatA = [l + [val] for l in listA]
    out = [li for l in concatA for li in l]
    return out[:-1]


def unsqueeze_list(listA, val=-1):
    """ Unpacks a list into a list of lists.

    Returns a list of lists by splitting the input list
    into 'N' lists when encounters an element equal to
    'val'. Empty lists resulting of trailing values at the
    end of the list are discarded.

    Source: https://stackoverflow.com/questions/4322705/split-a-list-into-nested-lists-on-a-value

    Parameters
    ----------
    listA : list
        A list.
    val : int/float, optional
        Value to separate the lists.

    Returns
    -------
    list
        A list of lists.

    Examples
    --------
    Unpack a list into a list of lists.

    >>> from dbcollection.utils.pad import unsqueeze_list
    >>> unsqueeze_list([1, 2, -1, 3, -1, 4, 5, 6], -1)
    [[1, 2], [3], [4, 5, 6]]

    """
    return [list(g) for k, g in itertools.groupby(listA, lambda x:x in (val, )) if not k]
