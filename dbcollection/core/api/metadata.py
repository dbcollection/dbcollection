"""
List of methods and classes to manage the available dataset's
information (metadata) stored in the package.
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
    except AttributeError:
        db_fields = None
    return db_fields


def get_list_urls_dataset():
    available_datasets = fetch_list_datasets()
    dataset_urls = []
    for name in available_datasets:
        urls = available_datasets[name]['urls']
        url_list = get_urls_list(urls)
        dataset_urls.append((name, url_list))
    return dataset_urls


def get_urls_list(urls):
    url_list = []
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
    return url_list


class MetadataConstructor(object):
    """Manages a dataset's metadata and constructor states.

    Parameters
    ----------
    name : str
        Name of the dataset.

    Attributes
    ----------
    name : str
        Name of the dataset.
    dataset_manager : dict
        Metadata retrieved from the available datasets database.

    """

    def __init__(self, name):
        """Initialize class."""
        assert name, "Must input a valid dataset name."
        self.name = name
        self.metadata_datasets = self.get_metadata_datasets()
        self.dataset_manager = self.get_dataset_metadata_from_database(name)

    def get_metadata_datasets(self):
        return fetch_list_datasets()

    def get_dataset_metadata_from_database(self, name):
        """Returns the metadata and constructor class generator for a dataset."""
        try:
            return self.metadata_datasets[name]
        except KeyError:
            raise KeyError("Dataset '{}' does not exist in the database.".format(name))

    def get_default_task(self):
        """Returns the default task for the dataset."""
        return self.dataset_manager["default_task"]

    def parse_task_name(self, task):
        """Parse the input task string."""
        assert isinstance(task, str), "Must input a string as a valid task name."
        if task == '':
            task_parsed = self.get_default_task()
        elif task == 'default':
            task_parsed = self.get_default_task()
        else:
            task_parsed = task
        return task_parsed

    def get_tasks(self):
        """Returns the available tasks of the dataset."""
        return self.dataset_manager["tasks"]

    def get_keywords(self, task):
        """Get the keywords for a task of a dataset."""
        pass

    def get_constructor(self):
        """Returns the constructor class to generate the dataset's metadata."""
        return self.dataset_manager["constructor"]
