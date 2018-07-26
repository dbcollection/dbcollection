"""
MPII Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTaskNew, BaseField
from dbcollection.utils.decorators import display_message_processing, display_message_load_annotations
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_matlab


class Keypoints(BaseTaskNew):
    """MPII Keypoints preprocessing functions."""

    filename_h5 = 'keypoint'
    is_full = True

    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        loader = DatasetAnnotationLoader(
            is_full=self.is_full,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_trainval_data()}
        yield {"train01": loader.load_train_data()}
        yield {"val01": loader.load_val_data()}
        yield {"test": loader.load_test_data()}

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
        args = {
            "is_full": self.is_full,
            "data": data,
            "set_name": set_name,
            "hdf5_manager": self.hdf5_manager,
            "verbose": self.verbose
        }

        # Fields
        if self.verbose:
            print('\n==> Setting up the data fields:')
        image_ids = ImageFilenamesField(**args).process()
        ScalesField(**args).process()
        ObjposField(**args).process()
        video_ids = VideoIdsField(**args).process()
        VideoNamesField(**args).process(video_ids)
        FrameSecField(**args).process()
        KeypointLabelsField(**args).process()
        CategoryNamesField(**args).process()
        ActivityNamesField(**args).process()
        ActivityIdsField(**args).process()
        SinglePersonField(**args).process()
        if set_name is not 'test':
            HeadBoundingBoxField(**args).process()
            KeypointsField(**args).process()
        ObjectFieldNamesField(**args).process()
        ObjectIdsField(**args).process(image_ids, video_ids)

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        SinglePersonPerImageList(**args).process()
        if set_name is not 'test':
            KeypointsPerImageList(**args).process()


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, is_full, data_path, cache_path, verbose):
        self.is_full = is_full
        self.data_path = data_path
        self.cache_path = cache_path
        self.verbose = verbose

    def load_trainval_data(self):
        """Loads the train set annotation data from disk
        and returns it as a dictionary."""
        return self.load_annotations_set(is_test=False)

    def load_train_data(self):
        """Loads the train+val set annotation data from disk
        and returns it as a dictionary.

        This validation set is a split of the training set
        of the MPII Human Pose dataset. It is a custom
        split not available in the original dataset but
        it is crafted for use in validation tasks.
        """
        from .train_image_ids import train_images_ids
        annotations = self.load_annotations_set(is_test=False)
        return self.filter_annotations_by_ids(annotations, train_images_ids)

    def load_val_data(self):
        """Loads the val set annotation data from disk
        and returns it as a dictionary.

        This validation set is a split of the training set
        of the MPII Human Pose dataset. It is a custom
        split not available in the original dataset but
        it is crafted for use in validation tasks.
        """
        from .val_image_ids import val_images_ids
        annotations = self.load_annotations_set(is_test=False)
        return self.filter_annotations_by_ids(annotations, val_images_ids)

    def load_test_data(self):
        """Loads the test set annotation data from disk
        and returns it as a dictionary."""
        return self.load_annotations_set(is_test=True)

    @display_message_load_annotations
    def load_annotations_set(self, is_test):
        """Loads the annotation's data for the train + test splits."""
        annotations = self.load_annotation_data_from_disk()
        nfiles = self.get_num_files(annotations)
        return {
            "image_ids": self.get_image_ids(annotations, nfiles, is_test),
            "image_filenames": self.get_image_filenames(annotations, nfiles, is_test),
            "frame_sec": self.get_frame_sec(annotations, nfiles, is_test),
            "video_idx": self.get_video_indexes(annotations, nfiles, is_test),
            "pose_annotations": self.get_pose_annotations(annotations, nfiles, is_test),
            "activity": self.get_activities(annotations, nfiles, is_test),
            "single_person": self.get_single_persons(annotations, nfiles, is_test),
            "video_names": self.get_video_names(annotations)
        }

    def load_annotation_data_from_disk(self):
        """Loads the annotation's data from the data file."""
        annotation_filename = os.path.join(self.data_path,
                                           'mpii_human_pose_v1_u12_2',
                                           'mpii_human_pose_v1_u12_1.mat')
        annotations = self.load_file(annotation_filename)
        return annotations

    def load_file(self, filename):
        """Loads the data of the annotation file."""
        return load_matlab(filename)

    def get_num_files(self, annotations):
        """Returns the total number of files available in the dataset."""
        return len(annotations["RELEASE"][0][0][3])

    def get_image_ids(self, annotations, num_files, is_test):
        """Returns the image indexes from the annotation's data for a
        set split."""
        image_ids = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                image_ids.append(ifile)
        return image_ids

    def get_image_filenames(self, annotations, num_files, is_test):
        """Returns the image filenames from the annotation's data for a
        set split."""
        image_filenames = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                filename = self.get_filename_from_annotation_id(annotations, ifile)
                image_filenames.append(os.path.join('images', filename))
        return image_filenames

    def is_test_annotation(self, annotations, ifile):
        """Returns True if the annotation belongs to the test set.
        Otherwise, returns False."""
        return annotations['RELEASE'][0][0][1][0][ifile] == 0

    def get_filename_from_annotation_id(self, annotations, ifile):
        """Return the image file name for an id."""
        return str(annotations['RELEASE'][0][0][0][0][ifile][0][0][0][0][0])

    def get_frame_sec(self, annotations, num_files, is_test):
        """Returns the image's frame position (seconds) from the
        annotation's data for a set split."""
        frame_sec = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                frame_sec_ = self.get_frame_sec_from_annotation_id(annotations, ifile)
                frame_sec.append(frame_sec_)
        return frame_sec

    def get_frame_sec_from_annotation_id(self, annotations, ifile):
        if any(self.get_annotations_list_by_image_id(annotations, ifile)):
            return int(annotations['RELEASE'][0][0][0][0][ifile][2][0][0])
        else:
            return -1

    def get_annotations_list_by_image_id(self, annotations, ifile):
        """.Returns a list of annotations for a given image id."""
        return annotations['RELEASE'][0][0][0][0][ifile][3][0]

    def get_video_indexes(self, annotations, num_files, is_test):
        """Returns the image's video identifier from the annotation's
        data for a set split."""
        video_indexes = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                video_idx = self.get_video_idx_from_annotation_id(annotations, ifile)
                video_indexes.append(video_idx)
        return video_indexes

    def get_video_idx_from_annotation_id(self, annotations, ifile):
        annotations_image = self.get_annotations_list_by_image_id(annotations, ifile)
        if any(annotations_image):
            return int(annotations_image[0]) - 1
        else:
            return -1

    def get_pose_annotations(self, annotations, num_files, is_test):
        """Returns the poses annotations of individual persons from the
        annotation's data for a set split."""
        poses_annotations = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                poses = self.get_poses_from_annotation_id(annotations, ifile, is_test)
                poses_annotations.append(poses)
        return poses_annotations

    def get_poses_from_annotation_id(self, annotations, ifile, is_test):
        """Returns the pose(s) annotations for an image file."""
        poses = []
        pnames = self.get_pose_annotation_names(annotations, ifile)
        if any(pnames):
            if any(self.get_annotations_list_by_image_id(annotations, ifile)):
                poses = self.get_full_pose_annotations(annotations, ifile, pnames)
            else:
                if is_test or self.is_full:
                    poses = self.get_partial_poses_annotations(annotations, ifile, pnames)
        return poses

    def get_pose_annotation_names(self, annotations, ifile):
        """Returns the annotation variable (table) names that categorize the annotated data."""
        try:
            annot_ptr = self.get_annotation_by_file_id(annotations, ifile)
            names = annot_ptr.dtype.names
            if names is not None:
                return names
            else:
                return []
        except IndexError:
            return []

    def get_annotation_by_file_id(self, annotations, ifile):
        return annotations['RELEASE'][0][0][0][0][ifile][1][0]

    def get_full_pose_annotations(self, annotations, ifile, pnames):
        """Returns the full pose's annotations (head bbox, body joints keypoints,
        center coordinates and scale) for a single file of all person detections."""
        poses_annotations = []
        annotations_file = self.get_annotation_by_file_id(annotations, ifile)
        for i in range(len(annotations_file)):
            keypoints = self.get_keypoints(annotations_file, i)
            head_bbox = self.get_head_coordinates(annotations_file, i, pnames)
            scale = self.get_person_scale(annotations_file, i, pnames)
            objpos = self.get_person_center_coordinates(annotations_file, i, pnames)
            poses_annotations.append({
                "keypoints": keypoints,
                "head_bbox": head_bbox,
                "scale": scale,
                "objpos": objpos
            })
        return poses_annotations

    def get_keypoints(self, annotations_file, ipose):
        """Returns the keypoints annotations for a single person detection."""
        keypoints = [[0, 0, 0]] * 16  # [x, y, is_visible]
        keypoints_annotations = self.get_keypoint_annotations(annotations_file, ipose)
        if any(keypoints_annotations):
            vnames = keypoints_annotations.dtype.names
            for i in range(len(keypoints_annotations)):
                x = float(keypoints_annotations[i][vnames.index('x')][0][0])
                y = float(keypoints_annotations[i][vnames.index('y')][0][0])
                idx = int(keypoints_annotations[i][vnames.index('id')][0][0])
                try:
                    is_visible = int(keypoints_annotations[i][vnames.index('is_visible')][0])
                except (ValueError, IndexError):
                    is_visible = -1
                keypoints[idx] = [x, y, is_visible]
        return keypoints

    def get_keypoint_annotations(self, annotations_file, ipose):
        """Returns the keypoint's annotations (x,y,id and is_visible)
        for a single pose detection from the annotations data."""
        try:
            keypoint_annotations = annotations_file[ipose][4][0][0][0][0]
            if isinstance(keypoint_annotations, str):
                return []
            return keypoint_annotations
        except (AttributeError, IndexError):
            return []

    def get_head_coordinates(self, annotations_file, ipose, pnames):
        """Returns the head bounding box coordinates of a person detection."""
        try:
            x1 = annotations_file[ipose][pnames.index('x1')][0][0]
            y1 = annotations_file[ipose][pnames.index('y1')][0][0]
            x2 = annotations_file[ipose][pnames.index('x2')][0][0]
            y2 = annotations_file[ipose][pnames.index('y2')][0][0]
        except ValueError:
            x1, y1, x2, y2 = -1, -1, -1, -1
        return float(x1), float(y1), float(x2), float(y2)

    def get_person_scale(self, annotations_file, ipose, pnames):
        """Returns the scale of a person detection."""
        try:
            scale = annotations_file[ipose][pnames.index('scale')][0][0]
        except (ValueError, IndexError):
            scale = -1
        return float(scale)

    def get_person_center_coordinates(self, annotations_file, ipose, pnames):
        """Returns the center coordinates of a person dection."""
        try:
            objnames = annotations_file[ipose][pnames.index('objpos')][0].dtype.names
            center_x = annotations_file[ipose][pnames.index('objpos')][0][0][objnames.index('x')][0][0]
            center_y = annotations_file[ipose][pnames.index('objpos')][0][0][objnames.index('y')][0][0]
        except (ValueError, IndexError):
            center_x, center_y = -1, -1
        return {"x": float(center_x), "y": float(center_y)}

    def get_partial_poses_annotations(self, annotations, ifile, pnames):
        """Returns partial poses' annotations (center coordinates and scale)
        for a single file of all person detections."""
        poses_annotations = []
        annotations_file = self.get_annotation_by_file_id(annotations, ifile)
        for i in range(len(annotations_file)):
            scale = self.get_person_scale(annotations_file, i, pnames)
            objpos = self.get_person_center_coordinates(annotations_file, i, pnames)
            poses_annotations.append({
                "scale": scale,
                "objpos": objpos
            })
        return poses_annotations

    def get_activities(self, annotations, annotation_size, is_test):
        """Returns the video's activities from the annotation's data
        for a set split."""
        activities = []
        for ifile in range(annotation_size):
            if is_test == self.is_test_annotation(annotations, ifile):
                category_name, activity_name, activity_id = '', '', -1
                if any(self.get_activity_annotation_of_file(annotations, ifile)):
                    category_name = self.get_category_name(annotations, ifile)
                    activity_name = self.get_activity_name(annotations, ifile)
                    activity_id = self.get_activity_id(annotations, ifile)
                activities.append({
                    "category_name": str(category_name),
                    "activity_name": str(activity_name),
                    "activity_id": int(activity_id)
                })
        return activities

    def get_activity_annotation_of_file(self, annotations, ifile):
        """Returns the activity annotations of an image file."""
        return annotations['RELEASE'][0][0][4][ifile][0][0]

    def get_category_name(self, annotations, ifile):
        """Returns the category name of the activity of an image file."""
        return annotations['RELEASE'][0][0][4][ifile][0][0][0]

    def get_activity_name(self, annotations, ifile):
        """Returns the activity name of the activity of an image file."""
        return annotations['RELEASE'][0][0][4][ifile][0][1][0]

    def get_activity_id(self, annotations, ifile):
        """Returns the activity id of the activity of an image file."""
        return annotations['RELEASE'][0][0][4][ifile][0][2][0][0]

    def get_single_persons(self, annotations, annotation_size, is_test):
        """Returns a list of 0 and 1s indicating the presence of a
        single person from the annotation's data for a set split."""
        single_person = []
        for ifile in range(annotation_size):
            if is_test == self.is_test_annotation(annotations, ifile):
                single_person_ = self.get_single_persons_by_file(annotations, ifile)
                single_person.append(single_person_)
        return single_person

    def get_single_persons_by_file(self, annotations, ifile):
        """Returns a list of single persons (0s and 1s) of an image file."""
        annotation_single_person = self.get_single_person_annotations_for_file(annotations, ifile)
        if any(annotation_single_person):
            single_person = []
            for i in range(len(annotation_single_person)):
                is_single = int(annotation_single_person[i][0])
                single_person.append(is_single)
        else:
            single_person = [-1]
        return single_person

    def get_single_person_annotations_for_file(self, annotations, ifile):
        """Returns the single person annotations of an image file."""
        return annotations['RELEASE'][0][0][3][ifile][0]

    def get_video_names(self, annotations):
        """Returns the video names of the dataset."""
        video_names = []
        annotations_videos = self.get_video_annotations(annotations)
        for ivideo in range(len(annotations_videos)):
            video_name = str(annotations_videos[ivideo][0])
            video_names.append(video_name)
        return video_names

    def get_video_annotations(self, annotations):
        """Returns the video names annotations."""
        return annotations['RELEASE'][0][0][5][0]

    def filter_annotations_by_ids(self, annotations, set_image_ids):
        """Returns a subset of the annotations w.r.t. a list of image indices."""
        filtered_ids = self.get_filtered_ids(annotations['image_ids'], set_image_ids)
        return {
            "image_filenames": self.select_items_from_list(annotations['image_filenames'], filtered_ids),
            "frame_sec": self.select_items_from_list(annotations['frame_sec'], filtered_ids),
            "video_idx": self.select_items_from_list(annotations['video_idx'], filtered_ids),
            "pose_annotations": self.select_items_from_list(annotations['pose_annotations'], filtered_ids),
            "activity": self.select_items_from_list(annotations['activity'], filtered_ids),
            "single_person": self.select_items_from_list(annotations['single_person'], filtered_ids),
            "video_names": annotations['video_names']
        }

    def get_filtered_ids(self, image_ids, set_image_ids):
        filtered_ids = []
        for idx in set_image_ids:
            try:
                filtered_ids.append(image_ids.index(idx))
            except ValueError:
                pass
        return filtered_ids

    def select_items_from_list(self, annotations, filtered_ids):
        annotations_filtered = []
        for idx in filtered_ids:
            annotations_filtered.append(annotations[idx])
        return annotations_filtered


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

class CustomBaseField(BaseField):
    """Custom BaseField with common methods for some fields."""

    def get_image_filenames_annotations(self):
        return self.data['image_filenames']

    def get_pose_annotations(self):
        return self.data['pose_annotations']

    def get_single_person_annotations(self):
        return self.data['single_person']

    def get_video_idx_annotations(self):
        return self.data['video_idx']

    def get_video_names_annotations(self):
        return self.data['video_names']

    def get_frame_sec_annotations(self):
        return self.data['frame_sec']

    def get_activity_annotations(self):
        return self.data['activity']


class ImageFilenamesField(CustomBaseField):
    """Image filenames' field metadata process/save class."""

    @display_message_processing('image_filenames')
    def process(self):
        """Processes and saves the image filenames metadata to hdf5."""
        image_filenames, image_filename_ids = self.get_image_filenames()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filenames',
            data=str2ascii(image_filenames),
            dtype=np.uint8,
            fillvalue=0
        )
        return image_filename_ids

    def get_image_filenames(self):
        """Returns a list of image filenames and ids."""
        image_filenames = []
        image_filenames_ids = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, image_filename in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for j, _ in enumerate(image_pose_annotations):
                image_filenames.append(image_filename)
                image_filenames_ids.append(i)
        return image_filenames, image_filenames_ids


class ScalesField(CustomBaseField):
    """Person's scale field metadata process/save class."""

    @display_message_processing('scale')
    def process(self):
        """Processes and saves the person's scale metadata to hdf5."""
        scales = self.get_scales()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='scale',
            data=np.array(scales, dtype=np.float),
            dtype=np.float,
            fillvalue=0
        )

    def get_scales(self):
        """Returns a list of person's scale."""
        scales = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                scales.append(pose['scale'])
        return scales


class ObjposField(CustomBaseField):
    """Person's position field metadata process/save class."""

    @display_message_processing('objpos')
    def process(self):
        """Processes and saves the person's position metadata to hdf5."""
        objpos = self.get_objpos()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='objpos',
            data=np.array(objpos, dtype=np.float),
            dtype=np.float,
            fillvalue=0
        )

    def get_objpos(self):
        """Returns a list of person's position."""
        objpos = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                objpos.append([pose['objpos']['x'], pose['objpos']['y']])
        return objpos


class VideoIdsField(CustomBaseField):
    """Video ids field metadata process/save class."""

    @display_message_processing('video_ids')
    def process(self):
        """Processes and saves the video ids metadata to hdf5."""
        video_ids = self.get_video_ids()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='video_id',
            data=np.array(video_ids, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )
        return video_ids

    def get_video_ids(self):
        """Returns a list of video ids."""
        video_ids = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        video_idx = self.get_video_idx_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                video_ids.append(video_idx[i])
        return video_ids


class VideoNamesField(CustomBaseField):
    """Video names field metadata process/save class."""

    @display_message_processing('video_names')
    def process(self, video_ids):
        """Processes and saves the video names metadata to hdf5."""
        video_names = self.get_video_names(video_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='video_name',
            data=str2ascii(video_names),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_video_names(self, video_ids):
        """Returns a list of video names."""
        video_names = []
        video_names_annotations = self.get_video_names_annotations()
        for video_idx in video_ids:
            if video_idx >= 0:
                video_names.append(video_names_annotations[video_idx])
            else:
                video_names.append('NA')
        return video_names


class FrameSecField(CustomBaseField):
    """Frame sec field metadata process/save class."""

    @display_message_processing('frame_sec')
    def process(self):
        """Processes and saves the frame sec metadata to hdf5."""
        frame_sec = self.get_frame_sec()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='frame_sec',
            data=np.array(frame_sec, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_frame_sec(self):
        """Returns a list of frame sec."""
        frame_sec = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        frame_sec_annotations = self.get_frame_sec_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                frame_sec.append(frame_sec_annotations[i])
        return frame_sec


class KeypointLabelsField(CustomBaseField):
    """Keypoint names field metadata process/save class."""

    @display_message_processing('keypoint_labels')
    def process(self):
        """Processes and saves the keypoint labels metadata to hdf5."""
        keypoint_labels = self.get_keypoint_labels()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoint_labels',
            data=str2ascii(keypoint_labels),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_keypoint_labels(self):
        """Returns a list of keypoint names."""
        keypoints_labels = [
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
        return keypoints_labels


class CategoryNamesField(CustomBaseField):
    """Category names field metadata process/save class."""

    @display_message_processing('category_name')
    def process(self):
        """Processes and saves the category names metadata to hdf5."""
        category_name = self.get_category_name()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='category_name',
            data=str2ascii(category_name),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_category_name(self):
        """Returns a list of category names."""
        category_names = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        activity_annotations = self.get_activity_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                category_names.append(activity_annotations[i]['category_name'])
        return category_names


class ActivityNamesField(CustomBaseField):
    """Activity names field metadata process/save class."""

    @display_message_processing('activity_name')
    def process(self):
        """Processes and saves the activity names metadata to hdf5."""
        activity_name = self.get_activity_name()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='activity_name',
            data=str2ascii(activity_name),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_activity_name(self):
        """Returns a list of activity names."""
        activity_names = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        activity_annotations = self.get_activity_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                activity_names.append(activity_annotations[i]['activity_name'])
        return activity_names


class ActivityIdsField(CustomBaseField):
    """Activity ids field metadata process/save class."""

    @display_message_processing('activity_id')
    def process(self):
        """Processes and saves the activity ids metadata to hdf5."""
        activity_id = self.get_activity_ids()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='activity_id',
            data=np.array(activity_id, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_activity_ids(self):
        """Returns a list of activity ids."""
        activity_ids = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        activity_annotations = self.get_activity_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                activity_ids.append(activity_annotations[i]['activity_id'])
        return activity_ids


class SinglePersonField(CustomBaseField):
    """Single person field metadata process/save class."""

    @display_message_processing('single_person')
    def process(self):
        """Processes and saves the single person metadata to hdf5."""
        single_person = self.get_single_person()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='single_person',
            data=np.array(single_person, dtype=np.uint8),
            dtype=np.uint8,
            fillvalue=-1
        )

    def get_single_person(self):
        """Returns a list of booleans ([0, 1]) indicating single person detections."""
        single_persons = []
        single_person_annotations = self.get_single_person_annotations()
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        activity_annotations = self.get_activity_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for j, pose in enumerate(image_pose_annotations):
                try:
                    val = single_person_annotations[i][j]
                except IndexError:
                    val = -1
                if val == -1:
                    single_persons.append(0)
                else:
                    single_persons.append(1)
        return single_persons


class ObjectFieldNamesField(CustomBaseField):
    """Object field names field metadata process/save class."""

    @display_message_processing('object_fields')
    def process(self):
        """Processes and saves the object fields metadata to hdf5."""
        object_fields = self.get_object_fields()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_fields',
            data=str2ascii(object_fields),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_object_fields(self):
        """Returns a list of object field names."""
        object_fields = [
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
        if self.set_name is not 'test':
            object_fields += ["head_bbox", "keypoints"]
        return object_fields


class ObjectIdsField(CustomBaseField):
    """Object ids field metadata process/save class."""

    @display_message_processing('object_ids')
    def process(self, image_ids, video_ids):
        """Processes and saves the object ids metadata to hdf5."""
        object_ids = self.get_object_ids(image_ids, video_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_ids',
            data=np.array(object_ids, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_object_ids(self, image_ids, video_ids):
        """Returns a list of object ids."""
        object_ids = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        counter = 0
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                obj_ids = [
                    image_ids[counter],  # image_filenames
                    counter,  # scale
                    counter,  # objpos
                    video_ids[counter],  # video_ids
                    video_ids[counter],  # video_name
                    counter,  # frame_sec
                    counter,  # category_name
                    counter,  # activity_name
                    counter,  # activity_id
                    counter,  # single_person
                    counter,  # keypoint_labels
                ]
                if self.set_name is not 'test':
                    obj_ids += [counter, counter]  # [head_bbox, keypoints]
                object_ids.append(obj_ids)
                counter += 1
        return object_ids


class HeadBoundingBoxField(CustomBaseField):
    """Head bounding box field metadata process/save class."""

    @display_message_processing('head_bbox')
    def process(self):
        """Processes and saves the head bbox metadata to hdf5."""
        head_bboxes = self.get_head_bboxes()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='head_bbox',
            data=np.array(head_bboxes, dtype=np.float),
            dtype=np.float,
            fillvalue=-1
        )

    def get_head_bboxes(self):
        """Returns a list of head bboxes."""
        head_bboxes = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                head_bboxes.append(pose['head_bbox'])
        return head_bboxes


class KeypointsField(CustomBaseField):
    """Keypoints field metadata process/save class."""

    @display_message_processing('keypoints')
    def process(self):
        """Processes and saves the keypoints metadata to hdf5."""
        keypoints = self.get_keypoints()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoints',
            data=np.array(keypoints, dtype=np.float),
            dtype=np.float,
            fillvalue=-1
        )

    def get_keypoints(self):
        """Returns a list of keypoints."""
        keypoints = []
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, _ in enumerate(image_fnames):
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                keypoints.append(pose['keypoints'])
        return keypoints


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------

class SinglePersonPerImageList(CustomBaseField):
    """Single persons per image list field metadata process/save class."""

    @display_message_processing('list_single_person_per_image')
    def process(self):
        """Processes and saves the single persons per image metadata to hdf5."""
        single_person_per_image = self.get_list_single_person_per_image()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_single_person_per_image',
            data=np.array(pad_list(single_person_per_image, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_list_single_person_per_image(self):
        """Returns a list of single persons ids per image."""
        single_person_per_image = []
        counter = 0
        single_person_annotations = self.get_single_person_annotations()
        for single_person in single_person_annotations:
            single_persons = []
            for val in single_person:
                if val == 1:
                    single_persons.append(counter)
                counter += 1
            single_person_per_image.append(single_persons)
        return single_person_per_image


class KeypointsPerImageList(CustomBaseField):
    """Keypoints per image list field metadata process/save class."""

    @display_message_processing('list_keypoints_per_image')
    def process(self):
        """Processes and saves the keypoints per image metadata to hdf5."""
        keypoints_per_image = self.get_list_keypoints_per_image()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_keypoints_per_image',
            data=np.array(pad_list(keypoints_per_image, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_list_keypoints_per_image(self):
        """Returns a list of keypoints ids per image."""
        keypoints_per_image = []
        keypoints_empty = [[0, 0, 0]] * 16
        counter = 0
        image_fnames = self.get_image_filenames_annotations()
        pose_annotations = self.get_pose_annotations()
        for i, _ in enumerate(image_fnames):
            keypoints_image = []
            image_pose_annotations = pose_annotations[i]
            for _, pose in enumerate(image_pose_annotations):
                keypoints = pose['keypoints']
                if not keypoints == keypoints_empty:
                    keypoints_image.append(counter)
                counter += 1
            keypoints_per_image.append(keypoints_image)
        return keypoints_per_image


# -----------------------------------------------------------
# Additional tasks
# -----------------------------------------------------------

class KeypointsClean(Keypoints):
    """MPII Keypoints (clean annotations) task class."""

    # metadata filename
    filename_h5 = 'keypoint_clean'
    is_full = False
