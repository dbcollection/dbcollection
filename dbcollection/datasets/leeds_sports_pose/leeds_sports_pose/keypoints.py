"""
LSP Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseTask
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.file_load import load_matlab
from dbcollection.utils.hdf5 import hdf5_write_data


class Keypoints(BaseTask):
    """LSP Keypoints preprocessing functions."""

    # metadata filename
    filename_h5 = 'keypoint'

    keypoints_labels = [
        'Right ankle',     # -- 1
        'Right knee',      # -- 2
        'Right hip',       # -- 3
        'Left hip',        # -- 4
        'Left knee',       # -- 5
        'Left ankle',      # -- 6
        'Right wrist',     # -- 7
        'Right elbow',     # -- 8
        'Right shoulder',  # -- 9
        'Left shoulder',   # -- 10
        'Left elbow',      # -- 11
        'Left wrist',      # -- 12
        'Neck',            # -- 13
        'Head top'         # -- 14
    ]

    def fetch_annotations_images_paths(self):
        """
        Returns the paths of the annotation file and images folder.
        """
        annot_filepath = os.path.join(self.data_path, 'lsp_dataset', 'joints.mat')
        images_dir = os.path.join(self.data_path, 'lsp_dataset', 'images')

        return annot_filepath, images_dir

    def load_annotations(self):
        """
        Load annotations from file and split them to train and test sets.
        """
        annot_filepath, images_dir = self.fetch_annotations_images_paths()

        # load annotations file
        annotations = load_matlab(annot_filepath)

        data = {
            "train": [],
            "test": []
        }

        image_filenames = os.listdir(images_dir)
        image_filenames.sort()

        for i in range(0, 2000):
            if i >= 1000:
                set_name = 'test'
            else:
                set_name = 'train'

            filename = os.path.join(self.data_path, 'images', image_filenames[i])

            joints = []
            for j in range(0, 14):
                joints.append([annotations['joints'][0][j][i],  # x
                               annotations['joints'][1][j][i],  # y
                               annotations['joints'][2][j][i]])  # is_visible (0 - visible,
                #             1 - hidden)

            data[set_name].append({"filename": filename, "joints": joints})

        return data

    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        # load annotations
        annotations = self.load_annotations()
        for set_name in annotations:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)
            yield {set_name: annotations[set_name]}

    def add_data_to_source(self, hdf5_handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        keypoint_names = str2ascii(self.keypoints_labels)

        for i, annot in enumerate(data):
            file_grp = hdf5_handler.create_group(str(i))
            file_grp['image_filename'] = str2ascii(annot["filename"])
            file_grp['keypoints'] = np.array(annot["joints"], dtype=np.float)
            file_grp['keypoint_names'] = keypoint_names

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
        image_filenames = []
        keypoints = []
        object_id = []
        object_fields = ["image_filenames", "keypoints"]

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, annot in enumerate(data):
            image_filenames.append(annot["filename"])
            keypoints.append(annot["joints"])

            object_id.append([i, i])

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        hdf5_write_data(hdf5_handler, 'image_filenames',
                        str2ascii(image_filenames),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'keypoints',
                        np.array(keypoints, dtype=np.float),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'keypoint_names',
                        str2ascii(self.keypoints_labels),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        np.array(object_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        str2ascii(object_fields),
                        dtype=np.uint8, fillvalue=0)


class KeypointsOriginal(Keypoints):
    """LSP Keypoints full images size (no source group) task class."""

    # metadata filename
    filename_h5 = 'keypoint_original'

    def fetch_annotations_images_paths(self):
        """
        Returns the paths of the annotation file and images folder.
        """
        annot_filepath = os.path.join(self.data_path, 'joints.mat')
        images_dir = os.path.join(self.data_path, 'images')

        return annot_filepath, images_dir
