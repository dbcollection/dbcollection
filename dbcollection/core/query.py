"""
Query API class.
"""


from __future__ import print_function

from dbcollection.core.cache import CacheManager


class QueryAPI(object):
    """Cache query API class.

    This class contains methods to query
    the cache registry for patterns.

    Parameters
    ----------
    pattern : str
        Field name used to search for a matching pattern in cache data.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    pattern : str
        Field name used to search for a matching pattern in cache data.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.
    query_list : list
        Stores all data found for the input pattern.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, pattern, verbose, is_test):
        """Initialize class."""
        assert pattern, 'Must input a valid pattern.'
        assert verbose is not None, 'verbose cannot be empty.'
        assert is_test is not None, 'is_test cannot be empty.'

        self.pattern = pattern
        self.verbose = verbose
        self.is_test = is_test
        self.query_list = []
        self.cache_manager = CacheManager(self.is_test)

    def run(self):
        """<stuff>.

        ** Main method **

        """
        self.match_pattern_root()
        self.match_pattern_info()
        self.match_pattern_datasets()
        self.match_pattern_categories()
        return self.query_list

    def match_pattern_root(self):
        """Check if there are any matches of the pattern with the root dict."""
        if self.pattern in self.cache_manager.data:
            data = {
                self.pattern: self.cache_manager.data[self.pattern]
            }
            self.append_data_to_query_list(data)

    def append_data_to_query_list(self, data):
        """Add pattern info + data to the a list."""
        self.query_list.append(data)

    def match_pattern_info(self):
        """Check if there are any matches of the pattern with the info section."""
        if self.pattern in self.cache_manager.data['info']:
            data = {
                'info': {
                    self.pattern: self.cache_manager.data['info'][self.pattern]
                }
            }
            self.append_data_to_query_list(data)

    def match_pattern_datasets(self):
        """Check if there are any matches of the pattern with the dataset section."""
        self.match_pattern_dataset_names()
        self.match_pattern_dataset_attributes()
        self.match_pattern_dataset_tasks()
        self.match_pattern_dataset_keywords()

    def match_pattern_dataset_names(self):
        """Check if the pattern matches any dataset name."""
        if self.pattern in self.cache_manager.data['dataset']:
            data = {
                'dataset': {
                    self.pattern: self.cache_manager.data['dataset'][self.pattern]
                }
            }
            self.append_data_to_query_list(data)

    def match_pattern_dataset_attributes(self):
        """Check if the pattern matches any dataset attributes."""
        for name in self.cache_manager.data['dataset']:
            if self.pattern in self.cache_manager.data['dataset'][name]:
                data = {
                    'dataset': {
                        name: {
                            self.pattern: self.cache_manager.data['dataset'][name][self.pattern]
                        }
                    }
                }
                self.append_data_to_query_list(data)

    def match_pattern_dataset_tasks(self):
        """Check if the pattern matches any dataset task."""
        for name in self.cache_manager.data['dataset']:
            if self.pattern in self.cache_manager.data['dataset'][name]['tasks']:
                data = {
                    'dataset': {
                        name: {
                            'tasks': {
                                self.pattern: self.cache_manager.data['dataset'][name]['tasks']
                                                                     [self.pattern]
                            }
                        }
                    }
                }
                self.append_data_to_query_list(data)

    def match_pattern_dataset_keywords(self):
        """Check if the pattern matches any dataset keyword."""
        for name in self.cache_manager.data['dataset']:
            if self.pattern in self.cache_manager.data['dataset'][name]['keywords']:
                data = {
                    'dataset': {
                        name: {
                            'keywords': {
                                self.pattern: self.cache_manager.data['dataset'][name]['keywords']
                            }
                        }
                    }
                }
                self.append_data_to_query_list(data)

    def match_pattern_categories(self):
        """Check if there are any matches of the pattern with the category section."""
        self.match_pattern_category_names()
        self.match_pattern_category_types()

    def match_pattern_category_names(self):
        """Check if the pattern matches any category name."""
        if self.pattern in self.cache_manager.data['category']:
            data = {
                'category': {
                    self.pattern: list(self.cache_manager.data['category'][self.pattern])
                }
            }
            self.append_data_to_query_list(data)

    def match_pattern_category_types(self):
        """Check if the pattern matches any category type."""
        for category in self.cache_manager.data['category']:
            if self.pattern in self.cache_manager.data['category'][category]:
                data = {
                    'category': {
                        category: [self.pattern, ]
                    }
                }
                self.append_data_to_query_list(data)
