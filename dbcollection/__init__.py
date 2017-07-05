"""
Dataset collection package.

This package allows to easily manage and load pre-processed datasets in an easy
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

# get version
from ._version import VERSION
__version__ = str(VERSION)

# load API methods
from .manager import load, download, process, add, remove, config_cache, query, info
