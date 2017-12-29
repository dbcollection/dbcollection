"""
Remove API class.
"""

from __future__ import print_function
import os
import sys
import shutil
import pkgutil
import json

import dbcollection.datasets as datasets
from dbcollection.core.cache import CacheManager
from dbcollection.core.loader import DataLoader

from .list_datasets import fetch_list_datasets


class RemoveAPI(object):
    pass
