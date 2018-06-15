"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.datasets.cifar.cifar100.classification import (
    Classification,
    DatasetAnnotationLoader,
    ClassLabelField,
    CoarseClassLabelField
)


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
        assert mock_get_list.called
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

    def test_get_data_test(self, mocker, mock_classification_class):
        mock_load_file = mocker.patch.object(Classification, "load_annotation_file", return_value='annotations')
        mock_parse_data = mocker.patch.object(Classification, "parse_data_annotations", return_value='dummy_data')

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        data = mock_classification_class.get_data_test(data_path)

        mock_load_file.assert_called_once_with(os.path.join(data_path, 'test'))
        mock_parse_data.assert_called_once_with('annotations', 10000)
        assert data == 'dummy_data'

    def test_parse_data_annotations(self, mocker, mock_classification_class):
        images = np.random.random((10, 3072))
        annotations = {
            "data": images,
            "fine_labels": range(10),
            "coarse_labels": range(5)
        }

        data, labels, coarse_labels = mock_classification_class.parse_data_annotations(annotations, 10)

        expected_images = np.transpose(images.reshape(10, 3, 32, 32), (0, 2, 3, 1))
        assert_array_equal(data, expected_images)
        assert_array_equal(labels, np.array(range(10), dtype=np.uint8))
        assert_array_equal(coarse_labels, np.array(range(5), dtype=np.uint8))

    def test_get_data_train(self, mocker, mock_classification_class):
        mock_load_file = mocker.patch.object(Classification, "load_annotation_file", return_value='annotations')
        mock_parse_data = mocker.patch.object(Classification, "parse_data_annotations", return_value='dummy_data')

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        data = mock_classification_class.get_data_train(data_path)

        mock_load_file.assert_called_once_with(os.path.join(data_path, 'train'))
        mock_parse_data.assert_called_once_with('annotations', 50000)
        assert data == 'dummy_data'

    def test_get_object_list(self, mocker, mock_classification_class):
        data = np.random.rand(10,3,32,32)
        fine_labels = np.array([1]*10, dtype=np.uint8)
        coarse_labels = np.array([2]*10, dtype=np.uint8)

        object_ids = mock_classification_class.get_object_list(data, fine_labels, coarse_labels)

        expected_object_ids = np.column_stack((np.array(range(10)), fine_labels, coarse_labels))
        assert_array_equal(object_ids, expected_object_ids)

    def test_get_images_per_class(self, mocker, mock_classification_class):
        labels = np.array([1,1,1,1,0,1,1,0])

        images_per_class = mock_classification_class.get_images_per_class(labels)

        expected = np.array([[4, 7, -1, -1, -1, -1],
                             [0, 1, 2, 3, 5, 6]],
                             dtype=np.int32)
        assert_array_equal(images_per_class, expected)

    def test_process_set_metadata(self, mocker, mock_classification_class):
        mock_save_hdf5 = mocker.patch.object(Classification, "save_field_to_hdf5")
        mock_class_field = mocker.patch.object(ClassLabelField, "process")
        mock_coarseclass_field = mocker.patch.object(CoarseClassLabelField, "process")

        data = {"classes": 1, "coarse_classes": 1, "images": 1, "labels": 1, "coarse_labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1, "list_images_per_superclass": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        mock_class_field.assert_called_once_with()
        mock_coarseclass_field.assert_called_once_with()
        assert mock_save_hdf5.called
        assert mock_save_hdf5.call_count == 9


class TestDatasetAnnotationLoader:
    """Unit tests for the DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            finer_classes=['beaver', 'dolphin', 'otter', 'seal', 'whale'],
            coarse_classes=['aquatic mammals', 'fish', 'flowers'],
            data_files = [
                "meta",
                "train",
                "test"
            ],
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.data_files == [
            "meta",
            "train",
            "test"
        ]
        assert mock_loader_class.data_path == '/some/path/data'
        assert mock_loader_class.cache_path == '/some/path/cache'
        assert mock_loader_class.verbose == True

    def test_load_train_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_data = mocker.patch.object(DatasetAnnotationLoader, 'load_data_set', return_value=dummy_data)

        data = mock_loader_class.load_train_data()

        mock_load_data.assert_called_once_with(is_test=False)
        assert data == dummy_data

    def test_load_test_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_data = mocker.patch.object(DatasetAnnotationLoader, 'load_data_set', return_value=dummy_data)

        data = mock_loader_class.load_test_data()

        mock_load_data.assert_called_once_with(is_test=True)
        assert data == dummy_data

    def test_load_data_set(self, mocker, mock_loader_class):
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_data_annotations", return_value=('images', 'labels', 'coarse_labels'))

        set_data = mock_loader_class.load_data_set(False)

        mock_load_annotations.assert_called_once_with(False)
        assert set_data['classes'] == mock_loader_class.finer_classes
        assert set_data['coarse_classes'] == mock_loader_class.coarse_classes
        assert set_data['images'] == 'images'
        assert set_data['labels'] == 'labels'

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations(self, mocker, mock_loader_class, is_test):
        mock_get_data_test = mocker.patch.object(DatasetAnnotationLoader, "get_data_test", return_value='test')
        mock_get_data_train = mocker.patch.object(DatasetAnnotationLoader, "get_data_train", return_value='train')

        annotations = mock_loader_class.load_data_annotations(is_test=is_test)

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        if is_test:
            mock_get_data_test.assert_called_once_with(data_path)
            mock_get_data_train.assert_not_called()
            assert annotations == 'test'
        else:
            mock_get_data_test.assert_not_called()
            mock_get_data_train.assert_called_once_with(data_path)
            assert annotations == 'train'

    def test_get_data_test(self, mocker, mock_loader_class):
        mock_load_file = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_file", return_value='annotations')
        mock_parse_data = mocker.patch.object(DatasetAnnotationLoader, "parse_data_annotations", return_value='dummy_data')

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        data = mock_loader_class.get_data_test(data_path)

        mock_load_file.assert_called_once_with(os.path.join(data_path, 'test'))
        mock_parse_data.assert_called_once_with('annotations', 10000)
        assert data == 'dummy_data'

    def test_parse_data_annotations(self, mocker, mock_loader_class):
        images = np.random.random((10, 3072))
        annotations = {
            "data": images,
            "fine_labels": range(10),
            "coarse_labels": range(5)
        }

        data, labels, coarse_labels = mock_loader_class.parse_data_annotations(annotations, 10)

        expected_images = np.transpose(images.reshape(10, 3, 32, 32), (0, 2, 3, 1))
        assert_array_equal(data, expected_images)
        assert_array_equal(labels, np.array(range(10), dtype=np.uint8))
        assert_array_equal(coarse_labels, np.array(range(5), dtype=np.uint8))

    def test_get_data_train(self, mocker, mock_loader_class):
        mock_load_file = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_file", return_value='annotations')
        mock_parse_data = mocker.patch.object(DatasetAnnotationLoader, "parse_data_annotations", return_value='dummy_data')

        data_path = os.path.join('/some/path/data', 'cifar-100-python')
        data = mock_loader_class.get_data_train(data_path)

        mock_load_file.assert_called_once_with(os.path.join(data_path, 'train'))
        mock_parse_data.assert_called_once_with('annotations', 50000)
        assert data == 'dummy_data'


@pytest.fixture()
def test_data_loaded():
    classes = [
        'beaver', 'dolphin', 'otter', 'seal', 'whale',
        'aquarium fish', 'flatfish', 'ray', 'shark', 'trout',
        'orchids', 'poppies', 'roses', 'sunflowers', 'tulips',
        'bottles', 'bowls', 'cans', 'cups', 'plates',
        'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers',
        'clock', 'computer keyboard', 'lamp', 'telephone', 'television'
    ]
    coarse_classes = ['aquatic mammals',
        'fish',
        'flowers',
        'food containers',
        'fruit and vegetables',
        'household electrical devices'
    ]
    images = np.random.rand(10,3,32,32)
    labels = np.random.randint(0,100,10)
    coarse_labels = np.random.randint(0,10,10)
    return {
            "images": images,
            "classes": classes,
            "coarse_classes": coarse_classes,
            "labels": labels,
            "coarse_labels": coarse_labels
        }


@pytest.fixture()
def field_kwargs(test_data_loaded):
    return {
        "data": test_data_loaded,
        "set_name": 'train',
        "hdf5_manager": {'dummy': 'object'},
        "verbose": True
    }


class TestClassLabelField:
    """Unit tests for the ClassLabelField class."""

    @staticmethod
    @pytest.fixture()
    def mock_classlabel_class(field_kwargs):
        return ClassLabelField(**field_kwargs)

    def test_process(self, mocker, mock_classlabel_class):
        dummy_names = ['car']*10
        mock_get_class = mocker.patch.object(ClassLabelField, "get_class_names", return_value=dummy_names)
        mock_save_hdf5 = mocker.patch.object(ClassLabelField, "save_field_to_hdf5")

        mock_classlabel_class.process()

        mock_get_class.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='classes',
        #     data=str2ascii(dummy_names),
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_class_names(self, mocker, mock_classlabel_class, test_data_loaded):
        class_names = mock_classlabel_class.get_class_names()

        assert class_names == test_data_loaded['classes']


class TestCoarseClassLabelField:
    """Unit tests for the CoarseClassLabelField class."""

    @staticmethod
    @pytest.fixture()
    def mock_coarseclasslabel_class(field_kwargs):
        return CoarseClassLabelField(**field_kwargs)

    def test_process(self, mocker, mock_coarseclasslabel_class):
        dummy_names = ['fish']*10
        mock_get_class = mocker.patch.object(CoarseClassLabelField, "get_class_names", return_value=dummy_names)
        mock_save_hdf5 = mocker.patch.object(CoarseClassLabelField, "save_field_to_hdf5")

        mock_coarseclasslabel_class.process()

        mock_get_class.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='coarse_classes',
        #     data=str2ascii(dummy_names),
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_class_names(self, mocker, mock_coarseclasslabel_class, test_data_loaded):
        class_names = mock_coarseclasslabel_class.get_class_names()

        assert class_names == test_data_loaded['coarse_classes']
