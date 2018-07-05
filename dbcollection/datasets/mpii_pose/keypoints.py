"""
MPII Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseTask, BaseField
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_matlab
from dbcollection.utils.hdf5 import hdf5_write_data


class Keypoints(BaseTask):
    """MPII Keypoints preprocessing functions."""

    filename_h5 = 'keypoint'
    is_full = False
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

    def load_annotations(self):
        """
        Load annotations from file and split them to train and test sets.
        """
        annot_filepath = os.path.join(
            self.data_path, 'mpii_human_pose_v1_u12_2', 'mpii_human_pose_v1_u12_1.mat')

        if self.verbose:
            print('\n> Loading annotations file: {}'.format(annot_filepath))

        # load annotations file
        annotations = load_matlab(annot_filepath)

        # total number of files
        nfiles = len(annotations["RELEASE"][0][0][3])

        # progressbar
        if self.verbose:
            print('\n> Parsing data from the annotations...')
            prgbar = progressbar.ProgressBar(max_value=nfiles)

        data = {
            "train": [],
            "test": []
        }

        # cycle all files
        for ifile in range(nfiles):
            if annotations['RELEASE'][0][0][1][0][ifile] == 0:
                set_name = 'test'
            else:
                set_name = 'train'

            # single person
            single_person = [0]
            if any(annotations['RELEASE'][0][0][3][ifile][0]):
                for i in range(len(annotations['RELEASE'][0][0][3][ifile][0])):
                    single_person.append(int(annotations['RELEASE'][0][0][3][ifile][0][i][0]))

            # activity/action id
            act = {"cat_name": '', "act_name": '', "act_id": -1}
            if any(annotations['RELEASE'][0][0][4][ifile][0][0]):
                act = {
                    "cat_name": str(annotations['RELEASE'][0][0][4][ifile][0][0][0]),
                    "act_name": str(annotations['RELEASE'][0][0][4][ifile][0][1][0]),
                    "act_id": int(annotations['RELEASE'][0][0][4][ifile][0][2][0][0])
                }

            # image annots
            image_filename = os.path.join(self.data_path, 'images', str(
                annotations['RELEASE'][0][0][0][0][ifile][0][0][0][0][0]))

            if any(annotations['RELEASE'][0][0][0][0][ifile][3][0]):
                frame_sec = int(annotations['RELEASE'][0][0][0][0][ifile][2][0][0])
                video_idx = int(annotations['RELEASE'][0][0][0][0][ifile][3][0][0])
            else:
                frame_sec, video_idx = -1, -1

            # properties field names ('scale', 'objpos', ...)
            try:
                pnames = annotations['RELEASE'][0][0][0][0][ifile][1][0].dtype.names
            except IndexError:
                data[set_name].append({
                    "image_filename": image_filename,
                    "frame_sec": frame_sec,
                    "video_idx": video_idx,
                    "poses_annotations": [],
                    "activity": act,
                    "single_person": single_person
                })
                continue  # skip rest

            # parse keypoints
            poses_annots = []
            if any(annotations['RELEASE'][0][0][0][0][ifile][3][0]):
                for i in range(len(annotations['RELEASE'][0][0][0][0][ifile][1][0])):
                    try:
                        keypoints = [[0, 0, 0]] * 16  # [x, y, is_visible]
                        annot = annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0]
                        vnames = annot.dtype.names
                        for j in range(len(annot)):
                            x = float(annot[j][vnames.index('x')][0][0])
                            y = float(annot[j][vnames.index('y')][0][0])
                            idx = int(annot[j][vnames.index('id')][0][0])

                            try:
                                is_visible = int(annot[j][vnames.index('is_visible')][0])
                            except (ValueError, IndexError):
                                is_visible = -1

                            try:
                                keypoints[idx] = [x, y, is_visible]
                            except IndexError as k:
                                if set_name == 'test' or self.is_full:
                                    print('Error: ', str(k))
                                    keypoints[idx] = [0, 0, 0]
                                else:
                                    continue  # skip this annotation
                    except (AttributeError, IndexError):
                        keypoints = [[0, 0, 0]] * 16  # [x, y, is_visible]

                    try:
                        x1 = float(annotations['RELEASE'][0][0][0][0][ifile]
                                   [1][0][i][pnames.index('x1')][0][0])
                        y1 = float(annotations['RELEASE'][0][0][0][0][ifile]
                                   [1][0][i][pnames.index('y1')][0][0])
                        x2 = float(annotations['RELEASE'][0][0][0][0][ifile]
                                   [1][0][i][pnames.index('x2')][0][0])
                        y2 = float(annotations['RELEASE'][0][0][0][0][ifile]
                                   [1][0][i][pnames.index('y2')][0][0])
                    except ValueError:
                        if set_name == 'test' or self.is_full:
                            x1, y1, x2, y2 = -1, -1, -1, -1
                        else:
                            continue  # skip this annotation

                    try:
                        annot_ptr = annotations['RELEASE'][0][0][0][0][ifile][1][0]
                        objnames = annot_ptr[i][pnames.index('objpos')][0].dtype.names
                        # objnames = annotations['RELEASE'][0][0][0][0][ifile][1][0][i]
                        # [pnames.index('objpos')][0].dtype.names
                        scale = float(annotations['RELEASE'][0][0][0][0]
                                      [ifile][1][0][i][pnames.index('scale')][0][0])
                        objpos = {
                            "x": float(annotations['RELEASE'][0][0][0][0]
                                       [ifile][1][0][i][pnames.index('objpos')][0][0]
                                       [objnames.index('x')][0][0]),
                            "y": float(annotations['RELEASE'][0][0][0][0]
                                       [ifile][1][0][i][pnames.index('objpos')][0][0]
                                       [objnames.index('y')][0][0])
                        }
                    except (ValueError, IndexError):
                        if set_name == 'test' or self.is_full:
                            scale = -1
                            objpos = {"x": -1, "y": -1}
                        else:
                            continue  # skip this annotation

                    poses_annots.append({
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                        "keypoints": keypoints,
                        "scale": scale,
                        "objpos": objpos
                    })
            else:
                if set_name == 'test' or self.is_full:
                    for i in range(len(annotations['RELEASE'][0][0][0][0][ifile][1][0])):
                        try:
                            annot_ptr = annotations['RELEASE'][0][0][0][0][ifile][1][0]
                            objnames = annot_ptr[i][pnames.index('objpos')][0].dtype.names
                            # objnames = annotations['RELEASE'][0][0][0][0][ifile][1][0][i]
                            # [pnames.index('objpos')][0].dtype.names
                            scale = float(annotations['RELEASE'][0][0][0][0]
                                          [ifile][1][0][i][pnames.index('scale')][0][0])
                            objpos = {
                                "x": float(annotations['RELEASE'][0][0][0][0]
                                           [ifile][1][0][i][pnames.index('objpos')][0][0]
                                           [objnames.index('x')][0][0]),
                                "y": float(annotations['RELEASE'][0][0][0][0]
                                           [ifile][1][0][i][pnames.index('objpos')][0][0]
                                           [objnames.index('y')][0][0])
                            }
                        except (IndexError, ValueError, AttributeError):
                            scale = -1
                            objpos = {"x": -1, "y": -1}

                        poses_annots.append({
                            "scale": scale,
                            "objpos": objpos
                        })
                else:
                    continue  # skip this annotation

            # add fields to data
            data[set_name].append({
                "image_filename": image_filename,
                "frame_sec": frame_sec,
                "video_idx": video_idx,
                "poses_annotations": poses_annots,
                "activity": act,
                "single_person": single_person
            })

            # update progressbar
            if self.verbose:
                prgbar.update(ifile)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        # fetch video ids
        videonames = []
        for ivideo in range(len(annotations['RELEASE'][0][0][5][0])):
            videonames.append(str(annotations['RELEASE'][0][0][5][0][ivideo][0]))

        return data, videonames

    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        # load annotations
        annotations, videonames = self.load_annotations()

        for set_name in annotations:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)

            yield {set_name: [annotations[set_name], videonames]}

    def add_data_to_source(self, hdf5_handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        # split list
        data_, videonames = data

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        hdf5_handler["videonames"] = str2ascii(videonames)
        hdf5_handler["keypoint_names"] = str2ascii(self.keypoints_labels)

        for i, annot in enumerate(data_):
            file_grp = hdf5_handler.create_group(str(i))
            file_grp['image_filename'] = str2ascii(annot["image_filename"])
            file_grp['frame_sec'] = np.array(annot["frame_sec"], dtype=np.int32)
            file_grp['video_idx'] = np.array(annot["video_idx"], dtype=np.int32)
            file_grp['single_person_id'] = np.array(annot["single_person"], dtype=np.uint8)

            activity_grp = file_grp.create_group("activity")
            activity_grp['category_name'] = str2ascii(annot["activity"]["cat_name"])
            activity_grp['activity_name'] = str2ascii(annot["activity"]["act_name"])
            activity_grp['activity_id'] = np.array(annot["activity"]["act_id"], dtype=np.int32)

            if any(annot["poses_annotations"]):
                pose_annot_grp = file_grp.create_group("pose_annotations")
                for j in range(len(annot["poses_annotations"])):
                    pose_grp = pose_annot_grp.create_group(str(j))
                    pose_grp["scale"] = np.array(
                        annot["poses_annotations"][j]["scale"], dtype=np.float)
                    pose_grp["objpos/x"] = np.array(annot["poses_annotations"]
                                                    [j]["objpos"]["x"], dtype=np.float)
                    pose_grp["objpos/y"] = np.array(annot["poses_annotations"]
                                                    [j]["objpos"]["y"], dtype=np.float)

                    if "x1" in annot["poses_annotations"][j]:
                        pose_grp["x1"] = np.array(annot["poses_annotations"]
                                                  [j]["x1"], dtype=np.float)
                        pose_grp["y1"] = np.array(annot["poses_annotations"]
                                                  [j]["y1"], dtype=np.float)
                        pose_grp["x2"] = np.array(annot["poses_annotations"]
                                                  [j]["x2"], dtype=np.float)
                        pose_grp["y2"] = np.array(annot["poses_annotations"]
                                                  [j]["y2"], dtype=np.float)
                        pose_grp["keypoints"] = np.array(
                            annot["poses_annotations"][j]["keypoints"], dtype=np.float)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

    def add_data_to_default(self, hdf5_handler, data, set_name):
        """
        Add data of a set to the default group.
        """
        # split list
        data_, videonames = data

        if set_name == 'test':
            is_train = False
        else:
            is_train = True

        image_filenames = []
        frame_sec = []
        video_idx = []
        # single_person_id_list = []
        category_name, activity_name, activity_id = [], [], []
        scale = []
        objpos = []  # [x, y]
        head_bbox = []
        keypoints = []

        object_id = []

        if is_train:
            object_fields = ["image_filenames", "scale", "objpos",
                             "head_bbox", "keypoints", "frame_sec",
                             "video_idx"]
        else:
            object_fields = ["image_filenames", "scale", "objpos"]

        # adicionar listas
        list_object_ids_per_image = []
        list_single_person_per_image = []
        list_keypoints_per_image = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        obj_per_img_counter = 0
        for i, annot in enumerate(data_):
            image_filenames.append(annot["image_filename"])

            if is_train:
                frame_sec.append(annot["frame_sec"])
                video_idx.append(annot["video_idx"])
                category_name.append(annot["activity"]["cat_name"])
                activity_name.append(annot["activity"]["act_name"])
                activity_id.append(annot["activity"]["act_id"])

            objs_per_image = []
            keypoints_per_image = []
            single_person_per_image = []
            if not any(annot["poses_annotations"]):
                if is_train:
                    if self.is_full:
                        object_id.append([i, -1, -1, -1, -1, i, i])
                        objs_per_image.append(obj_per_img_counter)  # add object_id to the list
                        obj_per_img_counter += 1  # update counter
                else:
                    object_id.append([i, -1, -1])
                    objs_per_image.append(obj_per_img_counter)  # add object_id to the list
                    obj_per_img_counter += 1  # update counter
            else:
                for j, pose_annot in enumerate(annot["poses_annotations"]):
                    scale.append(pose_annot["scale"])
                    objpos.append([pose_annot["objpos"]["x"],
                                   pose_annot["objpos"]["y"]])

                    if j + 1 in annot["single_person"]:
                        single_person_per_image.append(obj_per_img_counter)

                    if is_train:
                        head_bbox.append([pose_annot["x1"],
                                          pose_annot["y1"],
                                          pose_annot["x2"],
                                          pose_annot["y2"]])

                        keypoints.append(pose_annot["keypoints"])

                        object_id.append([i, obj_per_img_counter, obj_per_img_counter,
                                          obj_per_img_counter, obj_per_img_counter, i, i])

                        # add object_id to the keypoint list
                        keypoints_per_image.append(obj_per_img_counter)
                    else:
                        object_id.append([i, obj_per_img_counter, obj_per_img_counter])

                    # add object_id to the list
                    objs_per_image.append(obj_per_img_counter)

                    # update counter
                    obj_per_img_counter += 1

            list_object_ids_per_image.append(objs_per_image)
            list_single_person_per_image.append(single_person_per_image)
            list_keypoints_per_image.append(keypoints_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        hdf5_write_data(hdf5_handler, 'image_filenames',
                        str2ascii(image_filenames), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'scale',
                        np.array(scale, dtype=np.float),
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'objpos',
                        np.array(objpos, dtype=np.float),
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        np.array(object_id, dtype=np.int32),
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        str2ascii(object_fields), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'video_names',
                        str2ascii(videonames), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'keypoint_names',
                        str2ascii(self.keypoints_labels), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'list_object_ids_per_image',
                        np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_single_person_per_image',
                        np.array(pad_list(list_single_person_per_image, -1), dtype=np.int32),
                        fillvalue=-1)

        if is_train:
            hdf5_write_data(hdf5_handler, 'frame_sec',
                            np.array(frame_sec, dtype=np.int32),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'video_idx',
                            np.array(video_idx, dtype=np.int32),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'category_name',
                            str2ascii(category_name), dtype=np.uint8,
                            fillvalue=0)
            hdf5_write_data(hdf5_handler, 'activity_name',
                            str2ascii(activity_name), dtype=np.uint8,
                            fillvalue=0)
            hdf5_write_data(hdf5_handler, 'activity_id',
                            np.array(activity_id, dtype=np.int32),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'head_bbox',
                            np.array(head_bbox, dtype=np.float),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'keypoints',
                            np.array(keypoints, dtype=np.float),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'list_keypoints_per_image',
                            np.array(pad_list(list_keypoints_per_image, -1), dtype=np.int32),
                            fillvalue=-1)


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, keypoints_labels, is_full, data_path, cache_path, verbose):
        self.keypoints_labels = keypoints_labels
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
        from .train_val_ids import train_images_ids
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
        from .train_val_ids import val_images_ids
        annotations = self.load_annotations_set(is_test=False)
        return self.filter_annotations_by_ids(annotations, val_images_ids)

    def load_test_data(self):
        """Loads the test set annotation data from disk
        and returns it as a dictionary."""
        return self.load_annotations_set(is_test=True)

    def load_annotations_set(self, is_test):
        """Loads the annotation's data for the train + test splits."""
        annotations = self.load_annotation_data_from_disk()
        nfiles = self.get_num_files(annotations)
        return {
            "image_filenames": self.get_image_filenames(annotations, nfiles, is_test),
            "frame_sec": self.get_frame_sec(annotations, nfiles, is_test),
            "video_idx": self.get_video_indexes(annotations, nfiles, is_test),
            "pose_annotations": self.get_pose_annotations(annotations, nfiles, is_test),
            "activity": self.get_activities(annotations, nfiles, is_test),
            "single_person": self.get_single_persons(annotations, nfiles),
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
            return int(annotations_image[0])
        else:
            return -1

    def get_pose_annotations(self, annotations, num_files, is_test):
        """Returns the poses annotations of individual persons from the
        annotation's data for a set split."""
        poses_annotations = []
        for ifile in range(num_files):
            if is_test == self.is_test_annotation(annotations, ifile):
                poses = self.get_poses_from_annotation_id(annotations, ifile, is_test)
                if any(poses):
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
            return annot_ptr.dtype.names
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
            return annotations_file[ipose][4][0][0][0][0]
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

    def get_single_persons(self, annotations, annotation_size):
        """Returns a list of 0 and 1s indicating the presence of a
        single person from the annotation's data for a set split."""
        single_person = []
        for ifile in range(annotation_size):
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
        videonames = []
        annotations_videos = self.get_video_annotations(annotations)
        for ivideo in range(len(annotations_videos)):
            video_name = str(annotations_videos[ivideo][0])
            videonames.append(video_name)

    def get_video_annotations(self, annotations):
        """Returns the video names annotations."""
        return annotations['RELEASE'][0][0][5][0]

    def filter_annotations_by_ids(self, annotations, image_ids):
        """Returns a subset of the annotations w.r.t. a list of image indices."""
        annotations_subset = []
        for ifile in image_ids:
            annotations_subset.append(annotations[ifile])
        return annotations_subset


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------

# -----------------------------------------------------------
# Additional tasks
# -----------------------------------------------------------

class KeypointsFull(Keypoints):
    """MPII Keypoints (FULL original annotations) task class."""

    # metadata filename
    filename_h5 = 'keypoint_full'
    is_full = True
