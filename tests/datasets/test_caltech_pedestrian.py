"""
Test the base classes for managing datasets and tasks.

Dataset: Caltech Pedestrian

Tasks: Detection, Detection10x, Detection30x
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.datasets.caltech.caltech_pedestrian.detection import (
    Detection,
    BaseField,
    BoundingBoxBaseField,
    BoundingBoxField,
    BoundingBoxPerImageList,
    BoundingBoxvField,
    BoundingBoxvPerImageList,
    ClassLabelField,
    DatasetLoader,
    ImageFilenamesField,
    ImageFilenamesPerClassList,
    LabelIdField,
    ObjectFieldNamesField,
    ObjectIdsField,
    ObjectsPerClassList,
    ObjectsPerImageList,
    OcclusionField,
)


@pytest.fixture()
def test_data():
    return {
        "set00": {
            "V000": {"images": ['image1.jpg', 'image2.jpg'], "annotations": ['annotation1.json', 'annotation2.json']},
            "V001": {"images": ['image3.jpg', 'image4.jpg'], "annotations": ['annotation3.json', 'annotation4.json']}
        },
        "set01": {
            "V000": {"images": ['image5.jpg', 'image6.jpg'], "annotations": ['annotation5.json', 'annotation6.json']},
            "V001": {"images": ['image7.jpg', 'image8.jpg'], "annotations": ['annotation7.json', 'annotation8.json']}
        },
    }


class TestDetectionTask:
    """Unit tests for the caltech pedestrian Detection task."""

    @staticmethod
    @pytest.fixture()
    def mock_detection_class():
        return Detection(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_detection_class):
        assert mock_detection_class.filename_h5 == 'detection'
        assert mock_detection_class.skip_step == 30
        assert mock_detection_class.classes == ('person', 'person-fa', 'people', 'person?')
        assert mock_detection_class.sets == {
            "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
            "test": ('set06', 'set07', 'set08', 'set09', 'set10')
        }

    def test_load_data(self, mocker, mock_detection_class):
        dummy_data = ['some_data']
        mock_load_train = mocker.patch.object(DatasetLoader, "load_train_data", return_value=dummy_data)
        mock_load_test = mocker.patch.object(DatasetLoader, "load_test_data", return_value=dummy_data)

        load_data_generator = mock_detection_class.load_data()

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

    def test_process_set_metadata(self, mocker, mock_detection_class, test_data):
        classes = ('person', 'person-fa', 'people', 'person?')
        dummy_ids = list(range(6))
        dummy_object_ids = [[i, i, i, i, i, i] for i in range(6)]
        mock_classes_field = mocker.patch.object(ClassLabelField, "process", return_value=(dummy_ids, dummy_ids))
        mock_image_field = mocker.patch.object(ImageFilenamesField, "process", return_value=(dummy_ids, [0, 0, 0, 1, 1, 1]))
        mock_bbox_field = mocker.patch.object(BoundingBoxField, "process", return_value=dummy_ids)
        mock_bboxv_field = mocker.patch.object(BoundingBoxvField, "process", return_value=dummy_ids)
        mock_lblid_field = mocker.patch.object(LabelIdField, "process", return_value=dummy_ids)
        mock_occlusion_field = mocker.patch.object(OcclusionField, "process", return_value=dummy_ids)
        mock_objfields_field = mocker.patch.object(ObjectFieldNamesField, "process")
        mock_objids_field = mocker.patch.object(ObjectIdsField, "process", return_value=dummy_object_ids)
        mock_img_per_class_list = mocker.patch.object(ImageFilenamesPerClassList, "process")
        mock_bbox_per_img_list = mocker.patch.object(BoundingBoxPerImageList, "process")
        mock_bboxv_per_img_list = mocker.patch.object(BoundingBoxvPerImageList, "process")
        mock_object_per_img_list = mocker.patch.object(ObjectsPerImageList, "process")
        mock_object_per_class_list = mocker.patch.object(ObjectsPerClassList, "process")

        mock_detection_class.process_set_metadata(test_data, 'train')

        mock_classes_field.assert_called_once_with(classes)
        mock_image_field.assert_called_once_with()
        mock_bbox_field.assert_called_once_with()
        mock_bboxv_field.assert_called_once_with()
        mock_lblid_field.assert_called_once_with()
        mock_occlusion_field.assert_called_once_with()
        mock_objfields_field.assert_called_once_with()
        mock_objids_field.assert_called_once_with(
            image_filenames_ids=dummy_ids,
            class_ids=dummy_ids,
            bbox_ids=dummy_ids,
            bboxv_ids=dummy_ids,
            label_ids=dummy_ids,
            occlusion_ids=dummy_ids
        )
        mock_img_per_class_list.assert_called_once_with([0, 0, 0, 1, 1, 1], dummy_ids)
        mock_bbox_per_img_list.assert_called_once_with(dummy_object_ids, [0, 0, 0, 1, 1, 1])
        mock_bboxv_per_img_list.assert_called_once_with(dummy_object_ids, [0, 0, 0, 1, 1, 1])
        mock_object_per_img_list.assert_called_once_with(dummy_object_ids, [0, 0, 0, 1, 1, 1])
        mock_object_per_class_list.assert_called_once_with(dummy_object_ids, dummy_ids)


class TestDatasetLoader:
    """Unit tests for the DatasetLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetLoader(
            skip_step=30,
            classes=('person', 'person-fa', 'people', 'person?'),
            sets={
                "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
                "test": ('set06', 'set07', 'set08', 'set09', 'set10')
            },
            is_clean=False,
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.skip_step == 30
        assert mock_loader_class.classes == ('person', 'person-fa', 'people', 'person?')
        assert mock_loader_class.sets == {
            "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
            "test": ('set06', 'set07', 'set08', 'set09', 'set10')
        }
        assert mock_loader_class.is_clean == False
        assert mock_loader_class.data_path=='/some/path/data'
        assert mock_loader_class.cache_path=='/some/path/cache'
        assert mock_loader_class.verbose==True

    def test_load_data_set(self, mocker, mock_loader_class):
        dummy_images, dummy_annotations = ['image1.jpg', 'image2.jpg'], ['annot1.json', 'annot2.json']
        dummy_annot_data = ['obj1', 'obj2']
        mock_unpack_data = mocker.patch.object(DatasetLoader, "unpack_raw_data_files", return_value='/some/path/data/')
        mock_get_partitions = mocker.patch.object(DatasetLoader, "get_set_partitions", return_value=('train', ('set00', 'set01')))
        mock_get_annotations = mocker.patch.object(DatasetLoader, "get_annotations_data", return_value=(dummy_images, dummy_annotations))
        mock_load_annotations = mocker.patch.object(DatasetLoader, "load_annotations", return_value=dummy_annot_data)

        set_data = mock_loader_class.load_data_set(False)

        mock_unpack_data.assert_called_once_with()
        mock_get_partitions.assert_called_once_with(is_test=False)
        mock_get_annotations.assert_called_once_with('train', ('set00', 'set01'), '/some/path/data/')
        mock_load_annotations.assert_called_once_with(dummy_annotations)
        assert sorted(list(set_data.keys())) == ["annotations", "image_filenames"]
        assert set_data["image_filenames"] == dummy_images
        assert set_data["annotations"] == dummy_annot_data

    @pytest.mark.parametrize('is_test', [False, True])
    def test_get_set_partitions(self, mocker, mock_loader_class, is_test):
        set_name, partitions = mock_loader_class.get_set_partitions(is_test=is_test)

        if is_test:
            assert set_name == 'test'
            assert partitions == ('set06', 'set07', 'set08', 'set09', 'set10')
        else:
            assert set_name == 'train'
            assert partitions == ('set00', 'set01', 'set02', 'set03', 'set04', 'set05')

    def test_get_annotations_data(self, mocker, mock_loader_class):
        test_data = {"images": ['image1', 'image2'], "annotations": ['annotation1', 'annotation2']}
        mock_get_annotations = mocker.patch.object(DatasetLoader, 'get_annotations_from_partition', return_value=test_data)

        set_name = 'train'
        partitions = ('set00', 'set01')
        unpack_dir = os.path.join('some', 'path', 'to', 'extracted', 'data', 'dir')
        image_filenames, annotation_filenames = mock_loader_class.get_annotations_data(set_name, partitions, unpack_dir)

        assert mock_get_annotations.call_count == 2
        assert image_filenames == {"set00": test_data['images'], "set01": test_data['images']}
        assert annotation_filenames == {"set00": test_data['annotations'], "set01": test_data['annotations']}

    def test_get_annotations_from_partition(self, mocker, mock_loader_class):
        mock_get_dirs = mocker.patch.object(DatasetLoader, 'get_sorted_object_names_from_dir', return_value=('V000', 'V001'))
        mock_get_image_fnames = mocker.patch.object(DatasetLoader, 'get_image_filenames_from_dir', return_value=['image1.jpg', 'image2.jpg'])
        mock_get_annotation_fnames = mocker.patch.object(DatasetLoader, 'get_annotation_filenames_from_dir', return_value=['annotation1.json', 'annotation2.json'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        partition_annotations = mock_loader_class.get_annotations_from_partition(path, partition)

        mock_get_dirs.assert_called_once_with(os.path.join(path, partition))
        assert mock_get_image_fnames.call_count  == 2
        assert mock_get_annotation_fnames.call_count  == 2
        assert partition_annotations == {
            "images": {
                "V000": ['image1.jpg', 'image2.jpg'],
                "V001": ['image1.jpg', 'image2.jpg']
            },
            "annotations":{
                "V000": ['annotation1.json', 'annotation2.json'],
                "V001": ['annotation1.json', 'annotation2.json'],
            }
        }

    def test_get_sorted_object_names_from_dir(self, mocker, mock_loader_class):
        mock_listdir = mocker.patch('os.listdir', return_value=['dir2', 'dir1', 'dir3'])

        path = os.path.join('some', 'path', 'to', 'dir')
        object_names = mock_loader_class.get_sorted_object_names_from_dir(path)

        mock_listdir.assert_called_once_with(path)
        assert object_names == ['dir1', 'dir2', 'dir3']

    def test_get_image_filenames_from_dir(self, mocker, mock_loader_class):
        mock_get_data = mocker.patch.object(DatasetLoader, 'get_sample_data_from_dir', return_value=['image1.jpg', 'image2.jpg'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        image_filenames = mock_loader_class.get_image_filenames_from_dir(path, partition, video)

        mock_get_data.assert_called_once_with(path, partition, video, 'images')
        assert image_filenames == ['image1.jpg', 'image2.jpg']

    def test_get_sample_data_from_dir(self, mocker, mock_loader_class):
        mock_get_filenames = mocker.patch.object(DatasetLoader, 'get_sorted_object_names_from_dir', return_value=['filename1', 'filename2'])
        mock_get_sample = mocker.patch.object(DatasetLoader, 'get_sample_filenames', return_value=['filename1', 'filename2'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        type_data = 'images'
        sample_filepaths = mock_loader_class.get_sample_data_from_dir(path, partition, video, type_data)

        annot_path = os.path.join(mock_loader_class.data_path, 'extracted_data', partition, video, type_data)
        filepaths = [os.path.join(annot_path, filename) for filename in ['filename1', 'filename2']]
        mock_get_filenames.assert_called_once_with(os.path.join(path, partition, video, type_data))
        mock_get_sample.assert_called_once_with(filepaths, mock_loader_class.skip_step)
        assert sample_filepaths == ['filename1', 'filename2']

    def test_get_sample_filenames(self, mocker, mock_loader_class):
        filenames = ['filename1', 'filename2', 'filename3', 'filename4', 'filename5']
        skip_step = 2

        sample = mock_loader_class.get_sample_filenames(filenames, skip_step)

        assert sample == ['filename2', 'filename4']

    def test_get_annotation_filenames_from_dir(self, mocker, mock_loader_class):
        mock_get_data = mocker.patch.object(DatasetLoader, 'get_sample_data_from_dir', return_value=['annotation1.json', 'annotation2.json'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        annotation_filenames = mock_loader_class.get_annotation_filenames_from_dir(path, partition, video)

        mock_get_data.assert_called_once_with(path, partition, video, 'annotations')
        assert annotation_filenames == ['annotation1.json', 'annotation2.json']

    def test_load_annotations(self, mocker, mock_loader_class, test_data):
        dummy_annotation = [{"pos": [0, 0, 0, 0]}, {"pos": [10, 10, 10, 10]}]
        mock_load_annotation = mocker.patch.object(DatasetLoader, "load_annotation_file", return_value=dummy_annotation)

        annotations = mock_loader_class.load_annotations(test_data)

        assert mock_load_annotation.call_count== 8
        assert annotations == {
            "set00": {
                "V000": [dummy_annotation, dummy_annotation],
                "V001": [dummy_annotation, dummy_annotation]
                },
            "set01": {
                    "V000": [dummy_annotation, dummy_annotation],
                    "V001": [dummy_annotation, dummy_annotation]
                },
        }


@pytest.fixture()
def test_data_loaded():
    return {
        "image_filenames": {
           "set00": {
                "V000": ['image1.jpg'],
                "V001": ['image2.jpg']
            },
            "set01": {
                "V000": ['image3.jpg'],
                "V001": ['image4.jpg', 'image5.jpg']
            },
        },
        "annotations": {
           "set00": {
                "V000": [[{"pos": [1,1,3,3]}, {"pos": [10,10,20,20]}]],
                "V001": [[{"pos": [1,1,6,6]}, {"pos": [10,10,4,5]}]]
            },
            "set01": {
                "V000": [[{"pos": [1,1,1,1]}, {"pos": [5,10,5,20]}]],
                "V001": [[{"pos": [6,6,6,6]}, {"pos": [10,10,1,1]}], []]
            },
        }
    }


@pytest.fixture()
def field_kwargs(test_data_loaded):
    return {
        "data": test_data_loaded,
        "set_name": 'train',
        "is_clean": True,
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
        is_clean = True
        hdf5_manager = {'dummy': 'object'}
        verbose = True

        base_field = BaseField(data, set_name, is_clean, hdf5_manager, verbose)

        assert base_field.data == data
        assert base_field.set_name == set_name
        assert base_field.is_clean == is_clean
        assert base_field.hdf5_manager == hdf5_manager
        assert base_field.verbose == verbose

    @pytest.mark.parametrize('is_clean', [False, True])
    def test_get_annotation_objects_generator(self, mocker, mock_base_class, is_clean):
        mock_base_class.is_clean = is_clean
        generator = mock_base_class.get_annotation_objects_generator()

        results = [d for d in generator]
        if is_clean:
            assert results == [
                {"obj": {"pos": [10,10,20,20]}, "image_counter": 0, "obj_counter": 0},
                {"obj": {"pos": [1,1,6,6]}, "image_counter": 1, "obj_counter": 1},
                {"obj": {"pos": [5,10,5,20]}, "image_counter": 2, "obj_counter": 2},
                {"obj": {"pos": [6,6,6,6]}, "image_counter": 3, "obj_counter": 3}
            ]
        else:
            assert results == [
                {"obj": {"pos": [1,1,3,3]}, "image_counter": 0, "obj_counter": 0},
                {"obj": {"pos": [10,10,20,20]}, "image_counter": 0, "obj_counter": 1},
                {"obj": {"pos": [1,1,6,6]}, "image_counter": 1, "obj_counter": 2},
                {"obj": {"pos": [10,10,4,5]}, "image_counter": 1, "obj_counter": 3},
                {"obj": {"pos": [1,1,1,1]}, "image_counter": 2, "obj_counter": 4},
                {"obj": {"pos": [5,10,5,20]}, "image_counter": 2, "obj_counter": 5},
                {"obj": {"pos": [6,6,6,6]}, "image_counter": 3, "obj_counter": 6},
                {"obj": {"pos": [10,10,1,1]}, "image_counter": 3, "obj_counter": 7}
            ]

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
        dummy_names = ['person', 'person-fa', 'person-fa', 'people', 'people', 'person?']
        dummy_ids = [0, 1, 2, 3, 4, 5]
        dummy_unique_ids = [0, 1, 1, 2, 2, 3]
        mock_get_class_ids = mocker.patch.object(ClassLabelField, "get_class_labels_ids", return_value=(dummy_names, dummy_ids, dummy_unique_ids))
        mock_save_hdf5 = mocker.patch.object(ClassLabelField, "save_field_to_hdf5")

        classes = ('person', 'person-fa', 'people', 'person?')
        class_ids, class_unique_ids = mock_classlabel_class.process(classes)

        assert class_ids == dummy_ids
        assert class_unique_ids == dummy_unique_ids
        mock_get_class_ids.assert_called_once_with(classes)
        assert mock_save_hdf5.call_count == 2
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='classes',
        #     data=str2ascii(classes),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    def test_get_class_labels_ids(self, mocker, mock_classlabel_class):
        def dummy_generator():
            labels = ('person', 'person', 'person-fa', 'person-fa', 'people', 'people', 'person?')
            for i, label in enumerate(labels):
                yield {"obj": {"lbl": label}, "obj_counter": i}
        mock_get_generator = mocker.patch.object(ClassLabelField, "get_annotation_objects_generator", side_effect=dummy_generator)

        classes = ('person', 'person-fa', 'people', 'person?')
        class_names, class_ids, class_unique_ids = mock_classlabel_class.get_class_labels_ids(classes)

        mock_get_generator.assert_called_once_with()
        assert class_names == ['person', 'person', 'person-fa', 'person-fa', 'people', 'people', 'person?']
        assert class_ids == list(range(7))
        assert class_unique_ids == [0, 0, 1, 1, 2, 2, 3]


class TestImageFilenamesField:
    """Unit tests for the ImageFilenamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_imagefilename_class(field_kwargs):
        return ImageFilenamesField(**field_kwargs)

    def test_process(self, mocker, mock_imagefilename_class):
        dummy_ids = list(range(6))
        dummy_unique_ids = [0, 0, 0, 1, 1, 1]
        dummy_filenames = ['image1.jpg', 'image1.jpg', 'image1.jpg', 'image2.jpg', 'image2.jpg', 'image2.jpg']
        dummy_filenames_unique = ['image1.jpg', 'image2.jpg']
        mock_get_filenames = mocker.patch.object(ImageFilenamesField, "get_image_filenames_from_data", return_value=dummy_filenames_unique)
        mock_get_ids = mocker.patch.object(ImageFilenamesField, "get_image_filenames_obj_ids_from_data", return_value=dummy_unique_ids)
        mock_save_hdf5 = mocker.patch.object(ImageFilenamesField, "save_field_to_hdf5")

        img_ids, img_ids_unique = mock_imagefilename_class.process()

        assert img_ids == dummy_ids
        assert img_ids_unique == dummy_unique_ids
        mock_get_filenames.assert_called_once_with()
        mock_get_ids.assert_called_once_with()
        assert mock_save_hdf5.call_count == 2
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='image_filenames',
        #     data=str2ascii(['image1', 'image2']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_image_filenames_from_data(self, mocker, mock_imagefilename_class):
        image_filenames = mock_imagefilename_class.get_image_filenames_from_data()

        assert image_filenames == ['image1.jpg', 'image2.jpg' ,'image3.jpg', 'image4.jpg', 'image5.jpg']

    def test_get_image_filenames_obj_ids_from_data(self, mocker, mock_imagefilename_class):
        def dummy_generator():
            for i in range(5):
                yield {"image_counter": i}
        mock_get_generator = mocker.patch.object(ImageFilenamesField, "get_annotation_objects_generator", side_effect=dummy_generator)

        ids = mock_imagefilename_class.get_image_filenames_obj_ids_from_data()

        mock_get_generator.assert_called_once_with()
        assert ids == list(range(5))


class TestBoundingBoxBaseField:
    """Unit tests for the BoundingBoxBaseField class."""

    @staticmethod
    @pytest.fixture()
    def mock_bboxbase_class(field_kwargs):
        return BoundingBoxBaseField(**field_kwargs)

    @pytest.mark.parametrize('bbox_type', ['pos', 'posv'])
    def test_get_bboxes_from_data(self, mocker, mock_bboxbase_class, bbox_type):
        def dummy_generator():
            for i in range(5):
                yield {"obj": {"pos": [1, 1, 10, 10], "posv": [1, 1, 1, 1]}, "obj_counter": i}
        mock_get_generator = mocker.patch.object(BoundingBoxBaseField, "get_annotation_objects_generator", side_effect=dummy_generator)
        mock_get_bbox = mocker.patch.object(BoundingBoxBaseField, "get_bbox_by_type", return_value=[1, 1, 1, 1])

        boxes, ids = mock_bboxbase_class.get_bboxes_from_data(bbox_type)

        mock_get_generator.assert_called_once_with()
        assert mock_get_bbox.call_count == 5
        assert boxes == [[1, 1, 1, 1] for i in range(5)]
        assert ids == list(range(5))

    @pytest.mark.parametrize('obj, bbox_type', [
        ({'pos': [1, 1, 10, 10]}, 'pos'),
        ({'posv': [10, 10, 20, 20]}, 'posv'),
        ({'posv': 0}, 'posv'),
    ])
    def test_get_bbox_by_type(self, mocker, mock_bboxbase_class, obj, bbox_type):
        dummy_bbox = [1, 1, 1, 1]
        mock_bbox_correct = mocker.patch.object(BoundingBoxBaseField, "bbox_correct_format", return_value=dummy_bbox)

        bbox = mock_bboxbase_class.get_bbox_by_type(obj, bbox_type)

        if bbox_type == 'pos':
            mock_bbox_correct.assert_called_once_with(obj['pos'])
            assert bbox == dummy_bbox
        else:
            if isinstance(obj['posv'], list):
                mock_bbox_correct.assert_called_once_with(obj['posv'])
                assert bbox == dummy_bbox
            else:
                assert not mock_bbox_correct.called
                assert bbox == [0, 0, 0, 0]

    @pytest.mark.parametrize('bbox, bbox_converted', [
        ([0, 0, 0, 0], [0, 0, -1, -1]),
        ([1, 1, 10, 10], [1, 1, 10, 10]),
        ([10, 10, 10, 10], [10, 10, 19, 19])
    ])
    def test_bbox_correct_format(self, mocker, mock_bboxbase_class, bbox, bbox_converted):
        result_bbox = mock_bboxbase_class.bbox_correct_format(bbox)
        assert result_bbox == bbox_converted


class TestBoundingBoxField:
    """Unit tests for the BoundingBoxField class."""

    @staticmethod
    @pytest.fixture()
    def mock_bbox_class(field_kwargs):
        return BoundingBoxField(**field_kwargs)

    def test_process(self, mocker, mock_bbox_class):
        dummy_boxes = []
        dummy_ids = [0, 0, 1, 1]
        mock_get_bboxes = mocker.patch.object(BoundingBoxField, "get_bboxes_from_data", return_value=(dummy_boxes, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(BoundingBoxField, "save_field_to_hdf5")

        bbox_ids = mock_bbox_class.process()

        assert bbox_ids == dummy_ids
        mock_get_bboxes.assert_called_once_with('pos')
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='bboxes',
        #     data=np.array(dummy_boxes, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )


class TestBoundingBoxvField:
    """Unit tests for the BoundingBoxvField class."""

    @staticmethod
    @pytest.fixture()
    def mock_bboxv_class(field_kwargs):
        return BoundingBoxvField(**field_kwargs)

    def test_process(self, mocker, mock_bboxv_class):
        dummy_boxes = []
        dummy_ids = [0, 0, 1, 1]
        mock_get_bboxesv = mocker.patch.object(BoundingBoxvField, "get_bboxes_from_data", return_value=(dummy_boxes, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(BoundingBoxvField, "save_field_to_hdf5")

        bboxv_ids = mock_bboxv_class.process()

        assert bboxv_ids == dummy_ids
        mock_get_bboxesv.assert_called_once_with('posv')
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='bboxesv',
        #     data=np.array(dummy_boxes, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )


class TestLabelIdField:
    """Unit tests for the LabelIdField class."""

    @staticmethod
    @pytest.fixture()
    def mock_lblid_class(field_kwargs):
        return LabelIdField(**field_kwargs)

    def test_process(self, mocker, mock_lblid_class):
        dummy_labels = []
        dummy_ids = [0, 0, 1, 1]
        mock_get_ids = mocker.patch.object(LabelIdField, "get_label_ids", return_value=(dummy_labels, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(LabelIdField, "save_field_to_hdf5")

        label_ids = mock_lblid_class.process()

        assert label_ids == dummy_ids
        mock_get_ids.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='id',
        #     data=np.array(dummy_labels, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    def test_get_label_ids(self, mocker, mock_lblid_class):
        def dummy_generator():
            for i in range(5):
                yield {"obj": {"id": i}, "obj_counter": i}
        mock_get_generator = mocker.patch.object(LabelIdField, "get_annotation_objects_generator", side_effect=dummy_generator)
        mock_get_id = mocker.patch.object(LabelIdField, "get_id", return_value=10)

        labels, label_ids = mock_lblid_class.get_label_ids()

        assert labels == [10 for i in range(5)]
        mock_get_generator.assert_called_once_with()
        assert label_ids == list(range(5))

    @pytest.mark.parametrize('obj', [{'id': None}, {'id': 1}, {'id': 'val'}])
    def test_get_id(self, mocker, mock_lblid_class, obj):
        result = mock_lblid_class.get_id(obj)

        if isinstance(obj['id'], int):
            assert result == obj['id']
        else:
            assert result == 0


class TestOcclusionField:
    """Unit tests for the OcclusionField class."""

    @staticmethod
    @pytest.fixture()
    def mock_occlusion_class(field_kwargs):
        return OcclusionField(**field_kwargs)

    def test_process(self, mocker, mock_occlusion_class):
        dummy_occlusions = []
        dummy_ids = [0, 0, 1, 1]
        mock_get_ids = mocker.patch.object(OcclusionField, "get_occlusion_ids", return_value=(dummy_occlusions, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(OcclusionField, "save_field_to_hdf5")

        occlusion_ids = mock_occlusion_class.process()

        assert occlusion_ids == dummy_ids
        mock_get_ids.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='occlusion',
        #     data=np.array(dummy_occlusions, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    def test_get_label_ids(self, mocker, mock_occlusion_class):
        def dummy_generator():
            for i in range(5):
                yield {"obj": {"occl": 0}, "obj_counter": i}
        mock_get_generator = mocker.patch.object(OcclusionField, "get_annotation_objects_generator", side_effect=dummy_generator)

        occlusions, occlusion_ids = mock_occlusion_class.get_occlusion_ids()

        assert occlusions == [0 for i in range(5)]
        mock_get_generator.assert_called_once_with()
        assert occlusion_ids == list(range(5))


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
        #     data=str2ascii(['image_filenames', 'classes', 'boxes', 'boxesv', 'id', 'occlusion']),
        #     dtype=np.float8,
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

        image_filenames_ids = [0, 0, 0, 1, 1, 1]
        class_ids = [0, 0, 1, 1, 2, 2]
        bbox_ids = range(6)
        bboxv_ids = range(6)
        label_ids = range(6)
        occlusion_ids = range(6)
        object_ids = mock_objfids_class.process(
            image_filenames_ids=image_filenames_ids,
            class_ids=class_ids,
            bbox_ids=bbox_ids,
            bboxv_ids=bboxv_ids,
            label_ids=label_ids,
            occlusion_ids=occlusion_ids
        )

        expected_ids = [[image_filenames_ids[i], class_ids[i], bbox_ids[i],
                         bboxv_ids[i], label_ids[i], occlusion_ids[i]] for i in range(6)]
        assert object_ids == expected_ids
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # object_ids = [[image_filenames_ids[i], class_ids[i], bbox_ids[i],
        #               bboxv_ids[i], label_ids[i], occlusion_ids[i]]
        #               for i in range(len(bbox_ids))]
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_ids',
        #     data=np.array(object_ids, dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )


class TestImageFilenamesPerClassList:
    """Unit tests for the ImageFilenamesPerClassList class."""

    @staticmethod
    @pytest.fixture()
    def mock_img_per_class_list(field_kwargs):
        return ImageFilenamesPerClassList(**field_kwargs)

    def test_process(self, mocker, mock_img_per_class_list):
        dummy_ids = [[0, 1], [2, 3], [4, 5]]
        mock_get_ids = mocker.patch.object(ImageFilenamesPerClassList, "get_image_filename_ids_per_class", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(ImageFilenamesPerClassList, "save_field_to_hdf5")

        object_ids = [[i, i, i, i] for i in range(6)]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        mock_img_per_class_list.process(object_ids, image_unique_ids)

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_ids',
        #     data=np.array(pad_list(list_image_filenames_per_class, val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_image_filename_ids_per_class(self, mocker, mock_img_per_class_list):
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        class_unique_ids = [0, 0, 1, 1, 2, 2]
        images_per_class_ids = mock_img_per_class_list.get_image_filename_ids_per_class(image_unique_ids, class_unique_ids)

        assert images_per_class_ids == [[0], [1], [2]]


class TestBoundingBoxPerImageList:
    """Unit tests for the BoundingBoxPerImageList class."""

    @staticmethod
    @pytest.fixture()
    def mock_bbox_per_img_list(field_kwargs):
        return BoundingBoxPerImageList(**field_kwargs)

    def test_process(self, mocker, mock_bbox_per_img_list):
        dummy_ids = [[0, 1], [2, 3], [4, 5]]
        mock_get_ids = mocker.patch.object(BoundingBoxPerImageList, "get_bbox_ids_per_image", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(BoundingBoxPerImageList, "save_field_to_hdf5")

        object_ids = [[i, i, i, i] for i in range(6)]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        mock_bbox_per_img_list.process(object_ids, image_unique_ids)

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_boxes_per_image',
        #     data=np.array(pad_list(mock_get_ids, val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_bbox_ids_per_image(self, mocker, mock_bbox_per_img_list):
        object_ids = [
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [2, 1, 2, 2],
            [3, 1, 3, 3],
            [4, 0, 4, 4],
            [5, 2, 5, 5]
        ]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        bboxes_per_image = mock_bbox_per_img_list.get_bbox_ids_per_image(object_ids, image_unique_ids)
        assert bboxes_per_image == [[0, 1], [2, 3], [4, 5]]


class TestBoundingBoxvPerImageList:
    """Unit tests for the BoundingBoxvPerImageList class."""

    @staticmethod
    @pytest.fixture()
    def mock_bboxv_per_img_list(field_kwargs):
        return BoundingBoxvPerImageList(**field_kwargs)

    def test_process(self, mocker, mock_bboxv_per_img_list):
        dummy_ids = [[0, 1], [2, 3], [4, 5]]
        mock_get_ids = mocker.patch.object(BoundingBoxvPerImageList, "get_bboxv_ids_per_image", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(BoundingBoxvPerImageList, "save_field_to_hdf5")

        object_ids = [[i, i, i, i] for i in range(6)]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        mock_bboxv_per_img_list.process(object_ids, image_unique_ids)

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_boxesv_per_image',
        #     data=np.array(pad_list(mock_get_ids, val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_bboxv_ids_per_image(self, mocker, mock_bboxv_per_img_list):
        object_ids = [
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [2, 1, 2, 2],
            [3, 1, 3, 3],
            [4, 0, 4, 4],
            [5, 2, 5, 5]
        ]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        bboxes_per_image = mock_bboxv_per_img_list.get_bboxv_ids_per_image(object_ids, image_unique_ids)
        assert bboxes_per_image == [[0, 1], [2, 3], [4, 5]]


class TestObjectsPerImageList:
    """Unit tests for the ObjectsPerImageList class."""

    @staticmethod
    @pytest.fixture()
    def mock_object_per_img_list(field_kwargs):
        return ObjectsPerImageList(**field_kwargs)

    def test_process(self, mocker, mock_object_per_img_list):
        dummy_ids = [[0, 1], [2, 3], [4, 5]]
        mock_get_ids = mocker.patch.object(ObjectsPerImageList, "get_object_ids_per_image", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(ObjectsPerImageList, "save_field_to_hdf5")

        object_ids = [[i, i, i, i] for i in range(6)]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        mock_object_per_img_list.process(object_ids, image_unique_ids)

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_object_ids_per_image',
        #     data=np.array(pad_list(mock_get_ids, val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_object_ids_per_image(self, mocker, mock_object_per_img_list):
        object_ids = [
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [2, 1, 2, 2],
            [3, 1, 3, 3],
            [4, 0, 4, 4],
            [5, 2, 5, 5]
        ]
        image_unique_ids = [0, 0, 1, 1, 2, 2]
        objects_per_image = mock_object_per_img_list.get_object_ids_per_image(object_ids, image_unique_ids)
        assert objects_per_image == [[0, 1], [2, 3], [4, 5]]


class TestObjectsPerClassList:
    """Unit tests for the ObjectsPerClassList class."""

    @staticmethod
    @pytest.fixture()
    def mock_object_per_class_list(field_kwargs):
        return ObjectsPerClassList(**field_kwargs)

    def test_process(self, mocker, mock_object_per_class_list):
        dummy_ids = [[0, 1], [2, 3], [4, 5]]
        mock_get_ids = mocker.patch.object(ObjectsPerClassList, "get_object_ids_per_class", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(ObjectsPerClassList, "save_field_to_hdf5")

        object_ids = [[i, i, i, i] for i in range(6)]
        class_unique_ids = [0, 0, 1, 1, 2, 2]
        mock_object_per_class_list.process(object_ids, class_unique_ids)

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_objects_ids_per_class',
        #     data=np.array(pad_list(mock_get_ids, val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_object_ids_per_class(self, mocker, mock_object_per_class_list):
        object_ids = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3],
            [4, 4, 4, 4],
            [5, 5, 5, 5]
        ]
        class_unique_ids = [0, 0, 1, 1, 2, 2]
        objects_per_class_ids = mock_object_per_class_list.get_object_ids_per_class(object_ids, class_unique_ids)

        assert objects_per_class_ids == [[0, 1], [2, 3], [4, 5]]
