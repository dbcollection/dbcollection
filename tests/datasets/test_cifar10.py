"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.datasets.cifar.cifar10.classification import (
    Classification,
    DatasetAnnotationLoader,
    BaseField,
    ClassLabelField,
    ImageField,
    LabelIdField,
    ObjectFieldNamesField
)


class TestClassificationTask:
    """Unit tests for the cifar10 Classification task."""

    @staticmethod
    @pytest.fixture()
    def mock_classification_class():
        return Classification(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_classification_class):
        assert mock_classification_class.filename_h5 == 'classification'
        assert mock_classification_class.data_files == ["batches.meta",
                                                        "data_batch_1",
                                                        "data_batch_2",
                                                        "data_batch_3",
                                                        "data_batch_4",
                                                        "data_batch_5",
                                                        "test_batch"]

    def test_load_data(self, mocker, mock_classification_class):
        dummy_data = {"dummy": 'data'}
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
        assert train_data == {"train": dummy_data}
        assert test_data == {"test": dummy_data}

    def test_load_data_set(self, mocker, mock_classification_class):
        mock_load_annotations = mocker.patch.object(Classification, "load_data_annotations", return_value=('data', 'labels', {"label_names": 'some_class'}))
        mock_get_object_list = mocker.patch.object(Classification, "get_object_list", return_value=list(range(10)))
        mock_get_list = mocker.patch.object(Classification, "get_images_per_class", return_value=list(range(5)))

        set_data = mock_classification_class.load_data_set(False)

        mock_load_annotations.assert_called_once_with(False)
        mock_get_object_list.assert_called_once_with('data', 'labels')
        mock_get_list.assert_called_once_with('labels')
        assert_array_equal(set_data['object_fields'], str2ascii(['images', 'classes']))
        assert_array_equal(set_data['classes'], str2ascii(['some_class']))
        assert set_data['images'] == 'data'
        assert set_data['labels'] == 'labels'
        assert set_data['object_ids'] == list(range(10))
        assert set_data['list_images_per_class'] == list(range(5))

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations_for_train_set(self, mocker, mock_classification_class, is_test):
        random_data = np.random.rand(20,3,32,32)
        mock_get_names = mocker.patch.object(Classification, "get_class_names", return_value=['some', 'class', 'names'])
        mock_get_data_test = mocker.patch.object(Classification, "get_data_test", return_value=(random_data, np.array(range(10))))
        mock_get_data_train = mocker.patch.object(Classification, "get_data_train", return_value=(random_data, np.array(range(10))))

        data_path = os.path.join(mock_classification_class.data_path, 'cifar-10-batches-py')
        data, labels, class_names = mock_classification_class.load_data_annotations(is_test=is_test)

        mock_get_names.assert_called_once_with(data_path)
        if is_test:
            mock_get_data_test.assert_called_once_with(data_path)
            assert not mock_get_data_train.called
        else:
            assert not mock_get_data_test.called
            mock_get_data_train.assert_called_once_with(data_path)
        assert_array_equal(data, np.transpose(random_data, (0, 2, 3, 1)))
        assert_array_equal(labels, np.array(range(10)))
        assert class_names == ['some', 'class', 'names']

    def test_get_class_names(self, mocker, mock_classification_class):
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value='dummy_data')

        path = mock_classification_class.data_path
        result = mock_classification_class.get_class_names(path)

        filename = os.path.join(path, "batches.meta")
        mock_load_annot_file.assert_called_once_with(filename)
        assert result == 'dummy_data'

    def test_get_data_train(self, mocker, mock_classification_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        test_data_concat = np.concatenate(
            (test_data['data'], test_data['data'], test_data['data'], test_data['data'], test_data['data']),
            axis=0
        )
        output_data = test_data_concat.reshape(50,3,32,32)
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(Classification, "reshape_array", return_value=output_data)

        path = mock_classification_class.data_path
        data, labels = mock_classification_class.get_data_train(path)

        assert mock_load_annot_file.called
        assert mock_load_annot_file.call_count == 5
        #mock_reshape_array.assert_called_once_with(test_data_concat, 50000)
        assert mock_reshape_array.called
        assert_array_equal(data, output_data)
        assert_array_equal(labels, np.concatenate(
            (test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels']),
            axis=0)
        )

    def test_reshape_array(self, mocker, mock_classification_class):
        data = np.random.rand(20, 3*32*32)

        result = mock_classification_class.reshape_array(data, 20)

        assert_array_equal(result, data.reshape(20, 3, 32, 32))

    def test_get_data_test(self, mocker, mock_classification_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(Classification, "reshape_array", return_value=test_data['data'].reshape(10, 3, 32, 32))

        path = mock_classification_class.data_path
        data, labels = mock_classification_class.get_data_test(path)

        mock_load_annot_file.assert_called_once_with(os.path.join(path, 'test_batch'))
        mock_reshape_array.assert_called_once_with(test_data['data'], 10000)
        assert_array_equal(data, test_data['data'].reshape((10, 3, 32, 32)))
        assert_array_equal(labels, test_data['labels'])

    def test_get_object_list(self, mocker, mock_classification_class):
        data = np.random.rand(20,2,32,32)
        labels = np.array(range(20))

        object_ids = mock_classification_class.get_object_list(data, labels)

        assert_array_equal(object_ids, np.array([[i, labels[i]] for i in range(20)]))

    def test_get_images_per_class(self, mocker, mock_classification_class):
        labels = np.array([1,1,1,1,0,1,1,0])

        images_per_class = mock_classification_class.get_images_per_class(labels)

        expected = np.array([[4, 7, -1, -1, -1, -1],
                             [0, 1, 2, 3, 5, 6]],
                             dtype=np.int32)
        assert_array_equal(images_per_class, expected)

    def test_process_set_metadata(self, mocker, mock_classification_class):
        dummy_ids = list(range(10))
        mock_save_hdf5 = mocker.patch.object(Classification, "save_field_to_hdf5")
        mock_class_field = mocker.patch.object(ClassLabelField, "process")
        mock_image_field = mocker.patch.object(ImageField, "process", return_value=dummy_ids)
        mock_label_field = mocker.patch.object(LabelIdField, "process", return_value=dummy_ids)
        mock_objfield_field = mocker.patch.object(ObjectFieldNamesField, "process")

        data = {"classes": 1, "images": 1, "labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        mock_class_field.assert_called_once_with()
        mock_image_field.assert_called_once_with()
        mock_label_field.assert_called_once_with()
        mock_objfield_field.assert_called_once_with()
        assert mock_save_hdf5.called
        assert mock_save_hdf5.call_count == 6


class TestDatasetAnnotationLoader:
    """Unit tests for the DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            data_files = [
                "batches.meta",
                "data_batch_1",
                "data_batch_2",
                "data_batch_3",
                "data_batch_4",
                "data_batch_5",
                "test_batch"
            ],
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.data_files == [
            "batches.meta",
            "data_batch_1",
            "data_batch_2",
            "data_batch_3",
            "data_batch_4",
            "data_batch_5",
            "test_batch"
        ]
        assert mock_loader_class.data_path=='/some/path/data'
        assert mock_loader_class.cache_path=='/some/path/cache'
        assert mock_loader_class.verbose==True

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
        dummy_images = np.random.rand(10,3,32,32)
        dummy_labels = np.array(range(10))
        dummy_class_names = ['dummy_name']*10
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_data_annotations", return_value=(dummy_images, dummy_labels, dummy_class_names))

        set_data = mock_loader_class.load_data_set(False)

        mock_load_annotations.assert_called_once_with(False)
        assert set_data['classes'] == dummy_class_names
        assert_array_equal(set_data['images'], dummy_images)
        assert_array_equal(set_data['labels'], dummy_labels)

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations_for_train_set(self, mocker, mock_loader_class, is_test):
        random_data = np.random.rand(20,3,32,32)
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_class_names", return_value=['some', 'class', 'names'])
        mock_get_data_test = mocker.patch.object(DatasetAnnotationLoader, "get_data_test", return_value=(random_data, np.array(range(10))))
        mock_get_data_train = mocker.patch.object(DatasetAnnotationLoader, "get_data_train", return_value=(random_data, np.array(range(10))))

        data_path = os.path.join(mock_loader_class.data_path, 'cifar-10-batches-py')
        data, labels, class_names = mock_loader_class.load_data_annotations(is_test=is_test)

        mock_get_names.assert_called_once_with(data_path)
        if is_test:
            mock_get_data_test.assert_called_once_with(data_path)
            assert not mock_get_data_train.called
        else:
            assert not mock_get_data_test.called
            mock_get_data_train.assert_called_once_with(data_path)
        assert_array_equal(data, np.transpose(random_data, (0, 2, 3, 1)))
        assert_array_equal(labels, np.array(range(10)))
        assert class_names == ['some', 'class', 'names']

    def test_get_class_names(self, mocker, mock_loader_class):
        mock_load_annot_file = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_file", return_value='dummy_data')

        path = mock_loader_class.data_path
        result = mock_loader_class.get_class_names(path)

        filename = os.path.join(path, "batches.meta")
        mock_load_annot_file.assert_called_once_with(filename)
        assert result == 'dummy_data'

    def test_get_data_train(self, mocker, mock_loader_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        test_data_concat = np.concatenate(
            (test_data['data'], test_data['data'], test_data['data'], test_data['data'], test_data['data']),
            axis=0
        )
        output_data = test_data_concat.reshape(50,3,32,32)
        mock_load_annot_file = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(DatasetAnnotationLoader, "reshape_array", return_value=output_data)

        path = mock_loader_class.data_path
        data, labels = mock_loader_class.get_data_train(path)

        assert mock_load_annot_file.called
        assert mock_load_annot_file.call_count == 5
        assert mock_reshape_array.called
        assert_array_equal(data, output_data)
        assert_array_equal(labels, np.concatenate(
            (test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels']),
            axis=0)
        )

    def test_reshape_array(self, mocker, mock_loader_class):
        data = np.random.rand(20, 3*32*32)

        result = mock_loader_class.reshape_array(data, 20)

        assert_array_equal(result, data.reshape(20, 3, 32, 32))

    def test_get_data_test(self, mocker, mock_loader_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        mock_load_annot_file = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(DatasetAnnotationLoader, "reshape_array", return_value=test_data['data'].reshape(10, 3, 32, 32))

        path = mock_loader_class.data_path
        data, labels = mock_loader_class.get_data_test(path)

        mock_load_annot_file.assert_called_once_with(os.path.join(path, 'test_batch'))
        mock_reshape_array.assert_called_once_with(test_data['data'], 10000)
        assert_array_equal(data, test_data['data'].reshape((10, 3, 32, 32)))
        assert_array_equal(labels, test_data['labels'])


@pytest.fixture()
def test_data_loaded():
    classes = ['airplane']*10
    images = np.random.rand(10,3,32,32)
    labels = np.array(range(10))
    return {
            "classes": classes,
            "images": images,
            "labels": labels
        }


@pytest.fixture()
def field_kwargs(test_data_loaded):
    return {
        "data": test_data_loaded,
        "set_name": 'train',
        "hdf5_manager": {'dummy': 'object'},
        "verbose": True
    }

class TestBaseField:
    """Unit tests for the BaseField class."""

    @staticmethod
    @pytest.fixture()
    def mock_base_class(field_kwargs):
        return BaseField(**field_kwargs)

    def test_init(self, mocker):
        data = ['some', 'data']
        set_name = 'train'
        hdf5_manager = {'dummy': 'object'}
        verbose = True

        base_field = BaseField(data, set_name, hdf5_manager, verbose)

        assert base_field.data == data
        assert base_field.set_name == set_name
        assert base_field.hdf5_manager == hdf5_manager
        assert base_field.verbose == verbose

    def test_save_field_to_hdf5(self, mocker, mock_base_class):
        mock_manager = mocker.MagicMock()

        set_name = 'test'
        field = 'dummy_field'
        data = np.random.rand(2,2)
        args = {"dtype" : np.uint8, "chunks": True}

        mock_base_class.hdf5_manager = mock_manager
        mock_base_class.save_field_to_hdf5(
            set_name=set_name,
            field=field,
            data=data,
            **args
        )

        mock_manager.add_field_to_group.assert_called_once_with(
            group=set_name,
            field=field,
            data=data,
            **args
        )

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

    def test_get_images(self, mocker, mock_label_class, test_data_loaded):
        labels, label_ids = mock_label_class.get_labels()

        assert_array_equal(labels, test_data_loaded['labels'])
        assert label_ids == list(range(len(labels)))


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
        #     data=str2ascii(['images', 'classes']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )
