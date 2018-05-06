"""
Test dbcollection/utils/cache.py.
"""


import os
import sys
import random
import pytest

from dbcollection.core.manager import (
    CacheManager,
    CacheDataManager,
    CacheManagerInfo,
    CacheManagerDataset,
    CacheManagerTask,
    CacheManagerCategory
)


# -----------------------------------------------------------
# Test Data
# -----------------------------------------------------------

class DataGenerator:
    """Generates sample data for testing the CacheManager class.

    This class generates a sample data structure thet a cache file will
    contain wityh information about paths, datasets and categories of
    datasets.

    Example
    =======
    The generated data should resemble something like the following:

    data = {
        "info": {
            "root_cache_dir": '/some/path/dbcollection',
            "root_downloads_dir": '/some/path/dbcollection/downloads',
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
            "root_downloads_dir": os.path.join(self.base_path, "dbcollection", "downloads"),
        }

    def get_datasets_data(self):
        """Returns the dataset's data for the dataset cache field."""
        return self.generate_random_datasets()

    def generate_random_datasets(self):
        """Generates random datasets."""
        datasets = {}
        for dataset in self.list_datasets:
            data = {}
            data["data_dir"] = os.path.join(self.info["root_downloads_dir"], dataset)
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

@pytest.fixture()
def test_data():
    return DataGenerator()

@pytest.fixture()
def cache_data_manager(mocker, test_data):
    mocker.patch.object(CacheDataManager, "read_data_cache", return_value=test_data.data)
    cache_data = CacheDataManager()
    return cache_data


class TestCacheDataManager:
    """Unit tests for the CacheDataManager class."""

    def test_CacheDataManager__init(self, mocker, test_data):
        mocker.patch.object(CacheDataManager, "read_data_cache", return_value=test_data.data)

        cache = CacheDataManager()

        assert os.path.basename(cache.cache_filename) == 'dbcollection.json'

    def test___get_cache_filename(self, cache_data_manager):
        filename = cache_data_manager._get_cache_filename()
        assert os.path.basename(filename) == 'dbcollection.json'

    def test_read_data_cache__file_exists(self, mocker, test_data):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = True
        mocker.patch.object(CacheDataManager, "read_data_cache_file", return_value=test_data.data)
        cache = CacheDataManager()

        assert cache.read_data_cache() == test_data.data

    def test_read_data_cache__file_missing(self, mocker, test_data):
        mocked_exists = mocker.patch("os.path.exists")
        mocked_exists.return_value = False
        mocker.patch.object(CacheDataManager, "_empty_data", return_value=test_data.data)
        mocker.patch.object(CacheDataManager, "write_data_cache")
        cache = CacheDataManager()

        assert cache.read_data_cache() == test_data.data

    def test_write_data_cache(self, mocker, cache_data_manager):
        new_data = {"some": "data"}
        if sys.version_info[0] == 3:
            mocker.patch("builtins.open")
        else:
            mocker.patch("__builtin__.open")
        mocker.patch('json.dump')

        cache_data_manager.write_data_cache(new_data)

        assert cache_data_manager.data == new_data

    def test__set_cache_dir(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"

        cache_data_manager._set_cache_dir(new_path)

        assert cache_data_manager.cache_dir == new_path

    def test__get_cache_dir(self, mocker, cache_data_manager, test_data):
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

    def test__get_download_dir(self, mocker, cache_data_manager, test_data):
        download_dir = cache_data_manager.download_dir
        assert download_dir == test_data.data['info']['root_downloads_dir']

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
        mock_glob = mocker.patch("glob.glob", return_value=["some", "dirs", "paths"])

        cache_data_manager.delete_cache(force_delete_file=True, force_delete_metadata=True)

        assert not mock_shutil.called  # workaround: cannot get to mock "glob"

    def test_add_data_to_cache(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name = 'new_dataset'
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

        cache_data_manager.add_data(name, data_dir, tasks)

        self._assert_add_data_to_cache(name, data_dir, tasks, cache_data_manager)
        assert "new_categoryA" in cache_data_manager.data["category"]

    def _assert_add_data_to_cache(self, name, data_dir, tasks, cache_data_m):
        assert name in cache_data_m.data["dataset"]
        assert data_dir == cache_data_m.data["dataset"][name]["data_dir"]
        assert tasks == cache_data_m.data["dataset"][name]["tasks"]
        assert any(cache_data_m.data["dataset"][name]["keywords"])

    def test_add_data_to_cache_twice(self, mocker, cache_data_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        name_dbA = 'new_datasetA'
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
        data_dir_dbB = '/some/path/to/data'
        tasks_dbB = {
            "new_taskC": {
                "filename": '/some/path/dbcollection/{}/new_taskA.h5'.format(name_dbB),
                "categories": ["new_categoryZ"]
            }
        }

        cache_data_manager.add_data(name_dbA, data_dir_dbA, tasks_dbA)
        category_after_dbA = cache_data_manager.data["category"].copy()
        cache_data_manager.add_data(name_dbB, data_dir_dbB, tasks_dbB)
        category_after_dbB = cache_data_manager.data["category"].copy()

        self._assert_add_data_to_cache(name_dbA, data_dir_dbA, tasks_dbA, cache_data_manager)
        self._assert_add_data_to_cache(name_dbB, data_dir_dbB, tasks_dbB, cache_data_manager)
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

    def test_reload_cache(self, mocker, cache_data_manager, test_data):
        cache_data_manager.data = None

        cache_data_manager.reload_cache()

        assert cache_data_manager.data is not None
        assert cache_data_manager.data == test_data.data


@pytest.fixture()
def cache_manager(mocker, test_data):
    mocker.patch.object(CacheDataManager, "read_data_cache", return_value=test_data.data)
    cache = CacheManager()
    return cache

class TestCacheManager:
    """Unit tests for the CacheManager class."""

    def test_CacheManager__init(self, cache_manager, test_data):
        assert isinstance(cache_manager.manager, CacheDataManager)
        assert isinstance(cache_manager.info, CacheManagerInfo)
        assert isinstance(cache_manager.dataset, CacheManagerDataset)
        assert isinstance(cache_manager.task, CacheManagerTask)
        assert isinstance(cache_manager.category, CacheManagerCategory)

    def test_info(self, cache_manager):
        cache_manager.info_cache()


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

    def test__get_cache_dir(self, mocker, cache_info_manager, test_data):
        assert cache_info_manager.cache_dir == test_data.data['info']['root_cache_dir']

    def test_reset_cache_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/path"
        cache_info_manager.cache_dir == new_path

        cache_info_manager.reset_cache_dir()

        assert cache_info_manager.cache_dir == cache_info_manager.manager.cache_dir
        assert cache_info_manager.cache_dir is not new_path

    @pytest.mark.skipif(sys.version_info[0] == 2, reason="weird behaviour for python2")
    def test__set_download_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"

        cache_info_manager.download_dir = new_path

        assert cache_info_manager.manager.download_dir == new_path

    def test__get_download_dir(self, mocker, cache_info_manager, test_data):
        assert cache_info_manager.download_dir == test_data.data['info']['root_downloads_dir']

    @pytest.mark.skipif(sys.version_info[0] == 2, reason="weird behaviour for python2")
    def test_reset_download_dir(self, mocker, cache_info_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        new_path = "/new/cache/downloads/path"
        cache_info_manager.download_dir = new_path

        cache_info_manager.reset_download_dir()

        assert cache_info_manager.download_dir == cache_info_manager.manager.download_dir
        assert cache_info_manager.download_dir is not new_path

    def test_reset(self, mocker, cache_info_manager):
        mock_reset_cache = mocker.patch.object(CacheManagerInfo, 'reset_cache_dir')
        mock_reset_download = mocker.patch.object(CacheManagerInfo, 'reset_download_dir')

        cache_info_manager.reset()

        assert mock_reset_cache.called
        assert mock_reset_download.called

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
        data_dir = '/some/path/to/data'
        tasks = {
            "new_task": {
                "filename": '/some/path/dbcollection/{}/new_task.h5'.format(name),
                "categories": ["new_category_A", "new_category_B", "new_category_C"]
            },
        }

        cache_dataset_manager.add(name, data_dir, tasks)

        assert name in cache_dataset_manager.manager.data["dataset"]
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
        mock_select_data = mocker.patch.object(CacheManagerDataset, '_get_select_tasks_and_datasets_data', return_value={})
        mock_data = mocker.patch.object(CacheManagerDataset, '_get_dataset_data', return_value={})

        cache_dataset_manager.info()

        assert not mock_select_data.called
        assert mock_data.called

    def test_info_empty_inputs(self, mocker, cache_dataset_manager):
        mock_select_data = mocker.patch.object(CacheManagerDataset, '_get_select_tasks_and_datasets_data', return_value={})
        mock_data = mocker.patch.object(CacheManagerDataset, '_get_dataset_data', return_value={})

        cache_dataset_manager.info('', '')

        assert not mock_select_data.called
        assert mock_data.called

    @pytest.mark.parametrize('datasets, tasks', [
        (['datasetA', 'datasetB'], None),
        (['taskA', 'TaskC'], None),
        (['datasetA', 'datasetB'], 'taskB'),
    ])
    def test_info_with_datasets_and_tasks(self, mocker, cache_dataset_manager, datasets, tasks):
        mock_select_data = mocker.patch.object(CacheManagerDataset, '_get_select_tasks_and_datasets_data', return_value={})
        mock_data = mocker.patch.object(CacheManagerDataset, '_get_dataset_data', return_value={})

        cache_dataset_manager.info(datasets, tasks)

        assert mock_select_data.called
        assert not mock_data.called

    def test_info__raises_error_too_many_inputs(self, mocker, cache_dataset_manager):
        with pytest.raises(TypeError):
            cache_dataset_manager.info('', '', '')

    def test_get_select_tasks_and_datasets_data_with_datasets_only(self, mocker, cache_dataset_manager):
        mock_filter_datasets = mocker.patch.object(CacheManagerDataset, '_get_data_selected_datasets', return_value={'some': 'data'})
        mock_filter_tasks = mocker.patch.object(CacheManagerDataset, '_get_data_selected_tasks', return_value={})
        datasets = ('datasetA', 'datasetB')
        tasks = ()

        result = cache_dataset_manager._get_select_tasks_and_datasets_data(datasets, tasks)

        assert mock_filter_datasets.called
        assert not mock_filter_tasks.called
        assert result == {'some': 'data'}

    def test_get_select_tasks_and_datasets_data_with_tasks_only(self, mocker, cache_dataset_manager):
        mock_filter_datasets = mocker.patch.object(CacheManagerDataset, '_get_data_selected_datasets', return_value={})
        mock_filter_tasks = mocker.patch.object(CacheManagerDataset, '_get_data_selected_tasks', return_value={'some': 'tasks'})
        tasks = 'taskA'

        result = cache_dataset_manager._get_select_tasks_and_datasets_data(tasks=tasks)

        assert not mock_filter_datasets.called
        assert mock_filter_tasks.called
        assert result == {'some': 'tasks'}

    def test_get_select_tasks_and_datasets_data_with_both(self, mocker, cache_dataset_manager):
        mock_filter_datasets = mocker.patch.object(CacheManagerDataset, '_get_data_selected_datasets', return_value={'some': {'data': [1, 2, 3]}})
        mock_filter_tasks = mocker.patch.object(CacheManagerDataset, '_get_data_selected_tasks', return_value={'some': {'tasks': 'taskA'}})
        datasets = 'some_dataset'
        tasks = 'some_task'

        result = cache_dataset_manager._get_select_tasks_and_datasets_data(datasets, tasks)

        assert mock_filter_datasets.called
        assert mock_filter_tasks.called
        assert result == {'some': {'data': [1, 2, 3], 'tasks': 'taskA'}}

    def test_get_data_selected_datasets(self, mocker, cache_dataset_manager):
        data = {'datasetA': ['some', 'data'], 'datasetB': {'data': 1}, 'datasetC': [1, 2, 3]}
        datasets = ['datasetA', 'datasetb']
        mock_get_data = mocker.patch.object(CacheManagerDataset, '_get_dataset_data', return_value=data)

        result = cache_dataset_manager._get_data_selected_datasets(datasets)

        assert mock_get_data.called
        assert result == {'datasetA': ['some', 'data'], 'datasetB': {'data': 1}}

    def test_get_data_selected_tasks(self, mocker, cache_dataset_manager):
        data = {'datasetA': {"stuff": 'some_stuffA', "tasks": {"taskA": 'itemA'}}, 'datasetB': {"stuff": 'some_stuffB', "tasks": {"taskb": 'itemb'}}}
        tasks = ('taskB',)
        mock_get_data = mocker.patch.object(CacheManagerDataset, '_get_dataset_data', return_value=data)

        result = cache_dataset_manager._get_data_selected_tasks(tasks)

        assert mock_get_data.called
        assert result == {'datasetB': {"tasks": {"taskb": 'itemb'}}}

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
def cache_task_manager(mocker, cache_data_manager):
    cache_task = CacheManagerTask(cache_data_manager)
    return cache_task


class TestCacheManagerTask:
    """Unit tests for the CacheManagerTask class."""

    def test_init_class(self, mocker):
        manager = mocker.Mock()
        cache_task = CacheManagerTask(manager)

    def test_init_class__raises_error_missing_manager(self, mocker):
        with pytest.raises(TypeError):
            cache_info = CacheManagerTask()

    def test_add_task(self, mocker, cache_task_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        dataset = 'dataset2'
        task = "new_task"
        filename = "/path/to/new/task.h5"
        categories = ["brand", "new", "categories"]

        cache_task_manager.add(dataset, task, filename, categories)

        cache_db = cache_task_manager.manager.data["dataset"][dataset]
        assert task in cache_db["tasks"]
        assert filename == cache_db["tasks"][task]["filename"]
        assert sorted(categories) == cache_db["tasks"][task]["categories"]

    def test_add_task_empty_categories(self, mocker, cache_task_manager):
        mocker.patch.object(CacheDataManager, "write_data_cache")
        dataset = 'dataset3'
        task = "new_task"
        filename = "/path/to/new/task_2.h5"
        categories = []

        cache_task_manager.add(dataset, task, filename, categories)

        cache_db = cache_task_manager.manager.data["dataset"][dataset]
        assert task in cache_db["tasks"]
        assert filename == cache_db["tasks"][task]["filename"]
        assert sorted(categories) == cache_db["tasks"][task]["categories"]

    def test_add_task__raises_error_missing_inputs(self, mocker, cache_task_manager):
        with pytest.raises(TypeError):
            cache_task_manager.add()

    def test_add_task__raises_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = 'datasetQWERTY'
        task = "some_task"
        filename = "/path/to/new/some_task.h5"
        categories = ["brand", "new", "categories"]

        with pytest.raises(KeyError):
            cache_task_manager.add(dataset, task, filename, categories)

    def test_add_task__raises_error_task_already_exists(self, mocker, cache_task_manager):
        dataset = 'dataset0'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        filename = "/path/to/new/some_task.h5"
        categories = ["brand", "new", "categories"]

        with pytest.raises(AssertionError):
            cache_task_manager.add(dataset, task, filename, categories)

    def test_get_task(self, mocker, cache_task_manager):
        dataset = 'dataset0'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        metadata = cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]

        result = cache_task_manager.get(dataset, task)

        assert metadata == result

    def test_get_task__raises_error_missing_inputs(self, mocker, cache_task_manager):
        with pytest.raises(TypeError):
            cache_task_manager.get()

    def test_get_task__raises_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = 'unknown_dataset'
        task = 'some_task'

        with pytest.raises(KeyError):
            cache_task_manager.get(dataset, task)

    def test_get_task__raises_error_invalid_task(self, mocker, cache_task_manager):
        dataset = 'dataset1'
        task = 'invalid_task'

        with pytest.raises(KeyError):
            cache_task_manager.get(dataset, task)

    def test_update_task__do_nothing(self, mocker, cache_task_manager):
        dataset = 'dataset4'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        filename = cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["filename"]
        categories = cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["categories"]

        cache_task_manager.update(dataset, task)

        assert dataset in cache_task_manager.manager.data["dataset"]
        assert task in cache_task_manager.manager.data["dataset"][dataset]["tasks"]
        assert filename == cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["filename"]
        assert categories == cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["categories"]

    def test_update_task_filename(self, mocker, cache_task_manager):
        dataset = 'dataset4'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        filename = "/new/file/name.h5"

        cache_task_manager.update(dataset, task, filename)

        assert dataset in cache_task_manager.manager.data["dataset"]
        assert task in cache_task_manager.manager.data["dataset"][dataset]["tasks"]
        assert filename == cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["filename"]

    def test_update_task_add_categories(self, mocker, cache_task_manager):
        dataset = 'dataset4'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        new_categories = ["add", "more", "categories"]
        update_categories = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["categories"]) + new_categories

        cache_task_manager.update(dataset, task, None, update_categories)

        assert dataset in cache_task_manager.manager.data["dataset"]
        assert task in cache_task_manager.manager.data["dataset"][dataset]["tasks"]
        assert sorted(update_categories) == cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["categories"]

    def test_update_task_filename_categories(self, mocker, cache_task_manager):
        dataset = 'dataset4'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]
        filename = "/new/file/name.h5"
        categories = []

        cache_task_manager.update(dataset, task, filename, categories)

        assert dataset in cache_task_manager.manager.data["dataset"]
        assert task in cache_task_manager.manager.data["dataset"][dataset]["tasks"]
        assert filename == cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["filename"]
        assert not any(cache_task_manager.manager.data["dataset"][dataset]["tasks"][task]["categories"])

    def test_update_task__raises_error_missing_inputs(self, mocker, cache_task_manager):
        with pytest.raises(TypeError):
            cache_task_manager.update()

    def test_update_task__raises_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = 'unknown_dataset'
        task = 'some_task'
        filename = "/new/file/name.h5"

        with pytest.raises(KeyError):
            cache_task_manager.update(dataset, task, filename)

    def test_delete_task(self, mocker, cache_task_manager):
        dataset = "dataset7"
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]

        cache_task_manager.delete(dataset, task)

        assert task not in cache_task_manager.manager.data["dataset"][dataset]["tasks"]

    def test_delete_task__raises_error_missing_inputs(self, mocker, cache_task_manager):
        with pytest.raises(TypeError):
            cache_task_manager.delete()

    def test_delete_task__raises_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = "invalid_dataset"
        task = "some_task"

        with pytest.raises(KeyError):
            cache_task_manager.delete(dataset, task)

    def test_delete_task__raises_error_invalid_task(self, mocker, cache_task_manager):
        dataset = "dataset0"
        task = "invalid_task"

        with pytest.raises(KeyError):
            cache_task_manager.delete(dataset, task)

    def test_list_all_tasks(self, mocker, cache_task_manager):
        datasets = cache_task_manager.manager.data["dataset"]
        list_tasks = [task for dataset in datasets for task in datasets[dataset]["tasks"]]
        list_tasks = sorted(list(set(list_tasks)))

        result = cache_task_manager.list()

        assert list_tasks == result

    def test_list_tasks_given_dataset(self, mocker, cache_task_manager):
        dataset = "dataset0"
        tasks = sorted(list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys()))

        result = cache_task_manager.list(dataset)

        assert tasks == result

    def test_list_tasks__raise_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = "invalid_dataset"

        with pytest.raises(KeyError):
            cache_task_manager.list(dataset)

    def test_exists_task_in_cache(self, mocker, cache_task_manager):
        task = 'task0'

        assert cache_task_manager.exists(task)

    def test_exists_task_in_cache_invalid_task(self, mocker, cache_task_manager):
        task = 'taskXYZ'

        assert not cache_task_manager.exists(task)

    def test_exists_task_in_dataset(self, mocker, cache_task_manager):
        dataset = 'dataset0'
        existing_tasks = list(cache_task_manager.manager.data["dataset"][dataset]["tasks"].keys())
        task = existing_tasks[0]

        assert cache_task_manager.exists(task, dataset)

    def test_exists_task_in_dataset_invalid_task(self, mocker, cache_task_manager):
        dataset = 'dataset1'
        task = "invalid_task"

        assert not cache_task_manager.exists(task, dataset)

    def test_exists_task__raises_error_missing_inputs(self, mocker, cache_task_manager):
        with pytest.raises(TypeError):
            cache_task_manager.exists()

    def test_exists_task_in_dataset__raise_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = 'datasetIOU'
        task = "task0"

        with pytest.raises(KeyError):
            cache_task_manager.exists(task, dataset)

    def test_info(self, mocker, cache_task_manager):
        dataset = 'dataset0'

        cache_task_manager.info(dataset)

    def test_info_dataset(self, mocker, cache_task_manager):
        cache_task_manager.info()

    def test_info_dataset__raises_error_invalid_dataset(self, mocker, cache_task_manager):
        dataset = 'non_existing_dataset'

        with pytest.raises(KeyError):
            cache_task_manager.info(dataset)

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

    def test_exists_category(self, mocker, cache_category_manager):
        category = "category0"

        assert cache_category_manager.exists(category)

    def test_exists_category__invalid_category(self, mocker, cache_category_manager):
        category = "categoryXYZ"

        assert not cache_category_manager.exists(category)

    def test_exists__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.exists()

    def test_exists_task(self, mocker, cache_category_manager):
        task = "task0"

        assert cache_category_manager.exists_task(task)

    def test_exists_task__invalid_task(self, mocker, cache_category_manager):
        task = "taskXYZ"

        assert not cache_category_manager.exists_task(task)

    def test_exists_task__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.exists_task()

    def test_exists_dataset(self, mocker, cache_category_manager):
        dataset = "dataset1"

        assert cache_category_manager.exists_dataset(dataset)

    def test_exists_dataset__invalid_dataset(self, mocker, cache_category_manager):
        dataset = "datasetIOU"

        assert not cache_category_manager.exists_dataset(dataset)

    def test_exists_dataset__raises_error_missing_input(self, mocker, cache_category_manager):
        with pytest.raises(TypeError):
            cache_category_manager.exists_dataset()

    def test_list_dataset_names(self, mocker, cache_category_manager):
        datasets = list(sorted(cache_category_manager.manager.data["category"].keys()))

        assert datasets == cache_category_manager.list()

    def test_info(self, mocker, cache_category_manager):
        cache_category_manager.info()

    def test_info_with_categories(self, mocker, cache_category_manager):
        mock_filter = mocker.patch.object(CacheManagerCategory, '_get_filtered_category_data', return_value={})

        cache_category_manager.info(categories='categoryA')

        assert mock_filter.called

    def test__get_filtered_category_data_single_category(self, mocker, cache_category_manager):
        data = {'categoryA': ['some_data'], 'categoryb': ['more', 'data'], 'categoryC': True}
        categories = ['categoryB']

        result = cache_category_manager._get_filtered_category_data(data, categories)

        assert result == {'categoryb': ['more', 'data']}

    def test__get_filtered_category_data_multiple_categories(self, mocker, cache_category_manager):
        data = {'categoryA': ['some_data'], 'categoryb': ['more', 'data'], 'categoryC': True}
        categories = ['categoryA', 'categoryB']

        result = cache_category_manager._get_filtered_category_data(data, categories)

        assert result == {'categoryA': ['some_data'], 'categoryb': ['more', 'data']}
