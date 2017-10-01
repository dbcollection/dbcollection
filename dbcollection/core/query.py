"""
API methods for querying the cache.
"""

from __future__ import print_function

from dbcollection.core.cache import CacheManager


def query(pattern='info', is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess.

    Parameters:
    -----------
	pattern : str
        Field name used to search for a matching pattern in cache data.
        (optional, default='info')
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # init list
    query_list = {}

    # check info / dataset lists first
    if pattern in cache_manager.data:
        query_list.update({pattern : cache_manager.data[pattern]})

    # match default paths
    if pattern in cache_manager.data['info']:
        query_list.update({pattern : cache_manager.data['info'][pattern]})

    # match datasets/tasks
    if pattern in cache_manager.data['dataset']:
        query_list.update({pattern : cache_manager.data['dataset'][pattern]})

    # match datasets/tasks
    if pattern in cache_manager.data['category']:
        query_list.update({pattern : list(cache_manager.data['category'][pattern].keys())})

    for name in cache_manager.data['dataset']:
        if pattern in cache_manager.data['dataset'][name]:
            query_list.update({pattern : cache_manager.data['dataset'][name][pattern]})
        if pattern in cache_manager.data['dataset'][name]['tasks']:
            query_list.update({pattern : cache_manager.data['dataset'][name]['tasks'][pattern]})
        if pattern in cache_manager.data['dataset'][name]['keywords']:
            query_list.update({pattern : cache_manager.data['dataset'][name]['keywords'][pattern]})

    return query_list
