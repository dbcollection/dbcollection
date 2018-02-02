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
