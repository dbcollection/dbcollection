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


@pytest.fixture()
def mock_detection_class():
    return Detection(data_path='/some/path/data', cache_path='/some/path/cache')


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


    def test_get_sorted_dirs_from_partition(self, mocker, mock_detection_class):
        mock_listdir = mocker.patch('os.listdir', return_value=['dir2', 'dir1', 'dir3'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        dirs = mock_detection_class.get_sorted_dirs_from_partition(path, partition)

        mock_listdir.assert_called_once_with(os.path.join(path, partition))
        assert dirs == ['dir1', 'dir2', 'dir3']

    def test_get_image_filenames_from_dir(self, mocker, mock_detection_class):
        mock_get_data = mocker.patch.object(Detection, 'get_sample_data_from_dir', return_value=['image1.jpg', 'image2.jpg'])

        path = os.path.join('some', 'path', 'to', 'extracted', 'data', 'set')
        partition = 'set00'
        video = 'V000'
        image_filenames = mock_detection_class.get_image_filenames_from_dir(path, partition, video)

        mock_get_data.assert_called_once_with(path, partition, video, 'images')
        assert image_filenames == ['image1.jpg', 'image2.jpg']

    def test_get_sample_data_from_dir(self, mocker, mock_detection_class):
        mock_get_filenames = mocker.patch.object(Detection, 'get_sorted_filenames_from_dir', return_value=['filename1', 'filename2'])
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
