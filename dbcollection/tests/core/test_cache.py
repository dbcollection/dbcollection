"""
Test dbcollection/utils/cache.py.
"""


import os
import random
import pytest

from dbcollection.core.cache import (
    CacheManager,
    CacheManagerInfo,
    CacheManagerDataset,
    CacheManagerCategory
)


# -----------------------------------------------------------
# Test data setup
# -----------------------------------------------------------

class DataGenerator:
    """Generates sample data for testing the CacheManager class

    This class generates a sample data structure thet a cache file will
    contain wityh information about paths, datasets and categories of
    datasets.

    Example
    =======
    The generated data should resemble something like the following:

    data = {
        "info": {
            "root_cache_dir": '/some/path/dbcollection',
            "root_download_dir": '/some/path/dbcollection/downloads',
        },
        "dataset": {
            "datasetA": {
                "data_dir": 'some/path/dbcollection/downloads/datasetA'
                "keywords": ["categoryA", "categoryB", "categoryC"]
                "tasks": {
                    "taskA_i": {
                        "filename": 'some/path/dbcollection/datasetA/taskA_i.h5',
                        "categories": ["categoryB"]
                    },
                    "taskA_ii": {
                        "filename": 'some/path/dbcollection/datasetA/taskA_ii.h5',
                        "categories": ["categoryA"]
                    },
                    "taskA_iii": {
                        "filename": 'some/path/dbcollection/datasetA/taskA_iii.h5',
                        "categories": ["categoryA", "categoryC"]
                    }
                }
            },
            "datasetB": {
                "data_dir": 'some/path/dbcollection/downloads/datasetB'
                "keywords": ["categoryC", "categoryD"]
                "tasks": {
                    "taskB_i": {
                        "filename": 'some/path/dbcollection/datasetB/taskB_i.h5',
                        "categories": ["categoryD"]
                    },
                    "taskB_ii": {
                        "filename": 'some/path/dbcollection/datasetB/taskB_ii.h5',
                        "categories": ["categoryC"]
                    }
                }
            },
            "datasetC": {
                "data_dir": 'some/path/dbcollection/downloads/datasetC'
                "keywords": ["categoryA", "categoryB", "categoryC"]
                "tasks": {
                    "taskC_i": {
                        "filename": 'some/path/dbcollection/datasetC/taskC_i.h5',
                        "categories": ["categoryA", categoryB", "categoryC"]
                    },
                    "taskC_ii": {
                        "filename": 'some/path/dbcollection/datasetC/taskC_ii.h5',
                        "categories": ["categoryB", "categoryC"]
                    },
                    "taskC_iii": {
                        "filename": 'some/path/dbcollection/datasetC/taskC_iii.h5',
                        "categories": ["categoryA", "categoryC"]
                    },
                    "taskC_iv": {
                        "filename": 'some/path/dbcollection/datasetC/taskC_iv.h5',
                        "categories": ["categoryC"]
                    }
                }
            },
            .
            .
            .
        },
        "category": {
            "categoryA": {
                "datasetA": ["taskA_i", "taskA_ii", "taskA_iii"],
                "datasetC": ["taskC_i", "taskC_iv"]
            },
            "categoryB": {
                "datasetC": ["taskC_i", "taskC_ii"]
            },
            "categoryC": {
                "datasetA": ["taskA_i", "taskC_i", "taskC_ii", "taskC_iii", "taskC_iv"],
                "datasetB": ["taskB_ii"]
            },
            .
            .
            .
        }
    }

    """

    def __init__(self):
        self.base_path = "/some/path/"
        self.list_datasets = ["dataset" + str(i) for i in range(10)]
        self.list_categories = ["category" + str(i) for i in range(10)]
        self.list_tasks = ["task" + str(i) for i in range(10)]

        self.info = self.get_info_data()
        self.datasets = self.get_datasets_data()
        self.categories = self.get_categories_data()
        self.data = {
            "info": self.info,
            "dataset": self.datasets,
            "category": self.categories
        }

    def get_info_data(self):
        """Returns the paths data for the info cache field."""
        return {
            "root_cache_dir": os.path.join(self.base_path, "dbcollection"),
            "root_download_dir": os.path.join(self.base_path, "dbcollection", "downloads"),
        }

    def get_datasets_data(self):
        """Returns the dataset's data for the dataset cache field."""
        return self.generate_random_datasets()

    def generate_random_datasets(self):
        """Generates random datasets."""
        datasets = {}
        for dataset in self.list_datasets:
            data = {}
            data["data_dir"] = os.path.join(self.info["root_download_dir"], dataset)
            data["tasks"] = self.generate_random_tasks(dataset)
            data["keywords"] = self.get_keyword_list(data["tasks"])
            datasets.update({dataset: data})
        return datasets

    def generate_random_tasks(self, dataset):
        """Generates random dictionaries of tasks."""
        tasks = {}
        random_tasks = self.get_random_size_list_tasks()
        for task in random_tasks:
            tasks.update({
                task: {
                    "filename": os.path.join(self.info["root_cache_dir"], dataset, task + '.h5'),
                    "category": self.get_random_size_list_categories()
                }
            })
        return tasks

    def get_random_size_list_tasks(self):
        """Returns a random sized list of random tasks."""
        num_tasks = random.randint(1, len(self.list_tasks))
        tasks = self.list_tasks.copy()
        random.shuffle(tasks)
        return list(set(tasks[:num_tasks]))

    def get_random_size_list_categories(self):
        """Returns a random sized list of random categories."""
        num_categories = random.randint(1, len(self.list_categories))
        categories = self.list_categories.copy()
        random.shuffle(categories)
        return list(set(categories[:num_categories]))

    def get_keyword_list(self, tasks):
        """Returns a list of all unique task categories."""
        keywords = []
        for task in tasks:
            keywords.extend(tasks[task]["category"])
        return list(set(keywords))

    def get_categories_data(self):
        """Returns the category's data for the category cache field."""
        return self.generate_random_categories()

    def generate_random_categories(self):
        """Generates random categories."""
        categories = {}
        used_categories = self.get_list_categories_used(self.datasets)
        for category in used_categories:
            categories.update({
                category: self.get_datasets_tasks_by_category(category)
            })
        return categories

    def get_list_categories_used(self, datasets):
        """Returns a list of all categories available in the datasets data."""
        categories_used = []
        for dataset in datasets:
            categories_used.extend(datasets[dataset]['keywords'])
        return list(set(categories_used))

    def get_datasets_tasks_by_category(self, category):
        """Returns a list of all datasets and tasks that have the category name."""
        list_datasets_tasks = {}
        for dataset in self.datasets:
            list_datasets_tasks.update({
                dataset: self.get_tasks_by_category(self.datasets[dataset]["tasks"], category)
            })
        return list_datasets_tasks

    def get_tasks_by_category(self, tasks, category):
        """Returns a list of tasks that contains the category name"""
        tasks_category = []
        for task in tasks:
            if category in tasks[task]['category']:
                tasks_category.append(task)
        return tasks_category


# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------

test_data = DataGenerator()


@pytest.fixture()
def cache_manager(mocker):
    mocker.patch.object(CacheManager, "read_data_cache", return_value=test_data.data)
    cache = CacheManager()
    return cache


class TestCacheManager:
    """Unit tests for the CacheManager class."""

    def test_CacheManager__init(self, mocker):
        mocker.patch.object(CacheManager, "read_data_cache", return_value=test_data.data)
        cache = CacheManager()
        assert os.path.basename(cache.cache_filename) == 'dbcollection.json'

    def test___get_cache_filename(self, cache_manager):
        filename = cache_manager._get_cache_filename()
        assert os.path.basename(filename) == 'dbcollection.json'

    def test_read_data_cache__file_exists(self, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = True
        mocker.patch.object(CacheManager, "read_data_cache_file", return_value=test_data.data)
        cache = CacheManager()
        assert cache.read_data_cache() == test_data.data

    def test_read_data_cache__file_missing(self, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = False
        mocker.patch.object(CacheManager, "_empty_data", return_value=test_data.data)
        mocker.patch.object(CacheManager, "write_data_cache")
        cache = CacheManager()
        assert cache.read_data_cache() == test_data.data

    def test_write_data_cache(self, mocker, cache_manager):
        new_data = {"some": "data"}
        mocker.patch("builtins.open")
        mocker.patch('json.dump')
        cache_manager.write_data_cache(new_data)
        assert cache_manager.data == new_data

    def test__set_cache_dir(self, mocker, cache_manager):
        mocker.patch.object(CacheManager, "write_data_cache")
        new_path = "/new/cache/path"
        cache_manager._set_cache_dir(new_path)
        assert cache_manager.cache_dir == new_path

    def test__get_cache_dir(self, mocker, cache_manager):
        assert cache_manager.cache_dir == test_data.data['info']['root_cache_dir']

    def test__set_download_dir(self, mocker, cache_manager):
        mocker.patch.object(CacheManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"
        cache_manager._set_download_dir(new_path)
        assert cache_manager.download_dir == new_path

    def test__get_download_dir(self, mocker, cache_manager):
        assert cache_manager.download_dir == test_data.data['info']['root_downloads_dir']

    def test_reset_download_dir(self, mocker, cache_manager):
        mocker.patch.object(CacheManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"
        cache_manager._set_download_dir(new_path)
        assert cache_manager.download_dir == new_path
        cache_manager.reset_download_dir()
        assert cache_manager.download_dir == cache_manager._get_default_downloads_dir()
        assert cache_manager.download_dir is not new_path

class TestCacheManagerInfo:
    """Unit tests for the CacheManagerInfo class."""

    def test_CacheManagerDataset__init(self):
        pass


class TestCacheManagerDataset:
    """Unit tests for the CacheManagerDataset class."""

    def test_CacheManagerDataset__init(self):
        pass


class TestCacheManagerCategory:
    """Unit tests for the CacheManagerCategory class."""

    def test_CacheManagerCategory__init(self):
        pass
