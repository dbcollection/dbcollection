"""
Dataset collection package.

This package allows to easily manage and load datasets in an easy
way by using hdf5 files as metadata storage. By storing all the necessary metadata
on disk, memory RAM can be allocated to other functionalities without noticable
performance lost, and allows for huge datasets to be used in systems with limited
memory capacity.

This package enables the user to set and configure a dataset once and reuse it as
many times it for multiple tasks without manually having te need to setup a
dataset every time.

<TODO: finish the header file explanation>
"""


#from dbcollection import manager, utils


# load API methods
from dbcollection.core.download import download
from dbcollection.core.process import process
from dbcollection.core.load import load
from dbcollection.core.add import add
from dbcollection.core.remove import remove
from dbcollection.core.config import config_cache
from dbcollection.core.query import query
from dbcollection.core.info import info_cache, info_datasets

# open/load the cache file
from dbcollection.core.cache import CacheManager
cache = CacheManager()

# load information about the available datasets for download
from dbcollection.core.db import fetch_list_datasets
available_datasets_list = fetch_list_datasets()

# get package version
from ._version import __version__



