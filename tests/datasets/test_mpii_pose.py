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

    def test_load_data(self, mocker, mock_keypoints_class):
        mock_load_trainval = mocker.patch.object(DatasetAnnotationLoader, "load_trainval_data", return_value=['trainval_data'])
        mock_load_train = mocker.patch.object(DatasetAnnotationLoader, "load_train_data", return_value=['train_data'])
        mock_load_val = mocker.patch.object(DatasetAnnotationLoader, "load_val_data", return_value=['val_data'])
        mock_load_test = mocker.patch.object(DatasetAnnotationLoader, "load_test_data", return_value=['test_data'])

        load_data_generator = mock_keypoints_class.load_data()

        if sys.version[0] == '3':
            trainval_data = load_data_generator.__next__()
            train_data = load_data_generator.__next__()
            val_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            trainval_data = load_data_generator.next()
            train_data = load_data_generator.next()
            val_data = load_data_generator.next()
            test_data = load_data_generator.next()

        mock_load_trainval.assert_called_once_with()
        mock_load_train.assert_called_once_with()
        mock_load_val.assert_called_once_with()
        mock_load_test.assert_called_once_with()
        assert trainval_data == {"trainval": ['trainval_data']}
        assert train_data == {"train": ['train_data']}
        assert val_data == {"val": ['val_data']}
        assert test_data == {"test": ['test_data']}



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
        mock_get_single.assert_called_once_with(dummy_annotations, dummy_nfiles)
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
        dummy_annotations_list = ['dummy', 'values']
        mock_get_annotations_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=dummy_annotations_list)

        annotations = {"RELEASE": [[[[[[], [[], [], [[100]], [[1]]]]]]]]}
        ifile = 1
        frame_sec = mock_loader_class.get_frame_sec_from_annotation_id(annotations, ifile)

        mock_get_annotations_list.assert_called_once_with(annotations, ifile)
        assert frame_sec == 100

    def test_get_frame_sec_from_annotation_id__empty_frame_sec(self, mocker, mock_loader_class):
        mock_get_annotations_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])

        annotations = {"RELEASE": [[[[[[], [[], [], [[100]], [[]]]]]]]]}
        ifile = 1
        frame_sec = mock_loader_class.get_frame_sec_from_annotation_id(annotations, ifile)

        mock_get_annotations_list.assert_called_once_with(annotations, ifile)
        assert frame_sec == -1

    def test_get_annotations_list_by_image_id(self, mocker, mock_loader_class):
        annotations_list = mock_loader_class.get_annotations_list_by_image_id(
            annotations={"RELEASE": [[[[[[], [[], [], [], [[1, 2, 3, 4, 5]]]]]]]]},
            ifile=1
        )

        assert annotations_list == [1, 2, 3, 4, 5]

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
        mock_get_annotations_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[200])

        annotations = {"RELEASE": [[[[[[], [[], [], [], [[200]]]]]]]]},
        ifile = 1
        video_idx = mock_loader_class.get_video_idx_from_annotation_id(annotations, ifile)

        mock_get_annotations_list.assert_called_once_with(annotations, ifile)
        assert video_idx == 200

    def test_get_video_idx_from_annotation_id__empty_video(self, mocker, mock_loader_class):
        mock_get_annotations_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])

        annotations = {"RELEASE": [[[[[[], [[], [], [], [[]]]]]]]]}
        ifile = 1
        video_idx = mock_loader_class.get_video_idx_from_annotation_id(annotations, ifile)

        mock_get_annotations_list.assert_called_once_with(annotations, ifile)
        assert video_idx == -1

    def test_get_pose_annotations__only_one_file(self, mocker, mock_loader_class):
        dummy_poses = [{
            "keypoints": [[1, 1, 1]]*16,
            "head_bbox": (1,1, 10, 20),
            "scale": 2.0,
            "objpos": (20, 30)
        }]
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_poses = mocker.patch.object(DatasetAnnotationLoader, "get_poses_from_annotation_id", return_value=dummy_poses)

        annotations = {"RELEASE": []}
        num_files = 1
        poses_annotations = mock_loader_class.get_pose_annotations(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_poses.assert_called_once_with(annotations, 0, True)
        assert poses_annotations == [dummy_poses]

    def test_get_pose_annotations__multiple_file(self, mocker, mock_loader_class):
        dummy_poses = [{
            "keypoints": [[1, 1, 1]]*16,
            "head_bbox": (1,1, 10, 20),
            "scale": 2.0,
            "objpos": (20, 30)
        }]
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_poses = mocker.patch.object(DatasetAnnotationLoader, "get_poses_from_annotation_id", return_value=dummy_poses)

        annotations = {"RELEASE": []}
        num_files = 10
        poses_annotations = mock_loader_class.get_pose_annotations(annotations, num_files, True)

        assert mock_is_test.call_count == 10
        assert mock_get_poses.call_count == 10
        assert poses_annotations == [dummy_poses]*10

    def test_get_pose_annotations__returns_empty_list(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_poses = mocker.patch.object(DatasetAnnotationLoader, "get_poses_from_annotation_id", return_value=[])

        annotations = {"RELEASE": []}
        num_files = 1
        poses_annotations = mock_loader_class.get_pose_annotations(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_poses.assert_called_once_with(annotations, 0, True)
        assert poses_annotations == []

    def test_get_poses_from_annotation_id__returns_empty_list(self, mocker, mock_loader_class):
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotation_names", return_value=[])
        mock_get_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])
        mock_get_poses_full = mocker.patch.object(DatasetAnnotationLoader, "get_full_pose_annotations", return_value=[])
        mock_get_poses_partial = mocker.patch.object(DatasetAnnotationLoader, "get_partial_poses_annotations", return_value=[])

        annotations = {"RELEASE": []}
        ifile = 1
        poses = mock_loader_class.get_poses_from_annotation_id(annotations, ifile, True)

        mock_get_names.assert_called_once_with(annotations, ifile)
        assert not mock_get_list.called
        assert not mock_get_poses_full.called
        assert not mock_get_poses_partial.called
        assert poses == []

    def test_get_poses_from_annotation_id__returns_full_poses(self, mocker, mock_loader_class):
        dummy_pnames = {"dummy": 'data'}
        dummy_poses = [{"pose1": 'data'}, {"pose2": 'data'}]
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotation_names", return_value=dummy_pnames)
        mock_get_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=['dummy', 'values'])
        mock_get_poses_full = mocker.patch.object(DatasetAnnotationLoader, "get_full_pose_annotations", return_value=dummy_poses)
        mock_get_poses_partial = mocker.patch.object(DatasetAnnotationLoader, "get_partial_poses_annotations", return_value=[])

        annotations = {"RELEASE": []}
        ifile = 1
        poses = mock_loader_class.get_poses_from_annotation_id(annotations, ifile, True)

        mock_get_names.assert_called_once_with(annotations, ifile)
        mock_get_list.assert_called_once_with(annotations, ifile)
        mock_get_poses_full.assert_called_once_with(annotations, ifile, dummy_pnames)
        assert not mock_get_poses_partial.called
        assert poses == dummy_poses

    def test_get_poses_from_annotation_id__returns_partial_poses(self, mocker, mock_loader_class):
        dummy_pnames = {"dummy": 'data'}
        dummy_poses = [{"pose1": 'data'}, {"pose2": 'data'}]
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotation_names", return_value=dummy_pnames)
        mock_get_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])
        mock_get_poses_full = mocker.patch.object(DatasetAnnotationLoader, "get_full_pose_annotations", return_value=[])
        mock_get_poses_partial = mocker.patch.object(DatasetAnnotationLoader, "get_partial_poses_annotations", return_value=dummy_poses)

        annotations = {"RELEASE": []}
        ifile = 1
        poses = mock_loader_class.get_poses_from_annotation_id(annotations, ifile, True)

        mock_get_names.assert_called_once_with(annotations, ifile)
        mock_get_list.assert_called_once_with(annotations, ifile)
        assert not mock_get_poses_full.called
        mock_get_poses_partial.assert_called_once_with(annotations, ifile, dummy_pnames)
        assert poses == dummy_poses

    def test_get_poses_from_annotation_id__returns_partial_poses_for_full_task(self, mocker, mock_loader_class):
        dummy_pnames = {"dummy": 'data'}
        dummy_poses = [{"pose1": 'data'}, {"pose2": 'data'}]
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotation_names", return_value=dummy_pnames)
        mock_get_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])
        mock_get_poses_full = mocker.patch.object(DatasetAnnotationLoader, "get_full_pose_annotations", return_value=[])
        mock_get_poses_partial = mocker.patch.object(DatasetAnnotationLoader, "get_partial_poses_annotations", return_value=dummy_poses)

        annotations = {"RELEASE": []}
        ifile = 1
        mock_loader_class.is_full = True
        poses = mock_loader_class.get_poses_from_annotation_id(annotations, ifile, False)

        mock_get_names.assert_called_once_with(annotations, ifile)
        mock_get_list.assert_called_once_with(annotations, ifile)
        assert not mock_get_poses_full.called
        mock_get_poses_partial.assert_called_once_with(annotations, ifile, dummy_pnames)
        assert poses == dummy_poses

    def test_get_poses_from_annotation_id__returns_empty_list_for_train_set(self, mocker, mock_loader_class):
        dummy_pnames = {"dummy": 'data'}
        mock_get_names = mocker.patch.object(DatasetAnnotationLoader, "get_pose_annotation_names", return_value=dummy_pnames)
        mock_get_list = mocker.patch.object(DatasetAnnotationLoader, "get_annotations_list_by_image_id", return_value=[])
        mock_get_poses_full = mocker.patch.object(DatasetAnnotationLoader, "get_full_pose_annotations", return_value=[])
        mock_get_poses_partial = mocker.patch.object(DatasetAnnotationLoader, "get_partial_poses_annotations", return_value=[])

        annotations = {"RELEASE": []}
        ifile = 1
        poses = mock_loader_class.get_poses_from_annotation_id(annotations, ifile, False)

        mock_get_names.assert_called_once_with(annotations, ifile)
        mock_get_list.assert_called_once_with(annotations, ifile)
        assert not mock_get_poses_full.called
        assert not mock_get_poses_partial.called
        assert poses == []

    def test_get_pose_annotation_names__try_branch(self, mocker, mock_loader_class):
        dummy_names = ['name1', 'name2', 'name3']
        dummy_annot = mocker.MagicMock()
        dummy_annot.dtype = mocker.MagicMock()
        dummy_annot.dtype.names = dummy_names
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annot)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = mock_loader_class.get_pose_annotation_names(annotations, ifile)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert pnames == dummy_names

    def test_get_pose_annotation_names__except_branch(self, mocker, mock_loader_class):
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", side_effect=IndexError('raise exception'))

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = mock_loader_class.get_pose_annotation_names(annotations, ifile)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert pnames == []

    def test_get_annotation_by_file_id(self, mocker, mock_loader_class):
        dummy_annotations = ["dummy", "data"]
        annot_ptr = mock_loader_class.get_annotation_by_file_id(
            annotations = {"RELEASE": [[[[[0, [0, [dummy_annotations]]]]]]]},# [[[[], [[], [dummy_annotations]]]]]},
            ifile = 1
        )

        assert annot_ptr == dummy_annotations

    def test_get_full_pose_annotations__empty_list(self, mocker, mock_loader_class):
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=[])
        mock_get_keypoints = mocker.patch.object(DatasetAnnotationLoader, "get_keypoints")
        mock_get_head_bbox = mocker.patch.object(DatasetAnnotationLoader, "get_head_coordinates")
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale")
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates")

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_full_pose_annotations(annotations, ifile, pnames)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert not mock_get_keypoints.called
        assert not mock_get_head_bbox.called
        assert not mock_get_scale.called
        assert not mock_get_objpos.called
        assert poses_annotations == []

    def test_get_full_pose_annotations__single_annotation(self, mocker, mock_loader_class):
        dummy_annotation = [0]
        dummy_keypoints = [[0, 0, 0]] * 16
        dummy_head_bbox = [1,1, 50, 50]
        dummy_scale = [3.10]
        dummy_objpos = {"x": 10.0, "y": 10.0}
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annotation)
        mock_get_keypoints = mocker.patch.object(DatasetAnnotationLoader, "get_keypoints", return_value=dummy_keypoints)
        mock_get_head_bbox = mocker.patch.object(DatasetAnnotationLoader, "get_head_coordinates", return_value=dummy_head_bbox)
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale", return_value=dummy_scale)
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates", return_value=dummy_objpos)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_full_pose_annotations(annotations, ifile, pnames)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        mock_get_keypoints.assert_called_once_with(dummy_annotation, 0)
        mock_get_head_bbox.assert_called_once_with(dummy_annotation, 0, pnames)
        mock_get_scale.assert_called_once_with(dummy_annotation, 0, pnames)
        mock_get_objpos.assert_called_once_with(dummy_annotation, 0, pnames)
        assert poses_annotations == [{
            "keypoints": dummy_keypoints,
            "head_bbox": dummy_head_bbox,
            "scale": dummy_scale,
            "objpos": dummy_objpos
        }]

    def test_get_full_pose_annotations__multiple_annotations(self, mocker, mock_loader_class):
        dummy_annotation = [['dummy_annot']]*5
        dummy_keypoints = [[0, 0, 0]] * 16
        dummy_head_bbox = [1,1, 50, 50]
        dummy_scale = [3.10]
        dummy_objpos = {"x": 10.0, "y": 10.0}
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annotation)
        mock_get_keypoints = mocker.patch.object(DatasetAnnotationLoader, "get_keypoints", return_value=dummy_keypoints)
        mock_get_head_bbox = mocker.patch.object(DatasetAnnotationLoader, "get_head_coordinates", return_value=dummy_head_bbox)
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale", return_value=dummy_scale)
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates", return_value=dummy_objpos)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_full_pose_annotations(annotations, ifile, pnames)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert mock_get_keypoints.call_count == 5
        assert mock_get_head_bbox.call_count == 5
        assert mock_get_scale.call_count == 5
        assert mock_get_objpos.call_count == 5
        assert poses_annotations == [{
            "keypoints": dummy_keypoints,
            "head_bbox": dummy_head_bbox,
            "scale": dummy_scale,
            "objpos": dummy_objpos
        }]*5

    def test_get_keypoints__returns_default_value(self, mocker, mock_loader_class):
        mock_get_keypoints = mocker.patch.object(DatasetAnnotationLoader, "get_keypoint_annotations", return_value=[])

        annotations_file = {"dummy": 'data'}
        ipose = 1
        keypoints = mock_loader_class.get_keypoints(annotations_file, ipose)

        mock_get_keypoints.assert_called_once_with(annotations_file, ipose)
        assert keypoints == [[0, 0, 0]] * 16

    def test_get_keypoints__returns_parsed_keypoint(self, mocker, mock_loader_class):
        vnames = ['x', 'y', 'id']
        dummy_keypoints_annotations = mocker.MagicMock()
        dummy_keypoints_annotations.dtype.names = vnames
        dummy_keypoints_annotations.__len__.return_value = 1
        dummy_keypoints_annotations[0][0][0].__getitem__.return_value = 1
        dummy_keypoints_annotations.__iter__ = mocker.MagicMock()
        mock_get_keypoints = mocker.patch.object(DatasetAnnotationLoader, "get_keypoint_annotations", return_value=dummy_keypoints_annotations)

        annotations_file = {"dummy": 'data'}
        ipose = 1
        keypoints = mock_loader_class.get_keypoints(annotations_file, ipose)

        mock_get_keypoints.assert_called_once_with(annotations_file, ipose)
        assert keypoints[1] == [1.0, 1.0, -1]
        assert len(keypoints) == 16

    def test_get_keypoint_annotations__returns_empty(self, mocker, mock_loader_class):
        keypoint_annotations = mock_loader_class.get_keypoint_annotations(
            annotations_file=[[], [[], [], [], [], [[[[['dummy', 'data']]]]]]],
            ipose=0
        )
        assert keypoint_annotations == []

    def test_get_keypoint_annotations__returns_value(self, mocker, mock_loader_class):
        keypoint_annotations = mock_loader_class.get_keypoint_annotations(
            annotations_file=[[], [[], [], [], [], [[[[['dummy', 'data']]]]]]],
            ipose=1
        )
        assert keypoint_annotations == ['dummy', 'data']

    def test_get_head_coordinates__returns_default(self, mocker, mock_loader_class):
        head_coordinates = mock_loader_class.get_head_coordinates(
            annotations_file=[[], [[[1]], [[2]], [[3]], [[4]]]],
            ipose=1,
            pnames=[]
        )
        assert head_coordinates == (-1.0, -1.0, -1.0, -1.0)

    def test_get_head_coordinates__returns_coords(self, mocker, mock_loader_class):
        head_coordinates = mock_loader_class.get_head_coordinates(
            annotations_file=[[], [[[1]], [[2]], [[3]], [[4]]]],
            ipose=1,
            pnames=['x1', 'y1', 'x2', 'y2']
        )
        assert head_coordinates == (1.0, 2.0, 3.0, 4.0)

    def test_get_person_scale__return_default(self, mocker, mock_loader_class):
        scale = mock_loader_class.get_person_scale(
            annotations_file=[[], [[[1]], [[2]], [[3]], [[4]], [[3.5]]]],
            ipose=0,
            pnames=['x1', 'y1', 'x2', 'y2']
        )
        assert scale == -1.0

    def test_get_person_scale__return_person_scale(self, mocker, mock_loader_class):
        scale = mock_loader_class.get_person_scale(
            annotations_file=[[], [[[1]], [[2]], [[3]], [[4]], [[3.5]]]],
            ipose=1,
            pnames=['x1', 'y1', 'x2', 'y2', 'scale']
        )
        assert scale == 3.5

    def test_get_person_center_coordinates__return_default(self, mocker, mock_loader_class):
        objpos = mock_loader_class.get_person_center_coordinates(
            annotations_file=[[], [[[1]], [[2]], [[3]], [[4]]]],
            ipose=0,
            pnames=['x1', 'y1', 'x2', 'y2', 'scale', 'objpos']
        )
        assert objpos == {"x": -1.0, "y": -1.0}

    def test_get_person_center_coordinates__return_position_coordinates(self, mocker, mock_loader_class):
        objpos = mock_loader_class.get_person_center_coordinates(
            annotations_file=mocker.MagicMock(),
            ipose=1,
            pnames=['x1', 'y1', 'x2', 'y2', 'scale', 'objpos']
        )
        assert not objpos == {"x": -1.0, "y": -1.0}

    def test_get_partial_poses_annotations__return_empty_list(self, mocker, mock_loader_class):
        mock_get_annotation_file = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=[])
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale")
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates")

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_partial_poses_annotations(annotations, ifile, pnames)

        mock_get_annotation_file.assert_called_once_with(annotations, ifile)
        assert not mock_get_scale.called
        assert not mock_get_objpos.called
        assert poses_annotations == []

    def test_get_partial_poses_annotations__single_annotation(self, mocker, mock_loader_class):
        dummy_annotation = [0]
        dummy_scale = [3.10]
        dummy_objpos = {"x": 10.0, "y": 10.0}
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annotation)
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale", return_value=dummy_scale)
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates", return_value=dummy_objpos)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_partial_poses_annotations(annotations, ifile, pnames)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        mock_get_scale.assert_called_once_with(dummy_annotation, 0, pnames)
        mock_get_objpos.assert_called_once_with(dummy_annotation, 0, pnames)
        assert poses_annotations == [{
            "scale": dummy_scale,
            "objpos": dummy_objpos
        }]

    def test_get_partial_poses_annotations__multiple_annotations(self, mocker, mock_loader_class):
        dummy_annotation = [['dummy_annot']]*5
        dummy_scale = [3.10]
        dummy_objpos = {"x": 10.0, "y": 10.0}
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annotation)
        mock_get_scale = mocker.patch.object(DatasetAnnotationLoader, "get_person_scale", return_value=dummy_scale)
        mock_get_objpos = mocker.patch.object(DatasetAnnotationLoader, "get_person_center_coordinates", return_value=dummy_objpos)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = ['dummy_name1', 'dummy_name2']
        poses_annotations = mock_loader_class.get_partial_poses_annotations(annotations, ifile, pnames)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert mock_get_scale.call_count == 5
        assert mock_get_objpos.call_count == 5
        assert poses_annotations == [{
            "scale": dummy_scale,
            "objpos": dummy_objpos
        }]*5

    def test_get_activities__returns_default(self, mocker, mock_loader_class):
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name")
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name")
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id")

        annotations = {"RELEASE": []}
        num_files = 1
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        mock_get_annotation.assert_called_once_with(annotations, 0)
        assert not mock_get_category_name.called
        assert not mock_get_activity_name.called
        assert not mock_get_activity_id.called
        assert activities == [{
            "category_name": '',
            "activity_name": '',
            "activity_id": -1
        }]

    def test_get_activities__returns_single_activity(self, mocker, mock_loader_class):
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[1])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name", return_value='category1')
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name", return_value='activity1')
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id", return_value=1)

        annotations = {"RELEASE": []}
        num_files = 1
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        mock_get_annotation.assert_called_once_with(annotations, 0)
        mock_get_category_name.assert_called_once_with(annotations, 0)
        mock_get_activity_name.assert_called_once_with(annotations, 0)
        mock_get_activity_id.assert_called_once_with(annotations, 0)
        assert activities == [{
            "category_name": 'category1',
            "activity_name": 'activity1',
            "activity_id": 1
        }]

    def test_get_activities__returns_multiple_activities(self, mocker, mock_loader_class):
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[1])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name", return_value='category1')
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name", return_value='activity1')
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id", return_value=1)

        annotations = {"RELEASE": []}
        num_files = 5
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        assert mock_get_annotation.call_count == 5
        assert mock_get_category_name.call_count == 5
        assert mock_get_activity_name.call_count == 5
        assert mock_get_activity_id.call_count == 5
        assert activities == [{
            "category_name": 'category1',
            "activity_name": 'activity1',
            "activity_id": 1
        }]*5

    def test_get_activity_annotation_of_file(self, mocker, mock_loader_class):
        activity_annotation = mock_loader_class.get_activity_annotation_of_file(
            annotations={"RELEASE": [[[[], [], [], [], [[], [[100]]]]]]},
            ifile=1
        )
        assert activity_annotation == 100

    def test_get_category_name(self, mocker, mock_loader_class):
        category_name = mock_loader_class.get_category_name(
            annotations={"RELEASE": [[[[], [], [], [], [[], [[['category1']]]]]]]},
            ifile=1
        )
        assert category_name == 'category1'

    def test_get_activity_name(self, mocker, mock_loader_class):
        activity_name = mock_loader_class.get_activity_name(
            annotations={"RELEASE": [[[[], [], [], [], [[], [[[], ['activity1']]]]]]]},
            ifile=1
        )
        assert activity_name == 'activity1'

    def test_get_activity_id(self, mocker, mock_loader_class):
        activity_id = mock_loader_class.get_activity_id(
            annotations={"RELEASE": [[[[], [], [], [], [[], [[[], [] ,[[12345]]]]]]]]},
            ifile=1
        )
        assert activity_id == 12345

    def test_get_single_persons__returns_single_person(self, mocker, mock_loader_class):
        mock_get_single_person = mocker.patch.object(DatasetAnnotationLoader, "get_single_persons_by_file", return_value={"dummy": 'data'})

        annotations = {"RELEASE": []}
        num_files = 1
        single_person = mock_loader_class.get_single_persons(annotations, num_files)

        mock_get_single_person.assert_called_once_with(annotations, 0)
        assert single_person == [{"dummy": 'data'}]

    def test_get_single_persons__returns_multiple_persons(self, mocker, mock_loader_class):
        mock_get_single_person = mocker.patch.object(DatasetAnnotationLoader, "get_single_persons_by_file", return_value={"dummy": 'data'})

        annotations = {"RELEASE": []}
        num_files = 5
        single_person = mock_loader_class.get_single_persons(annotations, num_files)

        assert mock_get_single_person.call_count == 5
        assert single_person == [{"dummy": 'data'}]*5

    def test_get_single_persons_by_file__returns_default(self, mocker, mock_loader_class):
        mock_get_single_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_single_person_annotations_for_file", return_value=[])

        annotations = {"RELEASE": []}
        ifile = 1
        single_person = mock_loader_class.get_single_persons_by_file(annotations, ifile)

        mock_get_single_annotation.assert_called_once_with(annotations, ifile)
        assert single_person == [-1]

    def test_get_single_persons_by_file__returns_is_person(self, mocker, mock_loader_class):
        dummy_single_annotations = [[1], [-1], [1]]
        mock_get_single_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_single_person_annotations_for_file", return_value=dummy_single_annotations)

        annotations = {"RELEASE": []}
        ifile = 1
        single_person = mock_loader_class.get_single_persons_by_file(annotations, ifile)

        mock_get_single_annotation.assert_called_once_with(annotations, ifile)
        assert single_person == [1, -1, 1]

    def test_get_single_person_annotations_for_file(self, mocker, mock_loader_class):
        single_person_annotation = mock_loader_class.get_single_person_annotations_for_file(
            annotations={"RELEASE": [[[[], [], [], [[], [['person1', 'person2']]]]]]},
            ifile=1
        )
        assert single_person_annotation == ['person1', 'person2']

    def test_get_video_names(self, mocker, mock_loader_class):
        dummy_video_annotations = [['video1'], ['video2'], ['video3']]
        mock_get_video_annotations = mocker.patch.object(DatasetAnnotationLoader, "get_video_annotations", return_value=dummy_video_annotations)

        annotations = {"RELEASE": []}
        video_names = mock_loader_class.get_video_names(annotations)

        mock_get_video_annotations.assert_called_once_with(annotations)
        assert video_names == ['video1', 'video2', 'video3']

    def test_get_video_annotations(self, mocker, mock_loader_class):
        video_annotations = mock_loader_class.get_video_annotations(
            annotations={"RELEASE": [[[[], [], [], [], [], [[['video1'], ['video2'], ['video3']]]]]]},
        )
        assert video_annotations == [['video1'], ['video2'], ['video3']]

    def test_filter_annotations_by_ids__returns_empty_list(self, mocker, mock_loader_class):
        annotations_subset = mock_loader_class.filter_annotations_by_ids(
            annotations=[0, 2, 4, 6, 8, 10],
            image_ids=[]
        )
        assert annotations_subset == []

    def test_filter_annotations_by_ids__returns_full_list(self, mocker, mock_loader_class):
        annotations_subset = mock_loader_class.filter_annotations_by_ids(
            annotations=[0, 2, 4, 6, 8, 10],
            image_ids=list(range(6))
        )
        assert annotations_subset == [0, 2, 4, 6, 8, 10]

    def test_filter_annotations_by_ids__returns_filtered_list(self, mocker, mock_loader_class):
        annotations_subset = mock_loader_class.filter_annotations_by_ids(
            annotations=[0, 2, 4, 6, 8, 10],
            image_ids=[2, 3, 5]
        )
        assert annotations_subset == [4, 6, 10]
