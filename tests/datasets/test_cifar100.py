"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np

from dbcollection.datasets.cifar.cifar100 import Classification


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


class TestClassificationTask:
    """Unit tests for the cifar100 Classification task."""

    def test_task_attributes(self, mocker, mock_classification_class):
        assert mock_classification_class.filename_h5 == 'classification'
        assert mock_classification_class.data_files == ["meta", "train", "test"]
        assert mock_classification_class.coarse_classes == [
            'aquatic mammals',
            'fish',
            'flowers',
            'food containers',
            'fruit and vegetables',
            'household electrical devices',
            'household furniture',
            'insects',
            'large carnivores',
            'large man-made outdoor things',
            'large natural outdoor scenes',
            'large omnivores and herbivores',
            'medium-sized mammals',
            'non-insect invertebrates',
            'people',
            'reptiles',
            'small mammals',
            'trees',
            'vehicles 1',
            'vehicles 2',
        ]
        assert mock_classification_class.finer_classes == [
            'beaver', 'dolphin', 'otter', 'seal', 'whale',
            'aquarium fish', 'flatfish', 'ray', 'shark', 'trout',
            'orchids', 'poppies', 'roses', 'sunflowers', 'tulips',
            'bottles', 'bowls', 'cans', 'cups', 'plates',
            'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers',
            'clock', 'computer keyboard', 'lamp', 'telephone', 'television',
            'bed', 'chair', 'couch', 'table', 'wardrobe',
            'bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach',
            'bear', 'leopard', 'lion', 'tiger', 'wolf',
            'bridge', 'castle', 'house', 'road', 'skyscraper',
            'cloud', 'forest', 'mountain', 'plain', 'sea',
            'camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo',
            'fox', 'porcupine', 'possum', 'raccoon', 'skunk',
            'crab', 'lobster', 'snail', 'spider', 'worm',
            'baby', 'boy', 'girl', 'man', 'woman',
            'crocodile', 'dinosaur', 'lizard', 'snake', 'turtle',
            'hamster', 'mouse', 'rabbit', 'shrew', 'squirrel',
            'maple', 'oak', 'palm', 'pine', 'willow',
            'bicycle', 'bus', 'motorcycle', 'pickup truck', 'train',
            'lawn-mower', 'rocket', 'streetcar', 'tank', 'tractor'
        ]

    def test_load_data(self, mocker, mock_classification_class):
        mock_load_data = mocker.patch.object(Classification, "load_data_set", return_value=['some_data'])

        load_data_generator = mock_classification_class.load_data()
        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        assert mock_load_data.called
        assert train_data == {"train": ['some_data']}
        assert test_data == {"test": ['some_data']}
