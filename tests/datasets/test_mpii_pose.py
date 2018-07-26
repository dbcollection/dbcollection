"""
Test the base classes for managing datasets and tasks
for the MPII Human Pose Dataset.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.datasets.mpii_pose.keypoints import (
    Keypoints,
    KeypointsClean,
    DatasetAnnotationLoader,
    CustomBaseField,
    ImageFilenamesField,
    ScalesField,
    ObjposField,
    VideoIdsField,
    VideoNamesField,
    FrameSecField,
    KeypointLabelsField,
    CategoryNamesField,
    ActivityNamesField,
    ActivityIdsField,
    SinglePersonField,
    HeadBoundingBoxField,
    KeypointsField,
    ObjectFieldNamesField,
    ObjectIdsField,
    SinglePersonPerImageList,
    KeypointsPerImageList
)


class TestKeypointsTask:
    """Unit tests for the mpii Keypoints task."""

    @staticmethod
    @pytest.fixture()
    def mock_keypoints_class():
        return Keypoints(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_keypoints_class):
        assert mock_keypoints_class.filename_h5 == 'keypoint'
        assert mock_keypoints_class.is_full == True

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
        assert trainval_data == {"train": ['trainval_data']}
        assert train_data == {"train01": ['train_data']}
        assert val_data == {"val01": ['val_data']}
        assert test_data == {"test": ['test_data']}

    def test_process_set_metadata(self, mocker, mock_keypoints_class):
        dummy_ids = [0, 1, 2, 3, 4, 5]
        mock_image_field = mocker.patch.object(ImageFilenamesField, "process", return_value=dummy_ids)
        mock_scale_field = mocker.patch.object(ScalesField, "process")
        mock_objpos_field = mocker.patch.object(ObjposField, "process")
        mock_videoidx_field = mocker.patch.object(VideoIdsField, "process", return_value=dummy_ids)
        mock_videonames_field = mocker.patch.object(VideoNamesField, "process")
        mock_frame_sec_field = mocker.patch.object(FrameSecField, "process")
        mock_keypointlbls_field = mocker.patch.object(KeypointLabelsField, "process")
        mock_category_names_field = mocker.patch.object(CategoryNamesField, "process")
        mock_activity_names_field = mocker.patch.object(ActivityNamesField, "process")
        mock_activity_ids_field = mocker.patch.object(ActivityIdsField, "process")
        mock_single_person_field = mocker.patch.object(SinglePersonField, "process")
        mock_head_bbox_field = mocker.patch.object(HeadBoundingBoxField, "process")
        mock_keypoints_field = mocker.patch.object(KeypointsField, "process")
        mock_objfields_field = mocker.patch.object(ObjectFieldNamesField, "process")
        mock_objids_field = mocker.patch.object(ObjectIdsField, "process")
        mock_single_person_per_image_list = mocker.patch.object(SinglePersonPerImageList, "process")
        mock_keypoints_per_image_list = mocker.patch.object(KeypointsPerImageList, "process")

        mock_keypoints_class.process_set_metadata(
            data={
                "image_filenames": [1],
                "frame_sec": [1],
                "video_idx": [1],
                "pose_annotations": [1],
                "activity": [1],
                "single_person": [1],
                "video_names": [1]
            },
            set_name='train'
        )

        mock_image_field.assert_called_once_with()
        mock_scale_field.assert_called_once_with()
        mock_objpos_field.assert_called_once_with()
        mock_videoidx_field.assert_called_once_with()
        mock_videonames_field.assert_called_once_with(dummy_ids)
        mock_frame_sec_field.assert_called_once_with()
        mock_keypointlbls_field.assert_called_once_with()
        mock_category_names_field.assert_called_once_with()
        mock_activity_names_field.assert_called_once_with()
        mock_activity_ids_field.assert_called_once_with()
        mock_single_person_field.assert_called_once_with()
        mock_head_bbox_field.assert_called_once_with()
        mock_keypoints_field.assert_called_once_with()
        mock_objfields_field.assert_called_once_with()
        mock_objids_field.assert_called_once_with(dummy_ids, dummy_ids)
        mock_single_person_per_image_list.assert_called_once_with()
        mock_keypoints_per_image_list.assert_called_once_with()


class TestKeypointsCleanTask:
    """Unit tests for the mpii KeypointsClean task."""

    @staticmethod
    @pytest.fixture()
    def mock_keypointsclean_class():
        return KeypointsClean(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_keypointsclean_class):
        assert mock_keypointsclean_class.filename_h5 == 'keypoint_clean'
        assert mock_keypointsclean_class.is_full == False


class TestDatasetAnnotationLoader:
    """Unit tests for DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            is_full=False,
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
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

        from dbcollection.datasets.mpii_pose.train_image_ids import train_images_ids
        assert annotations == dummy_data_filtered
        mock_load_annotations.assert_called_once_with(is_test=False)
        mock_filter_annotations.assert_called_once_with(dummy_data, train_images_ids)

    def test_load_val_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        dummy_data_filtered = {"dummy": 'filtered'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)
        mock_filter_annotations = mocker.patch.object(DatasetAnnotationLoader, "filter_annotations_by_ids", return_value=dummy_data_filtered)

        annotations = mock_loader_class.load_val_data()

        from dbcollection.datasets.mpii_pose.val_image_ids import val_images_ids
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
        dummy_image_ids = [1, 2, 3, 3]
        dummy_filenames = ['filename1', 'filename2', 'filename2', 'filename3', 'filename3']
        dummy_framesec = [141,20,13,74,6]
        dummy_videos = [6,20,1,1, 4]
        dummy_poses = [[0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
        dummy_activities = [0, 1, 0, 2, 3]
        dummy_single = [1,1,1,0,1]
        dummy_video_names = ['video1', 'video2', 'video3']
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotation_data_from_disk", return_value=dummy_annotations)
        mock_get_total_files = mocker.patch.object(DatasetAnnotationLoader, "get_num_files", return_value=dummy_nfiles)
        mock_get_image_ids = mocker.patch.object(DatasetAnnotationLoader, "get_image_ids", return_value=dummy_image_ids)
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
        mock_get_image_ids.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_filenames.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_frame_sec.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_video_idx.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_pose.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_activity.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_single.assert_called_once_with(dummy_annotations, dummy_nfiles, True)
        mock_get_video_names.assert_called_once_with(dummy_annotations)
        assert annotations == {
            "image_ids": dummy_image_ids,
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

    def test_get_image_ids__only_one_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)

        annotations = {"RELEASE": []}
        num_files = 1
        image_ids = mock_loader_class.get_image_ids(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        assert image_ids == [0]

    def test_get_image_ids__multiple_file(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)

        annotations = {"RELEASE": []}
        num_files = 10
        image_ids = mock_loader_class.get_image_ids(annotations, num_files, True)

        assert mock_is_test.call_count == 10
        assert image_ids == list(range(10))

    def test_get_image_ids__returns_empty_list(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=False)

        annotations = {"RELEASE": []}
        num_files = 1
        image_ids = mock_loader_class.get_image_ids(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        assert image_ids == []

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
        assert video_idx == 200 - 1

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
        assert poses_annotations == [[]]

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

    def test_get_pose_annotation_names__try_branch__return_names(self, mocker, mock_loader_class):
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

    def test_get_pose_annotation_names__try_branch__return_empty_list(self, mocker, mock_loader_class):
        dummy_annot = mocker.MagicMock()
        dummy_annot.dtype = mocker.MagicMock()
        dummy_annot.dtype.names = None
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_annotation_by_file_id", return_value=dummy_annot)

        annotations = {"RELEASE": []}
        ifile = 1
        pnames = mock_loader_class.get_pose_annotation_names(annotations, ifile)

        mock_get_annotation.assert_called_once_with(annotations, ifile)
        assert pnames == []

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

    @pytest.mark.skipif(sys.version[0] == '2', reason="requires python3")
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

    def test_get_keypoint_annotations__try_branch__returns_value(self, mocker, mock_loader_class):
        keypoint_annotations = mock_loader_class.get_keypoint_annotations(
            annotations_file=[[], [[], [], [], [], [[[[['dummy', 'data']]]]]]],
            ipose=1
        )
        assert keypoint_annotations == ['dummy', 'data']

    def test_get_keypoint_annotations__try_branch__returns_empty_list(self, mocker, mock_loader_class):
        keypoint_annotations = mock_loader_class.get_keypoint_annotations(
            annotations_file=[[], [[], [], [], [], [[[['dummy_data']]]]]],
            ipose=1
        )
        assert keypoint_annotations == []

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
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name")
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name")
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id")

        annotations = {"RELEASE": []}
        num_files = 1
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
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
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[1])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name", return_value='category1')
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name", return_value='activity1')
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id", return_value=1)

        annotations = {"RELEASE": []}
        num_files = 1
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
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
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_annotation = mocker.patch.object(DatasetAnnotationLoader, "get_activity_annotation_of_file", return_value=[1])
        mock_get_category_name = mocker.patch.object(DatasetAnnotationLoader, "get_category_name", return_value='category1')
        mock_get_activity_name = mocker.patch.object(DatasetAnnotationLoader, "get_activity_name", return_value='activity1')
        mock_get_activity_id = mocker.patch.object(DatasetAnnotationLoader, "get_activity_id", return_value=1)

        annotations = {"RELEASE": []}
        num_files = 5
        activities = mock_loader_class.get_activities(annotations, num_files, True)

        assert mock_is_test.call_count == 5
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
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_single_person = mocker.patch.object(DatasetAnnotationLoader, "get_single_persons_by_file", return_value={"dummy": 'data'})

        annotations = {"RELEASE": []}
        num_files = 1
        single_person = mock_loader_class.get_single_persons(annotations, num_files, True)

        mock_is_test.assert_called_once_with(annotations, 0)
        mock_get_single_person.assert_called_once_with(annotations, 0)
        assert single_person == [{"dummy": 'data'}]

    def test_get_single_persons__returns_multiple_persons(self, mocker, mock_loader_class):
        mock_is_test = mocker.patch.object(DatasetAnnotationLoader, "is_test_annotation", return_value=True)
        mock_get_single_person = mocker.patch.object(DatasetAnnotationLoader, "get_single_persons_by_file", return_value={"dummy": 'data'})

        annotations = {"RELEASE": []}
        num_files = 5
        single_person = mock_loader_class.get_single_persons(annotations, num_files, True)

        assert mock_is_test.call_count == 5
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

    def test_filter_annotations_by_ids(self, mocker, mock_loader_class):
        dummy_filtered = [['dummy_data1'], ['dummy_data2'], ['dummy_data3']]
        mock_filtered_ids = mocker.patch.object(DatasetAnnotationLoader, "get_filtered_ids", return_value=[1,2,3,4,5])
        mock_select_items = mocker.patch.object(DatasetAnnotationLoader, "select_items_from_list", return_value=dummy_filtered)

        annotations = {
            "image_ids": list(range(5)),
            "image_filenames": [['dummy_data'], ['dummy_data']],
            "frame_sec": [['dummy_data'], ['dummy_data']],
            "video_idx": [['dummy_data'], ['dummy_data']],
            "pose_annotations": [['dummy_data'], ['dummy_data']],
            "activity": [['dummy_data'], ['dummy_data']],
            "single_person": [['dummy_data'], ['dummy_data']],
            "video_names": [['dummy_video1'], ['dummy_video2']]
        }
        set_image_ids = [1,2,5,6,9]
        filtered_annotations = mock_loader_class.filter_annotations_by_ids(annotations, set_image_ids)

        mock_filtered_ids.assert_called_once_with(list(range(5)), set_image_ids)
        assert mock_select_items.call_count == 6
        assert filtered_annotations == {
            "image_filenames": dummy_filtered,
            "frame_sec": dummy_filtered,
            "video_idx": dummy_filtered,
            "pose_annotations": dummy_filtered,
            "activity": dummy_filtered,
            "single_person": dummy_filtered,
            "video_names": [['dummy_video1'], ['dummy_video2']]
        }

    def test_get_filtered_ids(self, mocker, mock_loader_class):
        filtered_ids = mock_loader_class.get_filtered_ids(
            image_ids=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            set_image_ids=[3, 4, 8, 9]
        )
        assert filtered_ids == [7, 6, 2, 1]

    def test_select_items_from_list(self, mocker, mock_loader_class):
        annotations_filtered = mock_loader_class.select_items_from_list(
            annotations=[['dummy_data1'], ['dummy_data2'], ['dummy_data3'], ['dummy_data4'], ['dummy_data5']],
            filtered_ids=[2,3]
        )
        assert annotations_filtered == [['dummy_data3'], ['dummy_data4']]


@pytest.fixture()
def test_data_loaded():
    image_filenames = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    frame_sec = [102, 11, 32]
    video_idx = [2, 1, 1]
    pose_annotations = [[[[[1, 1, 1]]*16], [[[0, 0, 0]]*16]], [[[0, 0, 0]]*16], [[[0, 0, 0]]*16]]
    activity = [
        {"category_name": 'category1', "activity_name": 'activity1', "activity_id": 0},
        {"category_name": 'category2', "activity_name": 'activity2', "activity_id": 1},
        {"category_name": 'category2', "activity_name": 'activity3', "activity_id": 2}
    ]
    single_person = [0, 1, 0]
    video_names = ['video2', 'video1', 'video1']
    return {
        "image_filenames": image_filenames,
        "frame_sec": frame_sec,
        "video_idx": video_idx,
        "pose_annotations": pose_annotations,
        "activity": activity,
        "single_person": single_person,
        "video_names": video_names
    }


@pytest.fixture()
def field_kwargs(test_data_loaded):
    return {
        "is_full": False,
        "data": test_data_loaded,
        "set_name": 'train',
        "hdf5_manager": {'dummy': 'object'},
        "verbose": True
    }


class TestCustomBaseField:
    """Unit tests for the CustomBaseField class."""

    @staticmethod
    @pytest.fixture()
    def mock_custom_basefield__class(field_kwargs):
        return CustomBaseField(**field_kwargs)

    def test_get_image_filenames_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_image_filenames_annotations() == test_data_loaded['image_filenames']

    def test_get_pose_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_pose_annotations() == test_data_loaded['pose_annotations']

    def test_get_single_person_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_single_person_annotations() == test_data_loaded['single_person']

    def test_get_video_idx_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_video_idx_annotations() == test_data_loaded['video_idx']

    def test_get_video_names_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_video_names_annotations() == test_data_loaded['video_names']

    def test_get_frame_sec_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_frame_sec_annotations() == test_data_loaded['frame_sec']

    def test_get_activity_annotations(self, mocker, mock_custom_basefield__class, test_data_loaded):
        assert mock_custom_basefield__class.get_activity_annotations() == test_data_loaded['activity']


class TestImageFilenamesField:
    """Unit tests for the ImageFilenamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_image_filenames_class(field_kwargs):
        return ImageFilenamesField(**field_kwargs)

    def test_process(self, mocker, mock_image_filenames_class):
        mock_get_images = mocker.patch.object(ImageFilenamesField, "get_image_filenames", return_value=(['image1.jpg', 'image2.jpg', 'image3.jpg'], [0, 1, 2]))
        mock_save_hdf5 = mocker.patch.object(ImageFilenamesField, "save_field_to_hdf5")

        image_filenames_ids = mock_image_filenames_class.process()

        assert image_filenames_ids == [0, 1, 2]
        mock_get_images.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='image_filenames',
        #     data=str2ascii(['image1.jpg', 'image2.jpg', 'image3.jpg']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_image_filenames(self, mocker, mock_image_filenames_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(ImageFilenamesField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(ImageFilenamesField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy', 'dummy'], ['dummy']])

        image_filenames, image_filename_ids = mock_image_filenames_class.get_image_filenames()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert image_filenames == ['image1', 'image2', 'image2', 'image2', 'image3']
        assert image_filename_ids == [0, 1, 1, 1, 2]


class TestScalesField:
    """Unit tests for the ScalesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_scales_class(field_kwargs):
        return ScalesField(**field_kwargs)

    def test_process(self, mocker, mock_scales_class):
        mock_get_scales = mocker.patch.object(ScalesField, "get_scales", return_value=[1.0, 3.1, 2.0])
        mock_save_hdf5 = mocker.patch.object(ScalesField, "save_field_to_hdf5")

        mock_scales_class.process()

        mock_get_scales.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='scales',
        #     data=np.array([1.0, 3.1, 2.0], dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=0
        # )

    def test_get_scales(self, mocker, mock_scales_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(ScalesField, "get_image_filenames_annotations", return_value=['image1', 'image2'])
        mock_get_pose_annotations = mocker.patch.object(ScalesField, "get_pose_annotations", return_value=[[{"scale": 1.0}], [{"scale": 2.0}, {"scale": 1.5}]])

        scales = mock_scales_class.get_scales()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert scales == [1.0, 2.0, 1.5]


class TestObjposField:
    """Unit tests for the ObjposField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objpos_class(field_kwargs):
        return ObjposField(**field_kwargs)

    def test_process(self, mocker, mock_objpos_class):
        mock_get_objpos = mocker.patch.object(ObjposField, "get_objpos", return_value=[[12.5, 25.0], [11.0, 31.0], [25.0, 25.0]])
        mock_save_hdf5 = mocker.patch.object(ObjposField, "save_field_to_hdf5")

        mock_objpos_class.process()

        mock_get_objpos.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='objpos',
        #     data=np.array([[12.5, 25.0], [11.0, 31.0], [25.0, 25.0]], dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=0
        # )

    def test_get_objpos(self, mocker, mock_objpos_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(ObjposField, "get_image_filenames_annotations", return_value=['image1', 'image2'])
        mock_get_pose_annotations = mocker.patch.object(ObjposField, "get_pose_annotations", return_value=[[{"objpos": {"x": 11.0, "y":15.0}}], [{"objpos": {"x": 10.0, "y":10.0}}, {"objpos": {"x": 20.0, "y":20.0}}]])

        objpos = mock_objpos_class.get_objpos()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert objpos == [[11.0, 15.0], [10.0, 10.0], [20.0, 20.0]]


class TestVideoIdsField:
    """Unit tests for the VideoIdsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_videoidx_class(field_kwargs):
        return VideoIdsField(**field_kwargs)

    def test_process(self, mocker, mock_videoidx_class):
        mock_get_video_ids = mocker.patch.object(VideoIdsField, "get_video_ids", return_value=[0, 1, 1, 2])
        mock_save_hdf5 = mocker.patch.object(VideoIdsField, "save_field_to_hdf5")

        video_ids = mock_videoidx_class.process()

        mock_get_video_ids.assert_called_once_with()
        assert video_ids == [0, 1, 1, 2]
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='video_ids',
        #     data=np.array([0, 1, 1, 2], dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_video_ids(self, mocker, mock_videoidx_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(VideoIdsField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(VideoIdsField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])
        mock_get_video_annotations = mocker.patch.object(VideoIdsField, "get_video_idx_annotations", return_value=[0, 1, 2])

        video_ids = mock_videoidx_class.get_video_ids()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_video_annotations.assert_called_once_with()
        assert video_ids == [0, 1, 1, 2]


class TestVideoNamesField:
    """Unit tests for the VideoNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_videonames_class(field_kwargs):
        return VideoNamesField(**field_kwargs)

    def test_process(self, mocker, mock_videonames_class):
        mock_get_video_names = mocker.patch.object(VideoNamesField, "get_video_names", return_value=['video1', 'video2', 'video2', 'video3'])
        mock_save_hdf5 = mocker.patch.object(VideoNamesField, "save_field_to_hdf5")

        mock_videonames_class.process([0, 1, 1, 2])

        mock_get_video_names.assert_called_once_with([0, 1, 1, 2])
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='video_names',
        #     data=str2ascii(['video1', 'video2', 'video2', 'video3']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_video_names(self, mocker, mock_videonames_class, test_data_loaded):
        mock_get_video_annotations = mocker.patch.object(VideoNamesField, "get_video_names_annotations", return_value=['video1', 'video2', 'video3'])

        video_names = mock_videonames_class.get_video_names([0, 1, 1, 2, -1])

        mock_get_video_annotations.assert_called_once_with()
        assert video_names == ['video1', 'video2', 'video2', 'video3', 'NA']


class TestFrameSecField:
    """Unit tests for the FrameSecField class."""

    @staticmethod
    @pytest.fixture()
    def mock_frame_sec_class(field_kwargs):
        return FrameSecField(**field_kwargs)

    def test_process(self, mocker, mock_frame_sec_class):
        mock_get_frame_sec = mocker.patch.object(FrameSecField, "get_frame_sec", return_value=[0, 1, 2, 3])
        mock_save_hdf5 = mocker.patch.object(FrameSecField, "save_field_to_hdf5")

        mock_frame_sec_class.process()

        mock_get_frame_sec.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='frame_sec',
        #     data=np.array([0, 1, 2, 3], dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_frame_sec(self, mocker, mock_frame_sec_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(FrameSecField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(FrameSecField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])
        mock_get_frame_annotations = mocker.patch.object(FrameSecField, "get_frame_sec_annotations", return_value=[0, 1, 2, 3])

        frame_sec = mock_frame_sec_class.get_frame_sec()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_frame_annotations.assert_called_once_with()
        assert frame_sec == [0, 1, 1, 2]


class TestKeypointLabelsField:
    """Unit tests for the KeypointLabelsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_kplbls_class(field_kwargs):
        return KeypointLabelsField(**field_kwargs)

    def test_process(self, mocker, mock_kplbls_class):
        mock_get_kp_lbls = mocker.patch.object(KeypointLabelsField, "get_keypoint_labels", return_value=['right ankle', 'right knee', 'right hip'])
        mock_save_hdf5 = mocker.patch.object(KeypointLabelsField, "save_field_to_hdf5")

        mock_kplbls_class.process()

        mock_get_kp_lbls.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='keypoint_labels',
        #     data=str2ascii(['right ankle', 'right knee', 'right hip']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_keypoint_labels(self, mocker, mock_kplbls_class, test_data_loaded):
        keypoints_labels = mock_kplbls_class.get_keypoint_labels()
        assert keypoints_labels == [
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


class TestCategoryNamesField:
    """Unit tests for the CategoryNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_category_names_class(field_kwargs):
        return CategoryNamesField(**field_kwargs)

    def test_process(self, mocker, mock_category_names_class):
        mock_get_category_name = mocker.patch.object(CategoryNamesField, "get_category_name", return_value=['category1', 'category2', 'category3'])
        mock_save_hdf5 = mocker.patch.object(CategoryNamesField, "save_field_to_hdf5")

        mock_category_names_class.process()

        mock_get_category_name.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='category_name',
        #     data=str2ascii(['category1', 'category2', 'category3']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_category_name(self, mocker, mock_category_names_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(CategoryNamesField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(CategoryNamesField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])
        mock_get_activity_annotations = mocker.patch.object(CategoryNamesField, "get_activity_annotations", return_value=[
            {"category_name": 'category1', "activity_name": '', "activity_id": -1},
            {"category_name": 'category2', "activity_name": '', "activity_id": -1},
            {"category_name": 'category3', "activity_name": '', "activity_id": -1}
        ])

        category_names = mock_category_names_class.get_category_name()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_activity_annotations.assert_called_once_with()
        assert category_names == ['category1', 'category2', 'category2', 'category3']


class TestActivityNamesField:
    """Unit tests for the ActivityNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_activity_names_class(field_kwargs):
        return ActivityNamesField(**field_kwargs)

    def test_process(self, mocker, mock_activity_names_class):
        mock_get_activity_name = mocker.patch.object(ActivityNamesField, "get_activity_name", return_value=['activity1', 'activity2', 'activity3'])
        mock_save_hdf5 = mocker.patch.object(ActivityNamesField, "save_field_to_hdf5")

        mock_activity_names_class.process()

        mock_get_activity_name.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='activity_name',
        #     data=str2ascii(['activity1', 'activity2', 'activity3']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_activity_name(self, mocker, mock_activity_names_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(ActivityNamesField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(ActivityNamesField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])
        mock_get_activity_annotations = mocker.patch.object(ActivityNamesField, "get_activity_annotations", return_value=[
            {"category_name": '', "activity_name": 'activity1', "activity_id": -1},
            {"category_name": '', "activity_name": 'activity2', "activity_id": -1},
            {"category_name": '', "activity_name": 'activity3', "activity_id": -1}
        ])

        activity_names = mock_activity_names_class.get_activity_name()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_activity_annotations.assert_called_once_with()
        assert activity_names == ['activity1', 'activity2', 'activity2', 'activity3']


class TestActivityIdsField:
    """Unit tests for the ActivityIdsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_activity_ids_class(field_kwargs):
        return ActivityIdsField(**field_kwargs)

    def test_process(self, mocker, mock_activity_ids_class):
        mock_get_activity_id = mocker.patch.object(ActivityIdsField, "get_activity_ids", return_value=[1, 2, 3])
        mock_save_hdf5 = mocker.patch.object(ActivityIdsField, "save_field_to_hdf5")

        mock_activity_ids_class.process()

        mock_get_activity_id.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='activity_id',
        #     data=np.array([1, 2, 3], dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_activity_ids(self, mocker, mock_activity_ids_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(ActivityIdsField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(ActivityIdsField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])
        mock_get_activity_annotations = mocker.patch.object(ActivityIdsField, "get_activity_annotations", return_value=[
            {"category_name": '', "activity_name": '', "activity_id": 1},
            {"category_name": '', "activity_name": '', "activity_id": 2},
            {"category_name": '', "activity_name": '', "activity_id": 3}
        ])

        activity_ids = mock_activity_ids_class.get_activity_ids()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_activity_annotations.assert_called_once_with()
        assert activity_ids == [1, 2, 2, 3]


class TestSinglePersonField:
    """Unit tests for the SinglePersonField class."""

    @staticmethod
    @pytest.fixture()
    def mock_single_person_class(field_kwargs):
        return SinglePersonField(**field_kwargs)

    def test_process(self, mocker, mock_single_person_class):
        mock_get_single_person = mocker.patch.object(SinglePersonField, "get_single_person", return_value=[0, 1, 1, 1, 0, 1])
        mock_save_hdf5 = mocker.patch.object(SinglePersonField, "save_field_to_hdf5")

        mock_single_person_class.process()

        mock_get_single_person.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='single_person',
        #     data=np.array([0, 1, 1, 1, 0, 1], dtype=np.uint8),
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_single_person(self, mocker, mock_single_person_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(SinglePersonField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(SinglePersonField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy', 'dummy'], ['dumnmy', 'dummy', 'dummy']])
        mock_get_single_pose_annotations = mocker.patch.object(SinglePersonField, "get_single_person_annotations", return_value=[[-1], [1, 1, 1], [-1, 1]])

        single_persons = mock_single_person_class.get_single_person()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        mock_get_single_pose_annotations.assert_called_once_with()
        assert single_persons == [0, 1, 1, 1, 0, 1, 0]


class TestHeadBoundingBoxField:
    """Unit tests for the HeadBoundingBoxField class."""

    @staticmethod
    @pytest.fixture()
    def mock_head_bbox_class(field_kwargs):
        return HeadBoundingBoxField(**field_kwargs)

    def test_process(self, mocker, mock_head_bbox_class):
        mock_get_head_bbox = mocker.patch.object(HeadBoundingBoxField, "get_head_bboxes", return_value=[[1, 1, 10, 10], [10, 10, 20, 20], [40, 40, 60, 60]])
        mock_save_hdf5 = mocker.patch.object(HeadBoundingBoxField, "save_field_to_hdf5")

        mock_head_bbox_class.process()

        mock_get_head_bbox.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='head_bbox',
        #     data=np.array([[1, 1, 10, 10], [10, 10, 20, 20], [40, 40, 60, 60]], dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    def test_get_head_bboxes(self, mocker, mock_head_bbox_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(HeadBoundingBoxField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(HeadBoundingBoxField, "get_pose_annotations", return_value=[[{"head_bbox": (1, 1, 10, 10)}], [{"head_bbox": (100, 100, 200, 200)}, {"head_bbox": (1, 1, 5, 5)}], [{"head_bbox": (10, 10, 15, 15)}]])

        head_bbox = mock_head_bbox_class.get_head_bboxes()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert head_bbox == [
            (1, 1, 10, 10),
            (100, 100, 200, 200),
            (1, 1, 5, 5),
            (10, 10, 15, 15)
        ]


class TestKeypointsField:
    """Unit tests for the KeypointsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_keypoints_class(field_kwargs):
        return KeypointsField(**field_kwargs)

    def test_process(self, mocker, mock_keypoints_class):
        mock_get_keypoints = mocker.patch.object(KeypointsField, "get_keypoints", return_value=[[[0, 0, 0]]*16, [[1, 1, 1]]*16])
        mock_save_hdf5 = mocker.patch.object(KeypointsField, "save_field_to_hdf5")

        mock_keypoints_class.process()

        mock_get_keypoints.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='keypoints',
        #     data=np.array([[[0, 0, 0]]*16, [[1, 1, 1]]*16], dtype=np.float32),
        #     dtype=np.float32,
        #     fillvalue=-1
        # )

    def test_get_keypoints(self, mocker, mock_keypoints_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(KeypointsField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(KeypointsField, "get_pose_annotations", return_value=[
            [{"keypoints": [[1, 1, 1], [20, 30, 0]]}],
            [{"keypoints": [[5, 115, 1], [13, 31, 0]]}, {"keypoints": [[-1, -1, -1], [3, 3, 1]]}],
            [{"keypoints": [[10, 10, 1], [-1, -1, -1]]}]])

        keypoints = mock_keypoints_class.get_keypoints()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert keypoints == [
            [[1, 1, 1], [20, 30, 0]],
            [[5, 115, 1], [13, 31, 0]],
            [[-1, -1, -1], [3, 3, 1]],
            [[10, 10, 1], [-1, -1, -1]]
        ]


class TestObjectFieldNamesField:
    """Unit tests for the ObjectFieldNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objfields_class(field_kwargs):
        return ObjectFieldNamesField(**field_kwargs)

    def test_process(self, mocker, mock_objfields_class):
        mock_get_object_fields = mocker.patch.object(ObjectFieldNamesField, "get_object_fields", return_value=['field1', 'field2', 'field3'])
        mock_save_hdf5 = mocker.patch.object(ObjectFieldNamesField, "save_field_to_hdf5")

        mock_objfields_class.process()

        mock_get_object_fields.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_fields',
        #     data=str2ascii(['field1', 'field2', 'field3']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_keypoints__train_set(self, mocker, mock_objfields_class, test_data_loaded):
        assert mock_objfields_class.get_object_fields() == [
            "image_filenames",
            "scale",
            "objpos",
            "video_ids",
            "video_names",
            "frame_sec",
            "category_name",
            "activity_name",
            "activity_id",
            "single_person",
            "keypoint_labels",
            "head_bbox",
            "keypoints"
        ]

    def test_get_keypoints__test_set(self, mocker, mock_objfields_class, test_data_loaded):
        mock_objfields_class.set_name = 'test'
        assert mock_objfields_class.get_object_fields() == [
            "image_filenames",
            "scale",
            "objpos",
            "video_ids",
            "video_names",
            "frame_sec",
            "category_name",
            "activity_name",
            "activity_id",
            "single_person",
            "keypoint_labels"
        ]


class TestObjectIdsField:
    """Unit tests for the ObjectIdsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objids_class(field_kwargs):
        return ObjectIdsField(**field_kwargs)

    def test_process(self, mocker, mock_objids_class):
        dummy_ids = [
            [],
            [],
            []
        ]
        mock_get_object_ids = mocker.patch.object(ObjectIdsField, "get_object_ids", return_value=dummy_ids)
        mock_save_hdf5 = mocker.patch.object(ObjectIdsField, "save_field_to_hdf5")

        mock_objids_class.process(
            image_ids=[1,2,2,3],
            video_ids=[1,2,2,3]
        )

        mock_get_object_ids.assert_called_once_with([1,2,2,3], [1,2,2,3])
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_ids',
        #     data=np.array(dummy_ids, dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_object_ids(self, mocker, mock_objids_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(FrameSecField, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(FrameSecField, "get_pose_annotations", return_value=[['dummy'], ['dummy', 'dummy'], ['dummy']])

        object_ids = mock_objids_class.get_object_ids(
            image_ids=[0, 1, 1, 2],
            video_ids=[5, 6, 6, 4]
        )

        assert object_ids == [
            [0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 6, 6, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3]
        ]


class TestSinglePersonPerImageList:
    """Unit tests for the SinglePersonPerImageList class."""

    @staticmethod
    @pytest.fixture()
    def mock_single_per_image_class(field_kwargs):
        return SinglePersonPerImageList(**field_kwargs)

    def test_process(self, mocker, mock_single_per_image_class):
        mock_get_single = mocker.patch.object(SinglePersonPerImageList, "get_list_single_person_per_image", return_value=[[1], [2, 3, 4], [5, 6]])
        mock_save_hdf5 = mocker.patch.object(SinglePersonPerImageList, "save_field_to_hdf5")

        mock_single_per_image_class.process()

        mock_get_single.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_single_person_per_image',
        #     data=np.array(pad_list([[1], [2, 3, 4], [5, 6]], val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_list_single_person_per_image(self, mocker, mock_single_per_image_class, test_data_loaded):
        mock_get_single_person_annotations = mocker.patch.object(SinglePersonPerImageList, "get_single_person_annotations", return_value=[[-1], [1, 1, -1], [1]])

        single_person_per_image = mock_single_per_image_class.get_list_single_person_per_image()

        mock_get_single_person_annotations.assert_called_once_with()
        assert single_person_per_image == [[], [1, 2], [4]]


class TestKeypointsPerImageList:
    """Unit tests for the KeypointsPerImageList class."""

    @staticmethod
    @pytest.fixture()
    def mock_keypoints_per_image_class(field_kwargs):
        return KeypointsPerImageList(**field_kwargs)

    def test_process(self, mocker, mock_keypoints_per_image_class):
        mock_get_keypoints = mocker.patch.object(KeypointsPerImageList, "get_list_keypoints_per_image", return_value=[[1], [2, 4], [5, 6]])
        mock_save_hdf5 = mocker.patch.object(KeypointsPerImageList, "save_field_to_hdf5")

        mock_keypoints_per_image_class.process()

        mock_get_keypoints.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_keypoints_per_image',
        #     data=np.array(pad_list([[1], [2, 4], [5, 6]], val=-1), dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_list_keypoints_per_image(self, mocker, mock_keypoints_per_image_class, test_data_loaded):
        mock_get_image_annotations = mocker.patch.object(KeypointsPerImageList, "get_image_filenames_annotations", return_value=['image1', 'image2', 'image3'])
        mock_get_pose_annotations = mocker.patch.object(KeypointsPerImageList, "get_pose_annotations", return_value=[
            [{"keypoints": [[1, 1, 1]] * 16}, {"keypoints": [[0, 0, 0]] * 16}],
            [{"keypoints": [[5, 115, 1]] * 16}, {"keypoints": [[0, 0, 0]] * 16}, {"keypoints": [[3, 3, 1]] * 16}],
            [{"keypoints": [[10, 10, 1]] * 16}]])

        keypoints_per_image = mock_keypoints_per_image_class.get_list_keypoints_per_image()

        mock_get_image_annotations.assert_called_once_with()
        mock_get_pose_annotations.assert_called_once_with()
        assert keypoints_per_image == [[0], [2, 4], [5]]
