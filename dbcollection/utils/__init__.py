"""
Utility methods for url download, file extraction,
data padding and parsing, testing, etc.

Also, all third-party submodules are located under this module.
"""


from __future__ import print_function
from six import iteritems


def print_text_box(text):
    """Prints a simple text box.

    Parameters
    ----------
    text : str
        Header text.

    Examples
    --------
    Display a text box with a custom header

    >>> print_text_box('Some text to display!')
    >>>
    '-----------------------------'
    '--  Some text to display!  --'
    '-----------------------------'

    """
    assert text, "Must input a valid text string."
    str_display = '--  {display_text}  --'.format(display_text=text)
    str_separator = '-' * len(str_display)
    print('\n{separator}\n{text}\n{separator}\n'
          .format(separator=str_separator, text=str_display))


def nested_lookup(key, document, wild=False):
    """Lookup a key in a nested document recursively and yields a value.

    Parameters
    ----------
    key : str
        Key string to be found.
    document : dict/list
        List or dictionary to be searched.
    wild : bool, optional
        Exact key search (True) or case insensitive search (False).

    Returns
    -------
    List
        List of matching values / patterns.

    Examples
    --------
    Return all values from a dictionary that contain
    the key 'email'.

    >>> from dbcollection.utils import nested_lookup
    >>> nested_lookup('email', {'first_email': 'myemail@gmail.com', 'second_email': 'another@gmail.com'})
    ['myemail@gmail.com', 'another@gmail.com']

    """
    assert key, "Must input a valid key."
    assert document, "Must input a valid dictionary."
    if isinstance(document, list):
        for d in document:
            for result in nested_lookup(key, d, wild=wild):
                yield result

    if isinstance(document, dict):
        for k, v in iteritems(document):
            if key == k or (wild and key.lower() in k.lower()):
                yield v
            elif isinstance(v, dict):
                for result in nested_lookup(key, v, wild=wild):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in nested_lookup(key, d, wild=wild):
                        yield result


def merge_dicts(dict1, dict2):
    """Recursive dict merge.

    Recursively merges two dictionaries with different depths
    into a single dictionary. Also, the resulting output is
    returned as a generator.

    Parameters
    ----------
    dict1 : dict
        First dictinary.
    dict2 : dict
        Second dictionary.

    Returns
    -------
    dict
        Merged dictionary of two dictionaries.

    Note
    ----
    This method was based on @jterrace's stack overflow response:
    https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge

    """
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])
