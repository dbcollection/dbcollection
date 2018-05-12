"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.datasets.cifar.cifar100 import Classification
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


@pytest.fixture()
def classification_coarse_classes():
    return [
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


@pytest.fixture()
def classification_classes():
    return [
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


class TestClassificationTask:
    """Unit tests for the cifar100 Classification task."""

    def test_task_attributes(self, mocker, mock_classification_class,
                             classification_classes, classification_coarse_classes):
        assert mock_classification_class.filename_h5 == 'classification'
        assert mock_classification_class.data_files == ["meta", "train", "test"]
        assert mock_classification_class.coarse_classes == classification_coarse_classes
        assert mock_classification_class.finer_classes == classification_classes

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

    def test_load_data_set(self, mocker, mock_classification_class, classification_classes, classification_coarse_classes):
        mock_load_annotations = mocker.patch.object(Classification, "load_data_annotations", return_value=('images', 'labels', 'coarse_labels'))
        mock_get_object_list = mocker.patch.object(Classification, "get_object_list", return_value=list(range(10)))
        mock_get_list = mocker.patch.object(Classification, "get_images_per_class", return_value=list(range(5)))

        set_data = mock_classification_class.load_data_set(False)

        mock_load_annotations.assert_called_once_with(False)
        mock_get_object_list.assert_called_once_with('images', 'labels', 'coarse_labels')
        mock_get_list.assert_called()
        assert_array_equal(set_data['classes'], str2ascii(classification_classes))
        assert_array_equal(set_data['coarse_classes'], str2ascii(classification_coarse_classes))
        assert set_data['images'] == 'images'
        assert set_data['labels'] == 'labels'
        assert_array_equal(set_data['object_fields'], str2ascii(['images', 'classes', 'superclasses']))
        assert set_data['object_ids'] == list(range(10))
        assert set_data['list_images_per_class'] == list(range(5))
        assert set_data['list_images_per_superclass'] == list(range(5))

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations(self, mocker, mock_classification_class, is_test):
        mock_get_data_test = mocker.patch.object(Classification, "get_data_test", return_value='test')
        mock_get_data_train = mocker.patch.object(Classification, "get_data_train", return_value='train')

        annotations = mock_classification_class.load_data_annotations(is_test=is_test)

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        if is_test:
            mock_get_data_test.assert_called_once_with(data_path)
            mock_get_data_train.assert_not_called()
            assert annotations == 'test'
        else:
            mock_get_data_test.assert_not_called()
            mock_get_data_train.assert_called_once_with(data_path)
            assert annotations == 'train'
