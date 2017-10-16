"""
A collection of popular datasets for deep learning
==================================================

**dbcollection** is a library for downloading/parsing/managing datasets via simple methods.
It was built from the ground up to be cross-platform (Windows, Linux, MacOS) and
cross-language (Python, Lua, Matlab, etc.). This is achieved by using the popular HDF5
file format to store (meta)data of manually parsed datasets and Python for scripting.
By doing so, this library can target any platform that supports Python and any language
that has bindings for HDF5.

This package allows to easily manage and load datasets in an easy and simple
way by using HDF5 files as metadata storage. By storing all the necessary metadata
to disk, it allows for huge datasets to be used in systems with reduced
memory usage. Also, once a dataset is setup, it is setup forever! Users can reuse it
as many times as they want/need for a myriad of tasks without having to setup a
dataset each time they hack some code. This lets users focus on more important tasks
fast prototyping without having to spend time managing datasets or creating/modyfing
scripts to load/fetch data from disk.

Main features
-------------

Here are some of key features dbcollection provides:

- Simple API to load/download/setup/manage datasets
- Simple API to fetch data of a dataset
- All data is stored in disk, resulting in reduced RAM usage (useful for large datasets)
- Datasets only need to be setup once
- Cross-platform (Windows, Linux, MacOs).
- Easily extensible to other languages that have support for HDF5 files
- Concurrent/parallel data access is possible thanks to the HDF5 file format
- Diverse list of popular datasets are available for use
- All datasets were manually parsed by someone, meaning that some of the quirks were
  already solved for you
"""


import pkg_resources

# API methods
from dbcollection.core.api import (download,
                                   process,
                                   load,
                                   add,
                                   remove,
                                   config_cache,
                                   query,
                                   info_cache,
                                   info_datasets,
                                   fetch_list_datasets)

# load the cache file
from dbcollection.core.cache import CacheManager
cache = CacheManager()

# package version
__version__ = pkg_resources.get_distribution('dbcollection').version

# load information about the available datasets for download
available_datasets_list = fetch_list_datasets()
