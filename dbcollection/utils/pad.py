"""
Padding functions.
"""


def pad_list(listA, val=-1, length=None):
    """Pad list of lists with 'val' such that all lists have the same length.

    Parameters
    ----------
    listA : list
        List of lists of different sizes.
    val : number
        Value to pad the lists.
    length : number
        Total length of the list.

    Returns
    -------
    list
        A list of lists with the same same.

    Raises
    ------
        None

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
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    # get size of the biggest list
    if length:
        max_size = length
    else:
        max_size = len(max(listA, key=len))

    # pad all lists with the a padding value
    return [l + [val]*int(max_size-len(l)) for l in listA]


def pad_list2(listA, val=-1):
    """Pad list of lists of lists with 'val' such that all lists have the same length.

    Parameters
    ----------
    listA : list
        List of lists of lists of different sizes.
    val : number
        Value to pad the lists.

    Returns
    -------
    list
        A list of lists of lists with the same same.

    Raises
    ------
        None

    Examples
    --------
    Pad an uneven list of lists of lists with a value.

    >>> from dbcollection.utils.pad import pad_list2
    >>> pad_list2([[[1,2]],[[1],[2]]])
    [[[1, 2], [-1, -1]], [[1, -1], [2, -1]]]

    """
    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    max_nlists = max([len(l) for l in listA])
    max_list_size = max([len(li) for l in listA for li in l])

    out = []
    for l in listA:
        sublist = pad_list(l, val, max_list_size)
        if not len(sublist) == max_nlists:
            sublist += [[val] * int(max_list_size) for i in range(max_nlists - len(sublist))]
        out.append(sublist)

    return out


def unpad_list(listA, val=-1):
    """Unpad list of lists with which has values equal to 'val'.

    Parameters
    ----------
    listA : list
        List of lists of equal sizes.
    val : number
        Value to unpad the lists.

    Returns
    -------
    list
        A list of lists without the padding values.

    Raises
    ------
        None

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
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    if isinstance(listA[0], list):
        return [list(filter(lambda x: x != val, l)) for i, l in enumerate(listA)]
    else:
        return list(filter(lambda x: x != val, listA))


def unpad_list2(listA, val=-1):
    """Unpad list of lists of lists with which has values equal to 'val'.

    Parameters
    ----------
    listA : list
        List of lists or lists of equal sizes.
    val : number
        Value to unpad the lists.

    Returns
    -------
    list
        A list of lists of lists without the padding values.

    Raises
    ------
        None

    Examples
    --------
    Remove the padding values of a list of lists of lists.

    >>> from dbcollection.utils.pad import unpad_list2
    >>> unpad_list2([[[1,2,3,-1,-1],[5,6,-1,-1,-1]]])
    [[[1, 2, 3], [5, 6]]]
    >>> unpad_list2([[[1,2,3,-1,-1],[5,6,-1,-1,-1],[-1,-1,-1,-1,-1,-1]]])
    [[[1, 2, 3], [5, 6]]]

    """

    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    out = []
    for l in listA:
        sublist = unpad_list(l, val)
        out.append([li for li in sublist if li])

    return out