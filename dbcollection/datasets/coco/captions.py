"""
COCO Captions 2015/2016 process functions.
"""


from __future__ import print_function, division

import os
import numpy as np
import pandas as pd

from dbcollection.datasets import BaseField, BaseMetadataField, BaseTask
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_json

from .process_test import process_save_test_metadata_to_hdf5


class Caption2015(BaseTask):
    """COCO Captions (2015) preprocessing functions."""

    # metadata filename
    filename_h5 = 'caption_2015'

    annotations = {
        "train": {
            "images_dir": 'train2014',
            "file_name": 'captions_train2014.json',
        },
        "val": {
            "images_dir": 'val2014',
            "file_name": 'captions_val2014.json'
        },
        "test": {
            "images_dir": 'test2014',
            "file_name": 'image_info_test2014.json'
        }
    }

    def load_data(self):
        """
        Fetches the train/test data.
        """
        loader = DatasetAnnotationLoader(
            annotations=self.annotations,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_data_set('train')}
        yield {"val": loader.load_data_set('val')}
        yield {"test": loader.load_data_set('test')}

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
        if set_name in ['test', 'test_dev']:
            self.process_set_metadata_test(data, set_name)
        else:
            self.process_set_metadata_train_val(data, set_name)

    def process_set_metadata_test(self, data, set_name):
        """Saves the metadata of the test sets."""
        process_save_test_metadata_to_hdf5(data, set_name, self.hdf5_manager, self.verbose)

    def process_set_metadata_train_val(self, data, set_name):
        """Saves the metadata of the train and validation sets."""
        kwargs = {
            "data": data,
            "set_name": set_name,
            "hdf5_manager": self.hdf5_manager,
            "verbose": self.verbose
        }

        # Fields
        if self.verbose:
            print('\n==> Setting up the data fields:')
        # 'id',
        IdField(**kwargs).process()
        ImageIdField(**kwargs).process()
        CaptionField(**kwargs).process()
        CocoURLField(**kwargs).process()
        ImageFilenameField(**kwargs).process()
        ImageHeightField(**kwargs).process()
        ImageWidthField(**kwargs).process()

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        CaptionsPerImageList(**kwargs).process()

        # Fields' metadata info
        MetadataField(**kwargs).process()


class DatasetAnnotationLoader:
    """Annotation's data loader for the coco captions dataset (train/test)."""

    def __init__(self, annotations, data_path, cache_path, verbose):
        self.annotations = annotations
        self.data_path = data_path
        self.cache_path = cache_path
        self.verbose = verbose

    def load_data_set(self, set_name):
        """Loads the data from disk."""
        assert set_name
        filename = os.path.join(self.data_path, 'annotations', self.annotations[set_name]['file_name'])
        image_dir_path = self.annotations[set_name]['images_dir']
        if self.verbose:
            print("\n[Set: {}] Loading file from disk: {}".format(set_name, filename))
        data = load_json(filename)
        images = self.get_dataframe_images(data, image_dir_path)
        if set_name in ['test', 'test_dev']:
            categories = self.get_dataframe_categories(data)
            return {
                "images": images.reset_index(),
                "categories": categories.reset_index()
            }
        else:
            annotations = self.get_dataframe_annotations(data)
            df = annotations.join(images, on='image_id')
            return {
                "full_data": df.reset_index()
            }

    def get_dataframe_categories(self, data):
        categories = pd.DataFrame(data=data['categories'])
        categories = categories.set_index('id')
        categories = categories.sort_index(ascending=True)
        return categories

    def get_dataframe_images(self, data, image_dir_path):
        images = pd.DataFrame(data=data["images"])
        images = images.set_index('id')
        images = images.sort_index(ascending=True)
        # prefix the directory to the image filename
        images["file_name"] = images["file_name"].apply(lambda x: "{}/{}".format(image_dir_path, x))
        return images

    def get_dataframe_annotations(self, data):
        annotations = pd.DataFrame(data=data['annotations'])
        annotations = annotations.set_index('id')
        annotations = annotations.sort_index(ascending=True)
        return annotations


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

class IdField(BaseField):
    """Id field metadata process/save class."""

    @display_message_processing('id')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='id',
            data=self.data['full_data']['id'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class ImageIdField(BaseField):
    """Image id field metadata process/save class."""

    @display_message_processing('image_id')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_id',
            data=self.data['full_data']['image_id'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class CaptionField(BaseField):
    """Captions field metadata process/save class."""

    @display_message_processing('caption')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='caption',
            data=str2ascii(list(self.data['full_data']['caption'].values)),
            dtype=np.int32,
            fillvalue=-1
        )


class CocoURLField(BaseField):
    """Coco URL link field metadata process/save class."""

    @display_message_processing('coco_url')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='coco_url',
            data=str2ascii(list(self.data['full_data']['coco_url'].values)),
            dtype=np.uint8,
            fillvalue=0
        )


class ImageFilenameField(BaseField):
    """Image file name field metadata process/save class."""

    @display_message_processing('image_filename')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filename',
            data=str2ascii(list(self.data['full_data']['file_name'].values)),
            dtype=np.uint8,
            fillvalue=0
        )


class ImageHeightField(BaseField):
    """Image height field metadata process/save class."""

    @display_message_processing('height')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='height',
            data=self.data['full_data']['height'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class ImageWidthField(BaseField):
    """Image width field metadata process/save class."""

    @display_message_processing('width')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='width',
            data=self.data['full_data']['width'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class MetadataField(BaseMetadataField):
    """Metadata field class."""

    fields = [
        {"name": 'id', "type": 'number'},
        {"name": 'image_id', "type": 'number'},
        {"name": 'caption', "type": 'string'},
        {"name": 'coco_url', "type": 'string'},
        {"name": 'image_filename', "type": 'string'},
        {"name": 'height', "type": 'number'},
        {"name": 'width', "type": 'number'},
        {"name": 'list_captions_per_image', "type": 'list'}
    ]


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------

class CaptionsPerImageList(BaseField):
    """Captions per image list metadata process/save class."""

    @display_message_processing('captions per image list')
    def process(self):
        captions_per_image = self.get_captions_per_image_id()
        captions_per_image_array = self.convert_list_to_array(captions_per_image_array)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_captions_per_image',
            data=captions_per_image_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_captions_per_image_id(self):
        captions_per_image_id = self.data['full_data'].groupby('image_id')['id'].apply(list)
        return list(captions_per_image_id)

    def convert_list_to_array(self, list_ids, dtype=np.int32):
        """Pads a list of listsand converts it into a numpy.ndarray."""
        padded_list = pad_list(list_ids, val=-1)
        return np.array(padded_list, dtype=dtype)


# ---------------------------------------------------------
#  Captions 2016
# ---------------------------------------------------------

class Caption2016(Caption2015):
    """COCO Caption (2016) preprocessing functions."""

    filename_h5 = 'caption_2016'

    annotations = {
        "train": {
            "images_dir": 'train2014',
            "file_name": 'captions_train2014.json',
        },
        "val": {
            "images_dir": 'val2014',
            "file_name": 'captions_val2014.json'
        },
        "test": {
            "images_dir": 'test2014',
            "file_name": 'image_info_test2015.json'
        },
        "test_dev": {
            "images_dir": 'train2014',
            "file_name": 'image_info_test-dev2015.json',
        }
    }

    def load_data(self):
        """
        Fetches the train/test data.
        """
        loader = DatasetAnnotationLoader(
            annotations=self.annotations,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_data_set('train')}
        yield {"val": loader.load_data_set('val')}
        yield {"test": loader.load_data_set('test')}
        yield {"test_dev": loader.load_data_set('test_dev')}
