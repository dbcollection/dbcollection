"""
Test data for testing the cache api.

The data generator contained in this file produces
a mock of a potential cache file structure.

Note: The names used are not designed to be real names,
just examples of possible strings.
"""


import os
import random


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
