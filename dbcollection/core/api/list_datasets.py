"""
Fetch the names of all available datasets for download.
"""


from __future__ import print_function
import sys
import pkgutil

import dbcollection.datasets as datasets


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
    for _, modname, ispkg in pkgutil.walk_packages(path=datasets.__path__,
                                                   prefix=datasets.__name__ + '.',
                                                   onerror=lambda x: None):
        if ispkg:
            paths = modname.split('.')
            db = get_dataset_attributes(modname)
            if db:
                dbname = paths[-1]
                db_list.update({dbname: db})
    return db_list


def get_dataset_attributes(name):
    """Loads a module, checks for key attributes and returns them."""
    __import__(name)
    module = sys.modules[name]
    try:
        db_fields = {
            "urls": getattr(module, 'urls'),
            "keywords": getattr(module, 'keywords'),
            "tasks": getattr(module, 'tasks'),
            "default_task": getattr(module, 'default_task'),
            "constructor": getattr(module, 'Dataset')
        }
        return db_fields
    except AttributeError:
        return None


def check_if_dataset_name_is_valid(name):
    """Check if the dataset name exists (is valid) in the list of available dataset for download"""
    available_datasets_list = fetch_list_datasets()
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)


def get_list_urls_dataset():
    available_datasets = fetch_list_datasets()
    dataset_urls = []
    for name in available_datasets:
        url_list = []
        urls = available_datasets[name]['urls']
        for url in urls:
            if isinstance(url, str):
                url_list.append(url)
            elif isinstance(url, dict):
                try:
                    url_ = url['url']
                    url_list.append(url_)
                except KeyError:
                    pass  # do nothing
            else:
                raise Exception('Unknown format when downloading urls: {}'.format(type(url)))
        # add list to the out dictionary
        dataset_urls.append((name, url_list))
    return dataset_urls
