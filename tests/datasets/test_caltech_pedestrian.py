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

from dbcollection.datasets.caltech.caltech_pedestrian import Detection
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


@pytest.fixture()
def mock_detection_class():
    return Detection(data_path='/some/path/data', cache_path='/some/path/cache')


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

    def test_task_attributes(self, mocker, mock_detection_class):
        assert mock_detection_class.filename_h5 == 'detection'
        assert mock_detection_class.skip_step == 30
        assert mock_detection_class.classes == ('person', 'person-fa', 'people', 'person?')
        assert mock_detection_class.sets == {
            "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
            "test": ('set06', 'set07', 'set08', 'set09', 'set10')
        }

    def test_load_data(self, mocker, mock_detection_class):
        mock_load_data = mocker.patch.object(Detection, "load_data_set", return_value=['some_data'])

        load_data_generator = mock_detection_class.load_data()
        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        assert mock_load_data.called
        assert train_data == {"train": ['some_data']}
        assert test_data == {"test": ['some_data']}

    def test_load_data_set(self, mocker, mock_detection_class):
        mock_unpack_data = mocker.patch.object(Detection, "unpack_raw_data_files", return_value='/some/path/data/')
        mock_get_partitions = mocker.patch.object(Detection, "get_set_partitions", return_value=('train', ('set00', 'set01')))
        mock_get_annotations = mocker.patch.object(Detection, "get_annotations_data", return_value=(['image1', 'image2'], ['annot1', 'annot2']))

        set_data = mock_detection_class.load_data_set(False)

        mock_unpack_data.assert_called_once_with()
        mock_get_partitions.assert_called_once_with(is_test=False)
        mock_get_annotations.assert_called_once_with('train', ('set00', 'set01'), '/some/path/data/')
        assert sorted(list(set_data.keys())) == ["annotation_filenames", "image_filenames"]
        assert set_data["image_filenames"] == ['image1', 'image2']
        assert set_data["annotation_filenames"] == ['annot1', 'annot2']

    @pytest.mark.parametrize('is_test', [False, True])
    def test_get_set_partitions(self, mocker, mock_detection_class, is_test):
        set_name, partitions = mock_detection_class.get_set_partitions(is_test=is_test)

        if is_test:
            assert set_name == 'test'
            assert partitions == ('set06', 'set07', 'set08', 'set09', 'set10')
        else:
            assert set_name == 'train'
            assert partitions == ('set00', 'set01', 'set02', 'set03', 'set04', 'set05')

    def test_get_annotations_data(self, mocker, mock_detection_class):
        test_data = {"images": ['image1', 'image2'], "annotations": ['annotation1', 'annotation2']}
        mock_get_annotations = mocker.patch.object(Detection, 'get_annotations_from_partition', return_value=test_data)

        set_name = 'train'
        partitions = ('set00', 'set01')
        unpack_dir = os.path.join('some', 'path', 'to', 'extracted', 'data', 'dir')
        image_filenames, annotation_filenames = mock_detection_class.get_annotations_data(set_name, partitions, unpack_dir)

        assert mock_get_annotations.call_count == 2
        assert image_filenames == {"set00": test_data['images'], "set01": test_data['images']}
        assert annotation_filenames == {"set00": test_data['annotations'], "set01": test_data['annotations']}

    def test_get_annotations_from_partition(self, mocker, mock_detection_class):
        mock_get_dirs = mocker.patch.object(Detection, 'get_sorted_object_names_from_dir', return_value=('V000', 'V001'))
        mock_get_image_fnames = mocker.patch.object(Detection, 'get_image_filenames_from_dir', return_value=['image1.jpg', 'image2.jpg'])
        mock_get_annotation_fnames = mocker.patch.object(Detection, 'get_annotation_filenames_from_dir', return_value=['annotation1.json', 'annotation2.json'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        partition_annotations = mock_detection_class.get_annotations_from_partition(path, partition)

        mock_get_dirs.assert_called_once_with(os.path.join(path, partition))
        assert mock_get_image_fnames.call_count  == 2
        assert mock_get_annotation_fnames.call_count  == 2
        assert partition_annotations == {
            "V000": {"images":  ['image1.jpg', 'image2.jpg'], "annotations": ['annotation1.json', 'annotation2.json']},
            "V001": {"images":  ['image1.jpg', 'image2.jpg'], "annotations": ['annotation1.json', 'annotation2.json']}
        }

    def test_get_sorted_object_names_from_dir(self, mocker, mock_detection_class):
        mock_listdir = mocker.patch('os.listdir', return_value=['dir2', 'dir1', 'dir3'])

        path = os.path.join('some', 'path', 'to', 'dir')
        object_names = mock_detection_class.get_sorted_object_names_from_dir(path)

        mock_listdir.assert_called_once_with(path)
        assert object_names == ['dir1', 'dir2', 'dir3']

    def test_get_image_filenames_from_dir(self, mocker, mock_detection_class):
        mock_get_data = mocker.patch.object(Detection, 'get_sample_data_from_dir', return_value=['image1.jpg', 'image2.jpg'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        image_filenames = mock_detection_class.get_image_filenames_from_dir(path, partition, video)

        mock_get_data.assert_called_once_with(path, partition, video, 'images')
        assert image_filenames == ['image1.jpg', 'image2.jpg']

    def test_get_sample_data_from_dir(self, mocker, mock_detection_class):
        mock_get_filenames = mocker.patch.object(Detection, 'get_sorted_object_names_from_dir', return_value=['filename1', 'filename2'])
        mock_get_sample = mocker.patch.object(Detection, 'get_sample_filenames', return_value=['filename1', 'filename2'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        type_data = 'images'
        sample_filepaths = mock_detection_class.get_sample_data_from_dir(path, partition, video, type_data)

        annot_path = os.path.join(mock_detection_class.data_path, 'extracted_data', partition, video, type_data)
        filepaths = [os.path.join(annot_path, filename) for filename in ['filename1', 'filename2']]
        mock_get_filenames.assert_called_once_with(os.path.join(path, partition, video, type_data))
        mock_get_sample.assert_called_once_with(filepaths, mock_detection_class.skip_step)
        assert sample_filepaths == ['filename1', 'filename2']

    def test_get_sample_filenames(self, mocker, mock_detection_class):
        filenames = ['filename1', 'filename2', 'filename3', 'filename4', 'filename5']
        skip_step = 2

        sample = mock_detection_class.get_sample_filenames(filenames, skip_step)

        assert sample == ['filename2', 'filename4']

    def test_get_annotation_filenames_from_dir(self, mocker, mock_detection_class):
        mock_get_data = mocker.patch.object(Detection, 'get_sample_data_from_dir', return_value=['annotation1.json', 'annotation2.json'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        annotation_filenames = mock_detection_class.get_annotation_filenames_from_dir(path, partition, video)

        mock_get_data.assert_called_once_with(path, partition, video, 'annotations')
        assert annotation_filenames == ['annotation1.json', 'annotation2.json']

    def test_process_set_metadata(self, mocker, mock_detection_class, test_data):
        mock_image_filenames = mocker.patch.object(Detection, "process_image_filenames", return_value=[0, 0, 0, 1, 1, 1])
        mock_bbox_metadata = mocker.patch.object(Detection, "process_bboxes_metadata", return_value=[0, 0, 0, 1, 1, 1])
        mock_bboxv_metadata = mocker.patch.object(Detection, "process_bboxesv_metadata", return_value=[0, 0, 0, 1, 1, 1])
        mock_object_fields = mocker.patch.object(Detection, "process_object_fields")

        set_name = 'train'
        mock_detection_class.process_set_metadata(test_data, set_name)

        mock_image_filenames.assert_called_once_with(test_data, set_name)
        mock_bbox_metadata.assert_called_once_with(test_data, set_name)
        mock_bboxv_metadata.assert_called_once_with(test_data, set_name)
        mock_object_fields.assert_called_once_with(set_name)

    def test_process_image_filenames(self, mocker, mock_detection_class, test_data):
        mock_get_filenames = mocker.patch.object(Detection, "get_image_filenames_from_data", return_value=['image1.jpg', 'image2.jpg'])
        mock_get_ids = mocker.patch.object(Detection, "get_image_filenames_obj_ids_from_data", return_value=[0, 0, 1, 1])
        mock_save_hdf5 = mocker.patch.object(Detection, "save_field_to_hdf5")

        img_ids = mock_detection_class.process_image_filenames(test_data, 'train')

        assert img_ids == [0, 0, 1, 1]
        mock_get_filenames.assert_called_once_with(test_data)
        mock_get_ids.assert_called_once_with(test_data)
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='image_filenames',
        #     data=str2ascii(['image1', 'image2']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_image_filenames_from_data(self, mocker, mock_detection_class, test_data):
        image_filenames = mock_detection_class.get_image_filenames_from_data(test_data)

        assert image_filenames == ['image1.jpg', 'image2.jpg' ,'image3.jpg', 'image4.jpg',
                                   'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg']

    @pytest.mark.parametrize('is_clean', [False, True])
    def test_get_image_filenames_obj_ids_from_data(self, mocker, mock_detection_class, test_data, is_clean):
        mock_load_file = mocker.patch.object(Detection, "load_annotation_file", return_value=[{"pos": [0, 0, 0, 0]}, {"pos": [1, 1, 30, 30]}])

        mock_detection_class.is_clean = is_clean
        ids = mock_detection_class.get_image_filenames_obj_ids_from_data(test_data)

        assert mock_load_file.call_count == 8
        if is_clean:
            assert ids == [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            assert ids == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]

    def test_process_bboxes_metadata(self, mocker, mock_detection_class, test_data):
        bboxes = [[1, 1, 10, 10], [1, 1, 20, 20], [1, 1, 30, 30], [1, 1, 40, 40]]
        bboxes_ids = [0, 1, 2, 3]
        mock_get_bboxes = mocker.patch.object(Detection, "get_bboxes_from_data", return_value=[bboxes, bboxes_ids])
        mock_save_hdf5 = mocker.patch.object(Detection, "save_field_to_hdf5")

        bb_ids = mock_detection_class.process_bboxes_metadata(test_data, 'train')

        assert bb_ids == bboxes_ids
        mock_get_bboxes.assert_called_once_with(test_data, bbox_type='pos')
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='bboxes',
        #     data=np.array(bboxes, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    @pytest.mark.parametrize('is_clean', [False, True])
    def test_get_bboxes_from_data(self, mocker, mock_detection_class, test_data, is_clean):
        mock_load_file = mocker.patch.object(Detection, "load_annotation_file", return_value=[{"pos": [0, 0, 0, 0]}, {"pos": [1, 1, 30, 30]}])
        mock_get_bbox = mocker.patch.object(Detection, "get_bbox_by_type", return_value=[1, 1, 1, 1])

        mock_detection_class.is_clean = is_clean
        bbox, bbox_ids = mock_detection_class.get_bboxes_from_data(test_data, bbox_type='pos')

        assert mock_load_file.call_count == 8
        assert mock_get_bbox.called
        if is_clean:
            assert bbox == [[1, 1, 1, 1]] * 8
            assert bbox_ids == [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            assert bbox == [[1, 1, 1, 1]] * 8 * 2
            assert bbox_ids == list(range(16))

    @pytest.mark.parametrize('obj, bbox_type', [
        ({'pos': [1, 1, 10, 10]}, 'pos'),
        ({'posv': [10, 10, 20, 20]}, 'posv'),
        ({'posv': 0}, 'posv'),
    ])
    def test_get_bbox_by_type(self, mocker, mock_detection_class, obj, bbox_type):
        dummy_bbox = [1, 1, 1, 1]
        mock_bbox_correct = mocker.patch.object(Detection, "bbox_correct_format", return_value=dummy_bbox)

        bbox = mock_detection_class.get_bbox_by_type(obj, bbox_type)

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
    def test_bbox_correct_format(self, mocker, mock_detection_class, bbox, bbox_converted):
        result_bbox = mock_detection_class.bbox_correct_format(bbox)

        assert result_bbox == bbox_converted

    def test_process_bboxesv_metadata(self, mocker, mock_detection_class, test_data):
        bboxes = [[1, 1, 10, 10], [1, 1, 20, 20], [1, 1, 30, 30], [1, 1, 40, 40]]
        bboxesv_ids = [0, 1, 2, 3]
        mock_get_bboxes = mocker.patch.object(Detection, "get_bboxes_from_data", return_value=[bboxes, bboxesv_ids])
        mock_save_hdf5 = mocker.patch.object(Detection, "save_field_to_hdf5")

        bb_ids = mock_detection_class.process_bboxesv_metadata(test_data, 'train')

        assert bb_ids == bboxesv_ids
        mock_get_bboxes.assert_called_once_with(test_data, bbox_type='posv')
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='bboxesv',
        #     data=np.array(bboxes, dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )


    def test_process_object_fields(self, mocker, mock_detection_class):
        mock_save_hdf5 = mocker.patch.object(Detection, "save_field_to_hdf5")

        mock_detection_class.process_object_fields('train')

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_fields',
        #     data=str2ascii(['image_filenames', 'classes', 'boxes', 'boxesv', 'id', 'occlusion']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

