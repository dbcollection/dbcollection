"""
FLIC Keypoints process functions.
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
    """FLIC Keypoints preprocessing functions."""

    # metadata filename
    filename_h5 = 'keypoint'

    keypoints_labels = [
        'Left_Shoulder',   # -- 1
        'Left_Elbow',      # -- 2
        'Left_Wrist',      # -- 3
        'Right_Shoulder',  # -- 4
        'Right_Elbow',     # -- 5
        'Right_Wrist',     # -- 6
        'Left_Hip',        # -- 7
        'Right_Hip',       # -- 8
        'Left_Eye',        # -- 9
        'Right_Eye',       # -- 10
        'Nose'             # -- 11
    ]

    def load_annotations(self):
        """
        Load annotations from file and split them to train and test sets.
        """
        annot_filepath = os.path.join(self.data_path, 'FLIC', 'examples.mat')

        # load annotations file
        annotations = load_matlab(annot_filepath)

        data = {
            "train": [],
            "test": []
        }

        for i, annot in enumerate(annotations['examples'][0]):
            if annot[-1][0][0] == 0:
                set_name = 'train'
            else:
                set_name = 'test'

            width, height, _ = annot[4][0].tolist()
            moviename = annot[1][0]
            filename = os.path.join(self.data_path, 'FLIC', 'images', annot[3][0])
            torso_box = annot[6][0].squeeze().tolist(),  # [x1,y1,x2,y2]
            parts = [
                # [x, y, is_visible]
                [annot[2][0][0], annot[2][1][0], 1],  # -- 1, Left_Shoulder
                [annot[2][0][1], annot[2][1][1], 1],  # -- 2, Left_Elbow
                [annot[2][0][2], annot[2][1][2], 1],  # -- 3, Left_Wrist
                [annot[2][0][3], annot[2][1][3], 1],  # -- 4, Right_Shoulder
                [annot[2][0][4], annot[2][1][4], 1],  # -- 5, Right_Elbow
                [annot[2][0][5], annot[2][1][5], 1],  # -- 6, Right_Wrist
                [annot[2][0][6], annot[2][1][6], 1],  # -- 7, Left_Hip
                [annot[2][0][9], annot[2][1][9], 1],  # -- 8, Right_Hip
                [annot[2][0][12], annot[2][1][12], 1],  # -- 9, Left_Eye
                [annot[2][0][13], annot[2][1][13], 1],  # -- 10, Right_Eye
                [annot[2][0][16], annot[2][1][16], 1]  # -- 11, Nose
            ]

            data[set_name].append({
                "filename": filename,
                "width": width,
                "height": height,
                "moviename": moviename,
                "torso_box": torso_box,
                "parts": parts
            })

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
            file_grp['moviename'] = str2ascii(annot["moviename"])
            file_grp['width'] = np.array(annot["width"], dtype=np.int32)
            file_grp['height'] = np.array(annot["height"], dtype=np.int32)
            file_grp['keypoint_names'] = keypoint_names
            file_grp['torso_box'] = np.array(annot["torso_box"], dtype=np.float)
            file_grp['keypoints'] = np.array(annot["parts"], dtype=np.float)

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
        width = []
        height = []
        movienames = []
        torso_boxes = []
        keypoints = []
        object_id = []

        object_fields = ["image_filenames", "torso_boxes",
                         "keypoints", "width", "height"]

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, annot in enumerate(data):
            image_filenames.append(annot["filename"])
            movienames.append(annot["moviename"])
            width.append(annot["width"])
            height.append(annot["height"])
            torso_boxes.append(annot["torso_box"])
            keypoints.append(annot["parts"])

            object_id.append([i, i, i, i, i])

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        hdf5_write_data(hdf5_handler, 'image_filenames',
                        str2ascii(image_filenames), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'movienames',
                        str2ascii(movienames),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'width',
                        np.array(width, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'height',
                        np.array(height, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'torso_boxes',
                        np.array(torso_boxes, dtype=np.float).squeeze(),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'keypoints',
                        np.array(keypoints, dtype=np.float),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'keypoint_names',
                        str2ascii(self.keypoints_labels),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        str2ascii(object_fields),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        np.array(object_id, dtype=np.int32),
                        fillvalue=-1)
