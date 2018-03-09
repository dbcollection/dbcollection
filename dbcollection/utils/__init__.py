"""
Utility methods for url download, file extraction,
data padding and parsing, testing, etc.

Also, all third-party submodules are located under this module.
"""


from __future__ import print_function


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
    """Lookup a key in a nested document recursively and yields a value."""
    if isinstance(document, list):
        for d in document:
            for result in nested_lookup(key, d, wild=wild):
                yield result

    if isinstance(document, dict):
        for k, v in document:
            if key == k or (wild and key.lower() in k.lower()):
                yield v
            elif isinstance(v, dict):
                for result in nested_lookup(key, v, wild=wild):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in nested_lookup(key, d, wild=wild):
                        yield result
