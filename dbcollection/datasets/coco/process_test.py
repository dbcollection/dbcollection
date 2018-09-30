"""
Process and save the test set metadata to disk.
"""


from __future__ import print_function, division
import numpy as np
from dbcollection.datasets import BaseField, BaseColumnField
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


def process_save_test_metadata_to_hdf5(data, set_name, hdf5_manager, verbose=True):
    """
    Saves the metadata of a test set.
    """
    kwargs = {
        "data": data,
        "set_name": set_name,
        "hdf5_manager": hdf5_manager,
        "verbose": verbose
    }

    # Fields
    if verbose:
        print('\n==> Setting up the data fields:')
    ImageIdField(**kwargs).process()
    CategoryIdField(**kwargs).process()
    CategoryField(**kwargs).process()
    SuperCategoryField(**kwargs).process()
    CocoURLField(**kwargs).process()
    ImageFilenameField(**kwargs).process()
    ImageHeightField(**kwargs).process()
    ImageWidthField(**kwargs).process()

    # Column field
    ColumnField(**kwargs).process()


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

class CategoryIdField(BaseField):
    """Category id field metadata process/save class."""

    @display_message_processing('category_id')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='category_id',
            data=self.data['categories']['id'].values,
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
            data=self.data['images']['id'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class CategoryField(BaseField):
    """Category name field metadata process/save class."""

    @display_message_processing('category')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='category',
            data=str2ascii(list(self.data['categories']['name'].values)),
            dtype=np.uint8,
            fillvalue=0
        )


class SuperCategoryField(BaseField):
    """Super category name field metadata process/save class."""

    @display_message_processing('supercategory')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='supercategory',
            data=str2ascii(list(self.data['categories']['supercategory'].values)),
            dtype=np.uint8,
            fillvalue=0
        )


class CocoURLField(BaseField):
    """Coco URL link field metadata process/save class."""

    @display_message_processing('coco_url')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='coco_url',
            data=str2ascii(list(self.data['images']['coco_url'].values)),
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
            data=str2ascii(list(self.data['images']['file_name'].values)),
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
            data=self.data['images']['height'].values,
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
            data=self.data['images']['width'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class ColumnField(BaseColumnField):
    """Column names' field metadata process/save class."""

    fields = [
        'category_id',
        'image_id',
        'category',
        'supercategory',
        'coco_url',
        'image_filename',
        'height',
        'width'
    ]
