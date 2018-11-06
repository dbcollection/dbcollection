"""
FLIC Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseField, BaseTask, BaseMetadataField
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.file_load import load_matlab


class Keypoints(BaseTask):
    """FLIC Keypoints preprocessing functions."""

    version = '1.0.0'

    # metadata filename
    filename_h5 = 'keypoint'

    def load_data(self):
        """
        Loads data from annotation files.
        """
        loader = DatasetAnnotationLoader(
            data_files=self.data_files,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_train_data()}
        yield {"test": loader.load_test_data()}

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
        configs = {
            "data": data,
            "set_name": set_name,
            "hdf5_manager": self.hdf5_manager,
            "verbose": self.verbose
        }

        # Fields
        if self.verbose:
            print('\n==> Setting up the data fields:')
        ImageFilenameField(**configs).process()
        MoviesField(**configs).process()
        WidthField(**configs).process()
        HeightField(**configs).process()
        TorsoBoxesField(**configs).process()
        KeypointsField(**configs).process()
        KeypointLabelsField(**configs).process()

        # Fields' metadata info
        MetadataField(**configs).process()


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, data_files, data_path, cache_path, verbose):
        self.data_files = data_files
        self.data_path = data_path
        self.cache_path = cache_path
        self.verbose = verbose

    def load_train_data(self):
        """Loads the train set annotation data from disk
        and returns it as a dictionary."""
        return self.load_data_set(is_test=False)

    def load_test_data(self):
        """Loads the test set annotation data from disk
        and returns it as a dictionary."""
        return self.load_data_set(is_test=True)

    def load_data_set(self, is_test):
        """
        Load annotations from file and split them to train and test sets.
        """
        annotations = self.load_annotations()

        data = []
        for i, annot in enumerate(annotations['examples'][0]):
            if self.use_sample(annot, is_test):
                width, height, _ = annot[4][0].tolist()
                moviename = annot[1][0]
                filename = os.path.join(self.data_path, 'FLIC', 'images', annot[3][0])
                torso_box = annot[6][0].squeeze().tolist(),  # [x1,y1,x2,y2]
                keypoints = [
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

                data.append({
                    "filename": filename,
                    "width": width,
                    "height": height,
                    "moviename": moviename,
                    "torso_box": torso_box,
                    "keypoints": keypoints
                })
        return data

    def load_annotations(self):
        annot_filepath = os.path.join(self.data_path, 'FLIC', 'examples.mat')
        annotations = load_matlab(annot_filepath)
        return annotations

    def use_sample(self, annotation, is_test):
        if is_test:
            if annot[-1][0][0] == 0:
                use_sample = False
            else:
                use_sample = True
        else:
            if annot[-1][0][0] == 0:
                use_sample = True
            else:
                use_sample = False
        return use_sample


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

class CustomBaseField(BaseField):
    """Custom Base Field."""

    def get_field_data(self, field):
        return [annotation[field] for annotation in self.data]


class ImageFilenameField(CustomBaseField):
    """Image filenames data field process/save class."""

    @display_message_processing('image_filename')
    def process(self):
        """Processes and saves the image filenames metadata to hdf5."""
        image_filenames = self.get_field_data("filename")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filenames',
            data=str2ascii(image_filenames),
            dtype=np.uint8,
            fillvalue=0
        )


class MoviesField(CustomBaseField):
    """Movies data field process/save class."""

    @display_message_processing('movies')
    def process(self):
        """Processes and saves the movies metadata to hdf5."""
        movies = self.get_field_data("moviename")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='movies',
            data=str2ascii(movies),
            dtype=np.uint8,
            fillvalue=0
        )


class WidthField(CustomBaseField):
    """Image width data field process/save class."""

    @display_message_processing('width')
    def process(self):
        """Processes and saves the width metadata to hdf5."""
        width = self.get_field_data("width")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='width',
            data=np.array(width, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )


class HeightField(CustomBaseField):
    """Image height data field process/save class."""

    @display_message_processing('height')
    def process(self):
        """Processes and saves the height metadata to hdf5."""
        height = self.get_field_data("height")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='height',
            data=np.array(height, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )


class TorsoBoxesField(CustomBaseField):
    """Torso boxes data field process/save class."""

    @display_message_processing('torso_boxes')
    def process(self):
        """Processes and saves the torso boxes metadata to hdf5."""
        torso_boxes = self.get_field_data("torso_boxes")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='torso_boxes',
            data=np.array(torso_boxes, dtype=np.float),
            dtype=np.float,
            fillvalue=-1
        )


class KeypointsField(CustomBaseField):
    """Keypoints data field process/save class."""

    @display_message_processing('keypoints')
    def process(self):
        """Processes and saves the keypoints metadata to hdf5."""
        keypoints = self.get_field_data("keypoints")
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoints',
            data=np.array(keypoints, dtype=np.float),
            dtype=np.float,
            fillvalue=-1
        )


class KeypointLabelsField(CustomBaseField):
    """Keypoint names data field process/save class."""

    @display_message_processing('keypoint_labels')
    def process(self):
        """Processes and saves the keypoint names metadata to hdf5."""
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
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoint_labels',
            data=str2ascii(keypoints_labels),
            dtype=np.uint8,
            fillvalue=0
        )


class MetadataField(BaseMetadataField):
    """Metadata field class."""

    fields = [
        {"name": 'image_filenames', "type": 'filename'},
        {"name": 'movies', "type": 'string'},
        {"name": 'width', "type": 'number'},
        {"name": 'height', "type": 'number'},
        {"name": 'torso_boxes', "type": 'number'},
        {"name": 'keypoints', "type": 'number'}
    ]
