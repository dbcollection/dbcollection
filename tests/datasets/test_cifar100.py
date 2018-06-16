"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.datasets.cifar.cifar100.classification import (
    Classification,
    DatasetAnnotationLoader,
    ClassLabelField,
    SuperClassLabelField,
    ImageField,
    LabelIdField,
    SuperLabelIdField,
    ObjectFieldNamesField,
    ObjectIdsField,
    ImagesPerClassList,
    ImagesPerSuperClassList
)


@pytest.fixture()
def mock_classification_class():
    return Classification(
        data_path='/some/path/data',
        cache_path='/some/path/cache'
    )


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
        dummy_data = ['some_data']
        mock_load_train = mocker.patch.object(DatasetAnnotationLoader, "load_train_data", return_value=dummy_data)
        mock_load_test = mocker.patch.object(DatasetAnnotationLoader, "load_test_data", return_value=dummy_data)

        load_data_generator = mock_classification_class.load_data()

        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        mock_load_train.assert_called_once_with()
        mock_load_test.assert_called_once_with()
        assert train_data == {"train": ['some_data']}
        assert test_data == {"test": ['some_data']}

    def test_process_set_metadata(self, mocker, mock_classification_class):
        dummy_ids = [0, 1, 2, 3, 4, 5]
        mock_class_field = mocker.patch.object(ClassLabelField, "process")
        mock_coarseclass_field = mocker.patch.object(SuperClassLabelField, "process")
        mock_image_field = mocker.patch.object(ImageField, "process", return_value=dummy_ids)
        mock_label_field = mocker.patch.object(LabelIdField, "process", return_value=dummy_ids)
        mock_superlabel_field = mocker.patch.object(SuperLabelIdField, "process", return_value=dummy_ids)
        mock_objfields_field = mocker.patch.object(ObjectFieldNamesField, "process")
        mock_objids_field = mocker.patch.object(ObjectIdsField, "process")
        mock_images_list = mocker.patch.object(ImagesPerClassList, "process")
        mock_images_super_list = mocker.patch.object(ImagesPerSuperClassList, "process")

        data = {"classes": 1, "coarse_classes": 1, "images": 1, "labels": 1, "coarse_labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1, "list_images_per_superclass": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        mock_class_field.assert_called_once_with()
        mock_coarseclass_field.assert_called_once_with()
        mock_image_field.assert_called_once_with()
        mock_label_field.assert_called_once_with()
        mock_superlabel_field.assert_called_once_with()
        mock_objfields_field.assert_called_once_with()
        mock_objids_field.assert_called_once_with(dummy_ids, dummy_ids, dummy_ids)
        mock_images_list.assert_called_once_with()
        mock_images_super_list.assert_called_once_with()


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


class TestSuperClassLabelField:
    """Unit tests for the SuperClassLabelField class."""

    @staticmethod
    @pytest.fixture()
    def mock_coarseclasslabel_class(field_kwargs):
        return SuperClassLabelField(**field_kwargs)

    def test_process(self, mocker, mock_coarseclasslabel_class):
        dummy_names = ['fish']*10
        mock_get_class = mocker.patch.object(SuperClassLabelField, "get_class_names", return_value=dummy_names)
        mock_save_hdf5 = mocker.patch.object(SuperClassLabelField, "save_field_to_hdf5")

        mock_coarseclasslabel_class.process()

        mock_get_class.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='superclasses',
        #     data=str2ascii(dummy_names),
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_class_names(self, mocker, mock_coarseclasslabel_class, test_data_loaded):
        class_names = mock_coarseclasslabel_class.get_class_names()

        assert class_names == test_data_loaded['coarse_classes']


class TestImageField:
    """Unit tests for the ImageField class."""

    @staticmethod
    @pytest.fixture()
    def mock_image_class(field_kwargs):
        return ImageField(**field_kwargs)

    def test_process(self, mocker, mock_image_class):
        dummy_images = np.random.rand(5,3, 32, 32)
        dummy_ids = list(range(5))
        mock_get_images = mocker.patch.object(ImageField, "get_images", return_value=(dummy_images, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(ImageField, "save_field_to_hdf5")

        image_ids = mock_image_class.process()

        assert image_ids == dummy_ids
        mock_get_images.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='images',
        #     data=dummy_images,
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_images(self, mocker, mock_image_class, test_data_loaded):
        images, image_ids = mock_image_class.get_images()

        assert_array_equal(images, test_data_loaded['images'])
        assert image_ids == list(range(len(images)))


class TestLabelIdField:
    """Unit tests for the LabelIdField class."""

    @staticmethod
    @pytest.fixture()
    def mock_label_class(field_kwargs):
        return LabelIdField(**field_kwargs)

    def test_process(self, mocker, mock_label_class):
        dummy_labels = np.array(range(10))
        dummy_ids = list(range(10))
        mock_get_labels = mocker.patch.object(LabelIdField, "get_labels", return_value=(dummy_labels, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(LabelIdField, "save_field_to_hdf5")

        label_ids = mock_label_class.process()

        assert label_ids == dummy_ids
        mock_get_labels.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='labels',
        #     data=dummy_labels,
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_labels(self, mocker, mock_label_class, test_data_loaded):
        labels, label_ids = mock_label_class.get_labels()

        assert_array_equal(labels, test_data_loaded['labels'])
        assert label_ids == list(range(len(labels)))


class TestSuperLabelIdField:
    """Unit tests for the SuperLabelIdField class."""

    @staticmethod
    @pytest.fixture()
    def mock_superlabel_class(field_kwargs):
        return SuperLabelIdField(**field_kwargs)

    def test_process(self, mocker, mock_superlabel_class):
        dummy_labels = np.array(range(10))
        dummy_ids = list(range(10))
        mock_get_labels = mocker.patch.object(SuperLabelIdField, "get_super_labels", return_value=(dummy_labels, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(SuperLabelIdField, "save_field_to_hdf5")

        super_label_ids = mock_superlabel_class.process()

        assert super_label_ids == dummy_ids
        mock_get_labels.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='superlabels',
        #     data=dummy_labels,
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_super_labels(self, mocker, mock_superlabel_class, test_data_loaded):
        super_labels, super_label_ids = mock_superlabel_class.get_super_labels()

        assert_array_equal(super_labels, test_data_loaded['coarse_labels'])
        assert super_label_ids == list(range(len(super_labels)))


class TestObjectFieldNamesField:
    """Unit tests for the ObjectFieldNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objfields_class(field_kwargs):
        return ObjectFieldNamesField(**field_kwargs)

    def test_process(self, mocker, mock_objfields_class):
        mock_save_hdf5 = mocker.patch.object(ObjectFieldNamesField, "save_field_to_hdf5")

        mock_objfields_class.process()

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_fields',
        #     data=str2ascii(['images', 'labels', 'superlabels']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )


class TestObjectIdsField:
    """Unit tests for the ObjectIdsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objfids_class(field_kwargs):
        return ObjectIdsField(**field_kwargs)

    def test_process(self, mocker, mock_objfids_class):
        mock_save_hdf5 = mocker.patch.object(ObjectIdsField, "save_field_to_hdf5")

        image_ids = [0, 1, 2, 3, 4, 5]
        label_ids = [11, 35, 29, 8, 33, 45]
        super_label_ids = [1, 5, 9, 8, 3, 5]
        object_ids = mock_objfids_class.process(
            image_ids=image_ids,
            label_ids=label_ids,
            super_label_ids=super_label_ids
        )

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_ids',
        #     data=np.array([[0, 11, 1], [1, 35, 5], [2, 29, 9], [3, 8, 8], [4, 33, 3], [5, 45, 5]], dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )


class TestImagesPerClassList:
    """Unit tests for the ImagesPerClassList class."""

    @staticmethod
    @pytest.fixture()
    def mock_img_per_class_list(field_kwargs):
        return ImagesPerClassList(**field_kwargs)

    def test_process(self, mocker, mock_img_per_class_list):
        dummy_ids = [[0], [2, 3], [4, 5]]
        dummy_array = np.array([[0, -1], [2, 3], [4, 5]])
        mock_get_ids = mocker.patch.object(ImagesPerClassList, "get_image_ids_per_class", return_value=dummy_ids)
        mock_convert_array = mocker.patch.object(ImagesPerClassList, "convert_list_to_array", return_value=dummy_array)
        mock_save_hdf5 = mocker.patch.object(ImagesPerClassList, "save_field_to_hdf5")

        mock_img_per_class_list.process()

        mock_get_ids.assert_called_once_with()
        mock_convert_array.assert_called_once_with(dummy_ids)
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_images_per_class',
        #     data=dummy_array,
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_image_ids_per_class(self, mocker, mock_img_per_class_list):
        mock_img_per_class_list.data['labels'] = list(range(10))
        images_per_class_ids = mock_img_per_class_list.get_image_ids_per_class()

        assert images_per_class_ids == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    def test_convert_list_to_array(self, mocker, mock_img_per_class_list):
        list_ids = [[0], [2, 3], [4, 5, 6]]
        images_per_class_array = mock_img_per_class_list.convert_list_to_array(list_ids)

        expected = np.array(pad_list([[0, -1, -1], [2, 3, -1], [4, 5, 6]], -1), dtype=np.int32)
        assert_array_equal(images_per_class_array, expected)


class TestImagesPerSuperClassList:
    """Unit tests for the ImagesPerSuperClassList class."""

    @staticmethod
    @pytest.fixture()
    def mock_img_per_super_class_list(field_kwargs):
        return ImagesPerSuperClassList(**field_kwargs)

    def test_process(self, mocker, mock_img_per_super_class_list):
        dummy_ids = [[0], [2, 3], [4, 5]]
        dummy_array = np.array([[0, -1], [2, 3], [4, 5]])
        mock_get_ids = mocker.patch.object(ImagesPerSuperClassList, "get_image_ids_per_super_class", return_value=dummy_ids)
        mock_convert_array = mocker.patch.object(ImagesPerSuperClassList, "convert_list_to_array", return_value=dummy_array)
        mock_save_hdf5 = mocker.patch.object(ImagesPerSuperClassList, "save_field_to_hdf5")

        mock_img_per_super_class_list.process()

        mock_get_ids.assert_called_once_with()
        mock_convert_array.assert_called_once_with(dummy_ids)
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_images_per_superclass',
        #     data=dummy_array,
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_image_ids_per_super_class(self, mocker, mock_img_per_super_class_list):
        mock_img_per_super_class_list.data['coarse_labels'] = list(range(10))
        images_per_super_class_ids = mock_img_per_super_class_list.get_image_ids_per_super_class()

        assert images_per_super_class_ids == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    def test_convert_list_to_array(self, mocker, mock_img_per_super_class_list):
        list_ids = [[0], [2, 3], [4, 5, 6]]
        images_per_super_class_array = mock_img_per_super_class_list.convert_list_to_array(list_ids)

        expected = np.array(pad_list([[0, -1, -1], [2, 3, -1], [4, 5, 6]], -1), dtype=np.int32)
        assert_array_equal(images_per_super_class_array, expected)
