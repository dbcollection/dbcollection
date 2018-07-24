"""
Utility decorator methods.
"""


import sys


def display_message_processing(label):
    """Displays a message about processing a data field  metadata."""
    def decorator(fn):
        def decorated(*args, **kwargs):
            if args[0].verbose:
                sys.stdout.write("> Processing '{label}' metadata...".format(label=label))
            data = fn(*args, **kwargs)
            if args[0].verbose:
                sys.stdout.write(" Done.\n")
            return data
        return decorated
    return decorator


def display_message_load_annotations(fn):
    """Display message when loading data annotations from disk."""
    def decorated(*args, **kwargs):
        if args[0].verbose:
            sys.stdout.write("\n==> Loading data annotations from disk...")
        data = fn(*args, **kwargs)
        if args[0].verbose:
            sys.stdout.write(" Done.\n")
        return data
    return decorated
