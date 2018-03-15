"""
A collection of popular datasets for deep learning
==================================================

**dbcollection** is a library for downloading/parsing/managing datasets via simple methods.
It was built from the ground up to be cross-platform (**Windows**, **Linux**, **MacOS**) and
cross-language (**Python**, **Lua**, **Matlab**, etc.). This is achieved by using the popular
``HDF5`` file format to store (meta)data of manually parsed datasets and the power of Python for
scripting. By doing so, this library can target any platform that supports Python and
any language that has bindings for ``HDF5``.

This package allows to easily manage and load datasets by using ``HDF5`` files to store
metadata. By storing all the necessary metadata to disk, managing either big or small
datasets has an equal or very similar impact on the system's resource usage.
Also, once a dataset is setup, it is setup forever! This means users can reuse any
previously set dataset as many times as needed without having to set it each time they
are used.

**dbcollection** allows users to focus on more important tasks like prototyping new models
or testing them in different datasets without having to incur the loss of spending time managing
datasets or creating/modyfing scripts to load/fetch data by taking advantage
of the work of the community that shared these resources.

Main features
-------------

Here are some of key features dbcollection provides:

- Simple API to load/download/setup/manage datasets.
- Simple API to fetch data from a dataset.
- Store and pull data from disk or from memory, you choose!
- Datasets only need to be set/processed once, so next time you use it it will load instantly!
- Cross-platform (**Windows**, **Linux**, **MacOs**).
- Cross-language (**Python**, **Lua/Torch7**, **Matlab**).
- Easily extensible to other languages that support ``HDF5`` files format.
- Concurrent/parallel data access thanks to ``HDF5``.
- Contains a diverse (and growing!) list of popular datasets for machine-, deep-learning tasks
  (*object detection*, *action recognition*, *human pose estimation*, etc.)

"""


import pkg_resources

# API methods
from dbcollection.core.api.download import download
from dbcollection.core.api.process import process
from dbcollection.core.api.load import load
from dbcollection.core.api.add import add
from dbcollection.core.api.remove import remove
from dbcollection.core.api.cache import cache
from dbcollection.core.api.info import info
from dbcollection.core.api.metadata import fetch_list_datasets

# load the cache file
from dbcollection.core.manager import CacheManager
cache_manager = CacheManager()

# package version
__version__ = pkg_resources.get_distribution('dbcollection').version

# load information about the available datasets for download
available_datasets_list = fetch_list_datasets()
