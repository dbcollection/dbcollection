"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.datasets.mpii_pose.keypoints import Keypoints, DatasetAnnotationLoader


class TestKeypointsTask:
    """Unit tests for the mpii Keypoints task."""

    @staticmethod
    @pytest.fixture()
    def mock_keypoints_class():
        return Keypoints(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_keypoints_class):
        assert mock_keypoints_class.filename_h5 == 'keypoint'
        assert mock_keypoints_class.is_full == False
        assert mock_keypoints_class.keypoints_labels == [
            'right ankle',  # -- 1
            'right knee',  # -- 2
            'right hip',  # -- 3
            'left hip',  # -- 4
            'left knee',  # -- 5
            'left ankle',  # -- 6
            'pelvis',  # -- 7
            'thorax',  # -- 8
            'upper neck',  # -- 9
            'head top',  # -- 10
            'right wrist',  # -- 11
            'right elbow',  # -- 12
            'right shoulder',  # -- 13
            'left shoulder',  # -- 14
            'left elbow',  # -- 15
            'left wrist'  # -- 16
        ]


class TestDatasetAnnotationLoader:
    """Unit tests for DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            keypoints_labels=[
                'right ankle',
                'right knee',
                'right hip',
                'left hip',
                'left knee',
                'left ankle',
                'pelvis',
                'thorax',
                'upper neck',
                'head top',
                'right wrist',
                'right elbow',
                'right shoulder',
                'left shoulder',
                'left elbow',
                'left wrist'
            ],
            is_full=False,
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.keypoints_labels == [
            'right ankle',
            'right knee',
            'right hip',
            'left hip',
            'left knee',
            'left ankle',
            'pelvis',
            'thorax',
            'upper neck',
            'head top',
            'right wrist',
            'right elbow',
            'right shoulder',
            'left shoulder',
            'left elbow',
            'left wrist'
        ]
        assert mock_loader_class.is_full == False
        assert mock_loader_class.data_path=='/some/path/data'
        assert mock_loader_class.cache_path=='/some/path/cache'
        assert mock_loader_class.verbose==True

    def test_load_trainval_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)

        annotations = mock_loader_class.load_trainval_data()

        assert annotations == dummy_data
        mock_load_annotations.assert_called_once_with(is_test=False)

    def test_load_train_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        dummy_data_filtered = {"dummy": 'filtered'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)
        mock_filter_annotations = mocker.patch.object(DatasetAnnotationLoader, "filter_annotations_by_ids", return_value=dummy_data_filtered)

        annotations = mock_loader_class.load_train_data()

        from dbcollection.datasets.mpii_pose.train_val_ids import train_images_ids
        assert annotations == dummy_data_filtered
        mock_load_annotations.assert_called_once_with(is_test=False)
        mock_filter_annotations.assert_called_once_with(dummy_data, train_images_ids)

    def test_load_val_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        dummy_data_filtered = {"dummy": 'filtered'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)
        mock_filter_annotations = mocker.patch.object(DatasetAnnotationLoader, "filter_annotations_by_ids", return_value=dummy_data_filtered)

        annotations = mock_loader_class.load_val_data()

        from dbcollection.datasets.mpii_pose.train_val_ids import val_images_ids
        assert annotations == dummy_data_filtered
        mock_load_annotations.assert_called_once_with(is_test=False)
        mock_filter_annotations.assert_called_once_with(dummy_data, val_images_ids)

    def test_load_test_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)

        annotations = mock_loader_class.load_test_data()

        assert annotations == dummy_data
        mock_load_annotations.assert_called_once_with(is_test=True)

    def test_load_annotations_set(self, mocker, mock_loader_class):
        dummy_annotations = {"dummy": 'data'}
        dummy_nfiles = 10
        dummy_filenames = ['filename1', 'filename2', 'filename2', 'filename3', 'filename3']
        dummy_framesec = [141,20,13,74,6]
        dummy_videos = [6,20,1,1, 4]
        dummy_poses = [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
        dummy_activities = [0, 1, 0, 2, 3]
        dummy_single = [1,1,1,0,1]
        dummy_video_names = ['video1', 'video2', 'video3']
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_data_from_disk", return_value=dummy_annotations)
        mock_get_total_files = mocker.patch.object(DatasetAnnotationLoader, "get_num_files", return_value=dummy_nfiles)
        mock_get_filenames = mocker.patch.object(DatasetAnnotationLoader, "get_image_filenames", return_value=dummy_filenames)
        mock_get_frame_sec = mocker.patch.object(DatasetAnnotationLoader, "get_frame_sec", return_value=dummy_framesec)
        mock_get_video_idx = mocker.patch.object(DatasetAnnotationLoader, "get_video_indexes", return_value=dummy_videos)
        mock_get_pose = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotations", return_value=dummy_poses)
        mock_get_activity = mocker.patch.object(DatasetAnnotationLoader, "get_activities", return_value=dummy_activities)
        mock_get_single = mocker.patch.object(DatasetAnnotationLoader, "get_single_persons", return_value=dummy_single)
        mock_get_video_names = mocker.patch.object(DatasetAnnotationLoader, "get_video_names", return_value=dummy_video_names)

        annotations = mock_loader_class.load_annotations_set(is_test=True)

        mock_load_annotations.assert_called_once_with()
        mock_get_total_files.assert_called_once_with(dummy_annotations)
        mock_get_filenames.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_frame_sec.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_video_idx.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_pose.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_activity.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_single.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_video_names.assert_called_once_with(dummy_annotations)
        assert annotations == {
            "image_filenames": dummy_filenames,
            "frame_sec": dummy_framesec,
            "video_idx": dummy_videos,
            "pose_annotations": dummy_poses,
            "activity": dummy_activities,
            "single_person": dummy_single,
            "video_names": dummy_video_names
        }

    def test_load_annotation_data_from_disk(self, mocker, mock_loader_class):
        dummy_annotations = {"dummy": 'data'}
        mock_load_file = mocker.patch.object(DatasetAnnotationLoader, "load_file", return_value=dummy_annotations)

        annotations = mock_loader_class.load_annotation_data_from_disk()

        filename = os.path.join(mock_loader_class.data_path, 'mpii_human_pose_v1_u12_2', 'mpii_human_pose_v1_u12_1.mat')
        mock_load_file.assert_called_once_with(filename)
        assert annotations == dummy_annotations

    def test_get_num_files(self, mocker, mock_loader_class):
        annotations = {"RELEASE": [[[[], [], [], list(range(10))]]]}
        num_files = mock_loader_class.get_num_files(annotations)

        assert num_files == 10

    def test_get_image_filenames__only_one_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_filename = mocker.patch.object(DatasetAnnotationLoader, "get_filename_from_annotation_id", return_value='filename1')

        annotations = {"RELEASE": []}
        num_files = 1
        image_filenames = mock_loader_class.get_image_filenames(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_filename.assert_called_once_with(annotations, 0)
        assert image_filenames == [os.path.join('images', 'filename1')]

    def test_get_image_filenames__multiple_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_filename = mocker.patch.object(DatasetAnnotationLoader, "get_filename_from_annotation_id", return_value='filename1')

        annotations = {"RELEASE": []}
        num_files = 10
        image_filenames = mock_loader_class.get_image_filenames(annotations, num_files, True)

        assert mock_is_test.call_count == 10
        assert mock_get_filename.call_count == 10
        assert image_filenames == [os.path.join('images', 'filename1')]*10

    def test_get_image_filenames__returns_empty_list(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=False)
        mock_get_filename = mocker.patch.object(DatasetAnnotationLoader, "get_filename_from_annotation_id", return_value='filename1')

        annotations = {"RELEASE": []}
        num_files = 1
        image_filenames = mock_loader_class.get_image_filenames(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        assert not mock_get_filename.called
        assert image_filenames == []

    def test_is_test_annotation__returns_true(self, mocker, mock_loader_class):
        result = mock_loader_class.is_test_annotation({"RELEASE": [[['', [[0, 0, 1]]]]]}, 1)

        assert result == True

    def test_is_test_annotation__returns_false(self, mocker, mock_loader_class):
        result = mock_loader_class.is_test_annotation({"RELEASE": [[['', [[0, 0, 1]]]]]}, 2)

        assert result == False

    def test_get_filename_from_annotation_id(self, mocker, mock_loader_class):
        filename = mock_loader_class.get_filename_from_annotation_id({"RELEASE": [[[[[0, [[[[['filename1']]]]]]]]]]}, 1)

        assert filename == 'filename1'

    def test_get_frame_sec__only_one_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_frame = mocker.patch.object(DatasetAnnotationLoader, "get_frame_sec_from_annotation_id", return_value=0)

        annotations = {"RELEASE": []}
        num_files = 1
        frame_sec = mock_loader_class.get_frame_sec(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_frame.assert_called_once_with(annotations, 0)
        assert frame_sec == [0]

    def test_get_frame_sec__multiple_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_frame = mocker.patch.object(DatasetAnnotationLoader, "get_frame_sec_from_annotation_id", return_value=0)

        annotations = {"RELEASE": []}
        num_files = 10
        frame_sec = mock_loader_class.get_frame_sec(annotations, num_files, True)

        assert mock_is_test.call_count == 10
        assert mock_get_frame.call_count == 10
        assert frame_sec == [0]*10

    def test_get_frame_sec__returns_empty_list(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=False)
        mock_get_frame = mocker.patch.object(DatasetAnnotationLoader, "get_frame_sec_from_annotation_id", return_value=0)

        annotations = {"RELEASE": []}
        num_files = 1
        frame_sec = mock_loader_class.get_frame_sec(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        assert not mock_get_frame.called
        assert frame_sec == []

    def test_get_frame_sec_from_annotation_id(self, mocker, mock_loader_class):
        frame_sec = mock_loader_class.get_frame_sec_from_annotation_id(
            annotations={"RELEASE": [[[[[[], [[], [], [[100]], [[1]]]]]]]]},
            ifile=1
        )

        assert frame_sec == 100

    def test_get_frame_sec_from_annotation_id__empty_frame_sec(self, mocker, mock_loader_class):
        frame_sec = mock_loader_class.get_frame_sec_from_annotation_id(
            annotations={"RELEASE": [[[[[[], [[], [], [[100]], [[]]]]]]]]},
            ifile=1
        )

        assert frame_sec == -1

    def test_get_video_indexes__only_one_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_video = mocker.patch.object(DatasetAnnotationLoader, "get_video_idx_from_annotation_id", return_value=15)

        annotations = {"RELEASE": []}
        num_files = 1
        frame_sec = mock_loader_class.get_video_indexes(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_video.assert_called_once_with(annotations, 0)
        assert frame_sec == [15]

    def test_get_video_indexes__multiple_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_video = mocker.patch.object(DatasetAnnotationLoader, "get_video_idx_from_annotation_id", return_value=15)

        annotations = {"RELEASE": []}
        num_files = 10
        frame_sec = mock_loader_class.get_video_indexes(annotations, num_files, True)

        assert mock_is_test.call_count == 10
        assert mock_get_video.call_count == 10
        assert frame_sec == [15]*10

    def test_get_video_indexes__returns_empty_list(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=False)
        mock_get_video = mocker.patch.object(DatasetAnnotationLoader, "get_video_idx_from_annotation_id", return_value=15)

        annotations = {"RELEASE": []}
        num_files = 1
        frame_sec = mock_loader_class.get_video_indexes(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        assert not mock_get_video.called
        assert frame_sec == []

    def test_get_video_idx_from_annotation_id(self, mocker, mock_loader_class):
        video_idx = mock_loader_class.get_video_idx_from_annotation_id(
            annotations={"RELEASE": [[[[[[], [[], [], [], [[200]]]]]]]]},
            ifile=1
        )

        assert video_idx == 200

    def test_get_video_idx_from_annotation_id__empty_video(self, mocker, mock_loader_class):
        video_idx = mock_loader_class.get_video_idx_from_annotation_id(
            annotations={"RELEASE": [[[[[[], [[], [], [], [[]]]]]]]]},
            ifile=1
        )

        assert video_idx == -1
