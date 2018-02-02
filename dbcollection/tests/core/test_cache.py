"""
Test dbcollection/utils/cache.py.
"""


import os
import random
import pytest

from dbcollection.core.cache import (
    CacheManager,
    CacheDataManager,
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
                    "categories": self.get_random_size_list_categories()
                }
            })
        return tasks

    def get_random_size_list_tasks(self):
        """Returns a random sized list of random tasks."""
        num_tasks = random.randint(1, len(self.list_tasks))
        tasks = self.list_tasks
        random.shuffle(tasks)
        return sorted(tasks[:num_tasks])

    def get_random_size_list_categories(self):
        """Returns a random sized list of random categories."""
        num_categories = random.randint(1, len(self.list_categories))
        categories = self.list_categories
        random.shuffle(categories)
        return sorted(list(set(categories[:num_categories])))

    def get_keyword_list(self, tasks):
        """Returns a list of all unique task categories."""
        keywords = []
        for task in tasks:
            keywords.extend(tasks[task]["categories"])
        return sorted(list(set(keywords)))

    def get_categories_data(self):
        """Returns the category's data for the category cache field."""
        categories = {}
        used_categories = self._get_list_categories_used(self.datasets)
        for category in used_categories:
            categories.update({
                category: self._get_datasets_tasks_by_category(self.datasets, category)
            })
        return categories

    def _get_list_categories_used(self, datasets):
        """Returns a list of all categories available in the datasets data."""
        categories_used = []
        for dataset in datasets:
            categories_used.extend(datasets[dataset]['keywords'])
        return list(sorted(set(categories_used)))

    def _get_datasets_tasks_by_category(self, datasets, category):
        """Returns a list of all datasets and tasks that have the category name."""
        list_datasets_tasks = {}
        for dataset in datasets:
            list_datasets_tasks.update({
                dataset: self._get_tasks_by_category(datasets[dataset]["tasks"], category)
            })
        return list_datasets_tasks

    def _get_tasks_by_category(self, tasks, category):
        """Returns a list of tasks that contains the category name."""
        matching_tasks = []
        for task in tasks:
            if category in tasks[task]["categories"]:
                matching_tasks.append(task)
        return sorted(matching_tasks)


# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------

test_data = DataGenerator()


@pytest.fixture()
def cache_data_manager(mocker):
    mocker.patch.object(CacheDataManager, "read_data_cache", return_value=test_data.data)
    cache_data = CacheDataManager()
    return cache_data


class TestCacheDataManager:
    """Unit tests for the CacheDataManager class."""

    def test_CacheDataManager__init(self, mocker):
        mocker.patch.object(CacheDataManager, "read_data_cache", return_value=test_data.data)

        cache = CacheDataManager()

        assert os.path.basename(cache.cache_filename) == 'dbcollection.json'

    def test___get_cache_filename(self, cache_data_manager):
        filename = cache_data_manager._get_cache_filename()
        assert os.path.basename(filename) == 'dbcollection.json'

    def test_read_data_cache__file_exists(self, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = True
        mocker.patch.object(CacheDataManager, "read_data_cache_file", return_value=test_data.data)
        cache = CacheDataManager()

        assert cache.read_data_cache() == test_data.data

    def test_read_data_cache__file_missing(self, mocker):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = False
        mocker.patch.object(CacheDataManager, "_empty_data", return_value=test_data.data)
        mocker.patch.object(CacheDataManager, "write_data_cache")
        cache = CacheDataManager()

        assert cache.read_data_cache() == test_data.data

    def test_write_data_cache(self, mocker, cache_data_manager):
        new_data = {"some": "data"}
        mocker.patch("builtins.open")
        mocker.patch('json.dump')

        cache_data_manager.write_data_cache(new_data)

        assert cache_data_manager.data == new_data

    def test__set_cache_dir(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"

        cache_data_manager._set_cache_dir(new_path)

        assert cache_data_manager.cache_dir == new_path

    def test__get_cache_dir(self, mocker, cache_data_manager):
        assert cache_data_manager.cache_dir == test_data.data['info']['root_cache_dir']

    def test_reset_cache_dir(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"
        cache_data_manager._set_cache_dir(new_path)

        cache_data_manager.reset_cache_dir()

        assert cache_data_manager.cache_dir == cache_data_manager._get_default_cache_dir()
        assert cache_data_manager.cache_dir is not new_path

    def test__set_download_dir(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"

        cache_data_manager._set_download_dir(new_path)

        assert cache_data_manager.download_dir == new_path

    def test__get_download_dir(self, mocker, cache_data_manager):
        assert cache_data_manager.download_dir == test_data.data['info']['root_downloads_dir']

    def test_reset_download_dir(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"
        cache_data_manager._set_download_dir(new_path)

        cache_data_manager.reset_download_dir()

        assert cache_data_manager.download_dir == cache_data_manager._get_default_downloads_dir()
        assert cache_data_manager.download_dir is not new_path

    def test_reset_cache(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        cache_data_manager.reset_cache(True)

    def test_reset_cache__raise_warning(self, mocker, cache_data_manager):
        with pytest.warns(UserWarning):
            cache_data_manager.reset_cache()

    def test_delete_cache__raise_warning_cache_file(self, mocker, cache_data_manager):
        with pytest.warns(UserWarning):
            cache_data_manager.delete_cache()

    def test_delete_cache__delete_cache_file(self, mocker, cache_data_manager):
        mocker.patch('os.remove')

        cache_data_manager.delete_cache(force_delete_file=True)

        os.remove.assert_called_once_with(cache_data_manager.cache_filename)

    def test_delete_cache__raise_warning_cache_metadata(self, mocker, cache_data_manager):
        with pytest.warns(UserWarning):
            cache_data_manager.delete_cache(force_delete_metadata=True)

    def test_delete_cache__delete_cache_metadata(self, mocker, cache_data_manager):
        mock_shutil = mocker.patch('shutil.rmtree')

        cache_data_manager.delete_cache(force_delete_file=True, force_delete_metadata=True)

        assert mock_shutil.called

    def test_add_data_to_cache(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'new_dataset'
        cache_dir = '/some/path/to/cache/dir'
        data_dir = '/some/path/to/data'
        tasks = {
            "new_taskA": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name),
                "categories": ["new_categoryA"]
            },
            "new_taskB": {
                "filename": '/some/path/dbcollection/{}/new_taskB.h5'.format(name),
                "categories": ["new_categoryB", 'new_categoryC']
            },
        }

        cache_data_manager.add_data(name, cache_dir, data_dir, tasks)

        self._assert_add_data_to_cache(name, cache_dir, data_dir, tasks, cache_data_manager)
        assert "new_categoryA" in cache_data_manager.data["category"]

    def _assert_add_data_to_cache(self, name, cache_dir, data_dir, tasks, cache_data_m):
        assert name in cache_data_m.data["dataset"]
        assert cache_dir == cache_data_m.data["dataset"][name]["cache_dir"]
        assert data_dir == cache_data_m.data["dataset"][name]["data_dir"]
        assert tasks == cache_data_m.data["dataset"][name]["tasks"]
        assert any(cache_data_m.data["dataset"][name]["keywords"])

    def test_add_data_to_cache_twice(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name_dbA = 'new_datasetA'
        cache_dir_dbA = '/some/path/to/cache/dir'
        data_dir_dbA = '/some/path/to/data'
        tasks_dbA = {
            "new_taskA": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name_dbA),
                "categories": ["new_categoryA"]
            },
            "new_taskB": {
                "filename": '/some/path/dbcollection/{}/new_taskB.h5'.format(name_dbA),
                "categories": ["new_categoryB", 'new_categoryC']
            },
        }

        name_dbB = 'new_datasetB'
        cache_dir_dbB = '/some/path/to/cache/dir'
        data_dir_dbB = '/some/path/to/data'
        tasks_dbB = {
            "new_taskC": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name_dbB),
                "categories": ["new_categoryZ"]
            }
        }

        cache_data_manager.add_data(name_dbA, cache_dir_dbA, data_dir_dbA, tasks_dbA)
        category_after_dbA = cache_data_manager.data["category"].copy()
        cache_data_manager.add_data(name_dbB, cache_dir_dbB, data_dir_dbB, tasks_dbB)
        category_after_dbB = cache_data_manager.data["category"].copy()

        self._assert_add_data_to_cache(name_dbA, cache_dir_dbA, data_dir_dbA, tasks_dbA, cache_data_manager)
        self._assert_add_data_to_cache(name_dbB, cache_dir_dbB, data_dir_dbB, tasks_dbB, cache_data_manager)
        assert category_after_dbA != category_after_dbB

    def test_get_data(self, mocker, cache_data_manager):
        name = 'dataset0'

        data = cache_data_manager.get_data(name)

        assert data == cache_data_manager.data["dataset"][name]

    def test_get_data__raises_error_unknown_dataset_name(self, mocker, cache_data_manager):
        name = 'unknown_dataset_name'

        with pytest.raises(KeyError):
            cache_data_manager.get_data(name)

    def test_update_data_new_dirs(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'dataset0'
        cache_dir = '/new/some/path/to/cache/dir'
        data_dir = '/new/some/path/to/data'

        cache_data_manager.update_data(name, cache_dir=cache_dir, data_dir=data_dir)

        assert name in cache_data_manager.data["dataset"]
        assert cache_dir == cache_data_manager.data["dataset"][name]["cache_dir"]
        assert data_dir == cache_data_manager.data["dataset"][name]["data_dir"]

    def test_update_data_new_tasks(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'dataset0'
        tasks = {
            "new_taskA": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name),
                "categories": ["new_categoryA"]
            },
            "new_taskB": {
                "filename": '/some/path/dbcollection/{}/new_taskB.h5'.format(name),
                "categories": ["new_categoryB", 'new_categoryC']
            },
        }
        keywords = ("new_categoryA", "new_categoryB", "new_categoryC")
        categories = cache_data_manager.data["category"]

        cache_data_manager.update_data(name, tasks=tasks)

        assert name in cache_data_manager.data["dataset"]
        assert tasks == cache_data_manager.data["dataset"][name]["tasks"]
        assert keywords == cache_data_manager.data["dataset"][name]["keywords"]
        assert categories != cache_data_manager.data["category"]

    def test_update_data__raise_unknown_dataset_name(self, mocker, cache_data_manager):
        name = "some_unknown_dataset_name"

        with pytest.raises(AssertionError):
            cache_data_manager.update_data(name)

    def test_update_data_skip_writting_data_to_cache(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'dataset0'
        categories = cache_data_manager.data["category"]

        cache_data_manager.update_data(name)

        assert categories == cache_data_manager.data["category"]
        assert True  # check how to assert mocked function calls

    def test_delete_data(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'dataset5'
        categories = cache_data_manager.data["category"].copy()

        cache_data_manager.delete_data(name)

        assert name not in cache_data_manager.data["dataset"]
        assert categories != cache_data_manager.data["category"]

    def test_delete_data__raises_error_name_not_found(self, mocker, cache_data_manager):
        name = 'unknown_dataset_name'

        with pytest.raises(KeyError):
            cache_data_manager.delete_data(name)


@pytest.fixture()
def cache_manager(mocker):
    cache_info = CacheManagerInfo(cache_manager)
    return cache_info

class TestCacheManager:
    """Unit tests for the CacheManager class."""

    def test_CacheManager__init(self, cache_manager):
        pass


@pytest.fixture()
def cache_info_manager(mocker, cache_data_manager):
    cache_info = CacheManagerInfo(cache_data_manager)
    return cache_info


class TestCacheManagerInfo:
    """Unit tests for the CacheManagerInfo class."""

    def test_init_class(self, mocker):
        manager = mocker.Mock()
        cache_info = CacheManagerInfo(manager)

    def test_init_class__raises_error_missing_manager(self, mocker):
        with pytest.raises(TypeError):
            cache_info = CacheManagerInfo()

    def test__set_cache_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"

        cache_info_manager.manager.cache_dir = new_path

        assert cache_info_manager.cache_dir == new_path

    def test__get_cache_dir(self, mocker, cache_info_manager):
        assert cache_info_manager.cache_dir == test_data.data['info']['root_cache_dir']

    def test_reset_cache_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"
        cache_info_manager.cache_dir == new_path

        cache_info_manager.reset_cache_dir()

        assert cache_info_manager.cache_dir == cache_info_manager.manager.cache_dir
        assert cache_info_manager.cache_dir is not new_path

    def test__set_download_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"

        cache_info_manager.download_dir = new_path

        assert cache_info_manager.manager.download_dir == new_path

    def test__get_download_dir(self, mocker, cache_info_manager):
        assert cache_info_manager.download_dir == test_data.data['info']['root_downloads_dir']

    def test_reset_download_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"
        cache_info_manager.download_dir = new_path

        cache_info_manager.reset_download_dir()

        assert cache_info_manager.download_dir == cache_info_manager.manager.download_dir
        assert cache_info_manager.download_dir is not new_path

    def test_reset(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        cache_info_manager.cache_dir = "/new/cache/path"
        cache_info_manager.download_dir = "/new/cache/downloads/path"

        cache_info_manager.reset()

        assert cache_info_manager.cache_dir == cache_info_manager.manager._get_default_cache_dir()
        assert cache_info_manager.download_dir == cache_info_manager.manager._get_default_downloads_dir()

    def test_info(self, mocker, cache_info_manager):
        cache_info_manager.info()


@pytest.fixture()
def cache_dataset_manager(mocker, cache_data_manager):
    mocker.patch.object(CacheDataManager, "write_data_cache")
    cache_info = CacheManagerDataset(cache_data_manager)
    return cache_info


class TestCacheManagerDataset:
    """Unit tests for the CacheManagerDataset class."""

    def test_init_class(self, mocker):
        manager = mocker.Mock()
        cache_info = CacheManagerDataset(manager)

    def test_init_class__raises_error_missing_manager(self, mocker):
        with pytest.raises(TypeError):
            cache_info = CacheManagerDataset()

    def test_add_dataset(self, mocker, cache_dataset_manager):
        name = 'new_dataset_name'
        cache_dir = '/some/path/to/cache/dir'
        data_dir = '/some/path/to/data'
        tasks = {
            "new_task": {
                "filename": '/some/path/dbcollection/{}/new_task.h5'.format(name),
                "categories": ["new_category_A", "new_category_B", "new_category_C"]
            },
        }

        cache_dataset_manager.add(name, cache_dir, data_dir, tasks)

        assert name in cache_dataset_manager.manager.data["dataset"]
        assert cache_dir == cache_dataset_manager.manager.data["dataset"][name]["cache_dir"]
        assert data_dir == cache_dataset_manager.manager.data["dataset"][name]["data_dir"]
        assert tasks == cache_dataset_manager.manager.data["dataset"][name]["tasks"]
        assert any(cache_dataset_manager.manager.data["dataset"][name]["keywords"])
        assert "new_category_A" in cache_dataset_manager.manager.data["category"]

    def test_add_dataset__raises_error_missing_inputs(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.add()

    def test_get_dataset(self, mocker, cache_dataset_manager):
        name = 'dataset0'

        dataset = cache_dataset_manager.get(name)

        assert dataset == cache_dataset_manager.manager.data['dataset'][name]

    def test_get_dataset__raises_error_missing_input(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.get()

    def test_get_dataset__raises_error_unknown_dataset(self, mocker, cache_dataset_manager):
        name = "unknown_dataset"

        with pytest.raises(KeyError):
            cache_dataset_manager.get(name)

    def test_update_dataset(self, mocker, cache_dataset_manager):
        name = 'dataset0'
        tasks = {
            "new_taskA": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name),
                "categories": ["new_categoryA"]
            },
            "new_taskB": {
                "filename": '/some/path/dbcollection/{}/new_taskB.h5'.format(name),
                "categories": ["new_categoryB", 'new_categoryXYZ']
            },
        }
        keywords = ("new_categoryA", "new_categoryB", "new_categoryXYZ")
        categories = cache_dataset_manager.manager.data["category"]

        cache_dataset_manager.update(name, tasks=tasks)

        assert name in cache_dataset_manager.manager.data["dataset"]
        assert tasks == cache_dataset_manager.manager.data["dataset"][name]["tasks"]
        assert keywords == cache_dataset_manager.manager.data["dataset"][name]["keywords"]
        assert categories != cache_dataset_manager.manager.data["category"]

    def test_update_dataset__raises_error_missing_input(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.update()

    def test_update_dataset__raises_error_unknown_dataset(self, mocker, cache_dataset_manager):
        name = "another_unknown_dataset"

        with pytest.raises(AssertionError):
            cache_dataset_manager.update(name)

    def test_delete_dataset(self, mocker, cache_dataset_manager):
        name = 'dataset6'
        categories = cache_dataset_manager.manager.data["category"].copy()

        cache_dataset_manager.delete(name)

        assert name not in cache_dataset_manager.manager.data["dataset"]
        assert categories != cache_dataset_manager.manager.data["category"]

    def test_delete_dataset__raises_error_missing_input(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.delete()

    def test_delete_dataset__raises_error_unknown_dataset(self, mocker, cache_dataset_manager):
        name = "yet_another_unknown_dataset"

        with pytest.raises(KeyError):
            cache_dataset_manager.delete(name)

    def test_info(self, mocker, cache_dataset_manager):
        cache_dataset_manager.info()

    def test_exists_dataset__valid_dataset(self, mocker, cache_dataset_manager):
        name = 'dataset0'

        assert cache_dataset_manager.exists(name)

    def test_exists_dataset__invalid_dataset(self, mocker, cache_dataset_manager):
        name = 'dataset0__invalid'

        assert not cache_dataset_manager.exists(name)

    def test_exists_dataset__raises_error_missing_input(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.exists()

    def test_list_dataset_names(self, mocker, cache_dataset_manager):
        datasets = list(sorted(cache_dataset_manager.manager.data["dataset"].keys()))

        assert datasets == cache_dataset_manager.list()


@pytest.fixture()
def cache_category_manager(mocker, cache_data_manager):
    cache_info = CacheManagerCategory(cache_data_manager)
    return cache_info


class TestCacheManagerCategory:
    """Unit tests for the CacheManagerCategory class."""

    def test_init_class(self, mocker):
        manager = mocker.Mock()
        cache_info = CacheManagerCategory(manager)

    def test_init_class__raises_error_missing_manager(self, mocker):
        with pytest.raises(TypeError):
            cache_info = CacheManagerCategory()

    def test_get_category(self, mocker, cache_category_manager):
        category = 'category0'

        result = cache_category_manager.get(category)

        assert result == cache_category_manager.manager.data["category"][category]

    def test_get_categoryt__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.get()

    def test_get_category__raises_error_invalid_category(self, mocker, cache_category_manager):
        category = 'categoryZ'

        with pytest.raises(KeyError):
            cache_category_manager.get(category)

    def test_get_by_dataset(self, mocker, cache_category_manager):
        dataset = 'dataset0'

        result = cache_category_manager.get_by_dataset(dataset)

        assert any(result)

    def test_get_by_dataset__invalid_dataset(self, mocker, cache_category_manager):
        dataset = 'datasetZ'

        result = cache_category_manager.get_by_dataset(dataset)

        assert not any(result)

    def test_get_by_dataset__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.get_by_dataset()

    def test_get_by_task(self, mocker, cache_category_manager):
        task = 'task0'

        result = cache_category_manager.get_by_task(task)

        assert any(result)

    def test_get_by_task__invalid_task(self, mocker, cache_category_manager):
        task = 'taskXYZ'

        result = cache_category_manager.get_by_task(task)

        assert not any(result)

    def test_get_by_task__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.get_by_task()
