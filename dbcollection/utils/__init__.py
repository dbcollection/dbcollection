"""
Utility methods for url download, file extraction,
data padding and parsing, testing, etc.

Also, all third-party submodules are located under this module.
"""


from __future__ import print_function
from six import iteritems


def print_text_box(text):
    """Prints a simple text box.

    Example:
        >>> print_text_box('Some text to display!')
        >>>
        '-----------------------------'
        '--  Some text to display!  --'
        '-----------------------------'

    """
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
