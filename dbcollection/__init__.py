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
from ._version import __version__

# load information about the available datasets for download
available_datasets_list = fetch_list_datasets()
