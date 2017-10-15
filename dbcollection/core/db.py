"""
Dataset utility methods/classes.
"""

from __future__ import print_function
import sys
import pkgutil

import dbcollection.datasets as datasets


def get_dataset_attributes(name):
    __import__(name)
    module = sys.modules[name]
    try:
        db_fields =  {
            "urls": getattr(module, 'urls'),
            "keywords": getattr(module, 'keywords'),
            "tasks": getattr(module, 'tasks'),
            "default_task": getattr(module, 'default_task'),
            "constructor": getattr(module, 'Dataset')
        }
        return db_fields
    except AttributeError:
        return None


def fetch_list_datasets():
    """Get all datasets into a dictionary.

    Returns
    -------
    dict
        A dictionary where keys are names of datasets and values are
        a dictionary containing information like urls or keywords of
        a dataset.
    """
    db_list = {}
    for importer, modname, ispkg in pkgutil.walk_packages(path=datasets.__path__,
                                                          prefix=datasets.__name__ + '.',
                                                          onerror=lambda x: None):
        if ispkg:
            paths = modname.split('.')
            db = get_dataset_attributes(modname)
            if db:
                dbname = paths[-1]
                db_list.update({dbname: db})
    return db_list
