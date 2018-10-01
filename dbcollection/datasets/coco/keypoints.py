"""
COCO Keypoints 2016 process functions.
"""


from __future__ import print_function, division

import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from dbcollection.datasets import BaseTask, BaseField, BaseColumnField
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list, squeeze_list
from dbcollection.utils.file_load import load_json

from .process_test import process_save_test_metadata_to_hdf5


class Keypoints2016(BaseTask):
    """COCO Keypoints (2016) preprocessing functions."""

    # metadata filename
    filename_h5 = 'keypoint_2016'

    annotations = {
        "train": {
            "images_dir": 'train2014',
            "file_name": 'person_keypoints_train2014.json',
        },
        "val": {
            "images_dir": 'val2014',
            "file_name": 'person_keypoints_val2014.json'
        },
        "test": {
            "images_dir": 'test2015',
            "file_name": 'image_info_test2015.json'
        },
        "test_dev": {
            "images_dir": 'test2015',
            "file_name": 'image_info_test-dev2015.json'
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
        IdField(**kwargs).process()
        CategoryIdField(**kwargs).process()
        ImageIdField(**kwargs).process()
        AreaField(**kwargs).process()
        BboxField(**kwargs).process()
        IsCrowdField(**kwargs).process()
        SegmentationField(**kwargs).process()
        KeypointsField(**kwargs).process()
        NumberKeypointsField(**kwargs).process()
        KeypointNamesField(**kwargs).process()
        SkeletonField(**kwargs).process()
        CategoryField(**kwargs).process()
        SuperCategoryField(**kwargs).process()
        CocoURLField(**kwargs).process()
        ImageFilenameField(**kwargs).process()
        ImageHeightField(**kwargs).process()
        ImageWidthField(**kwargs).process()

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        ImagesPerCategoryIdList(**kwargs).process()
        ImagesPerSuperCategoryList(**kwargs).process()
        BboxesPerImageList(**kwargs).process()
        IdsPerImageList(**kwargs).process()
        IdsPerCategoryList(**kwargs).process()
        IdsPerSuperCategoryList(**kwargs).process()

        # Column field
        ColumnField(**kwargs).process()


class DatasetAnnotationLoader:
    """Annotation's data loader for the coco detection dataset (train/test)."""

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
        categories = self.get_dataframe_categories(data)
        images = self.get_dataframe_images(data, image_dir_path)
        if set_name in ['test', 'test_dev']:
            return {
                "images": images.reset_index(),
                "categories": categories.reset_index()
            }
        else:
            annotations = self.get_dataframe_annotations(data)
            df = annotations.join(categories, on='category_id', rsuffix='_names').join(images, on='image_id')
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


class CategoryIdField(BaseField):
    """Category id field metadata process/save class."""

    @display_message_processing('category_id')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='category_id',
            data=self.data['full_data']['category_id'].values,
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


class AreaField(BaseField):
    """Area field metadata process/save class."""

    @display_message_processing('area')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='area',
            data=self.data['full_data']['area'].values,
            dtype=np.int32,
            fillvalue=-1
        )


class BboxField(BaseField):
    """Bbox field metadata process/save class."""

    @display_message_processing('bbox')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='bbox',
            data=np.vstack(self.data['full_data']['bbox'].values).astype(np.int32),
            dtype=np.int32,
            fillvalue=-1
        )


class IsCrowdField(BaseField):
    """Is crowd field metadata process/save class."""

    @display_message_processing('iscrowd')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='iscrowd',
            data=self.data['full_data']['iscrowd'].values,
            dtype=np.uint8
        )


class SegmentationField(BaseField):
    """Segmentation field metadata process/save class."""

    @display_message_processing('segmentation')
    def process(self):
        segmentation = self.convert_numpy_array_to_list_of_lists(self.data['full_data']['segmentation'].values)
        segmentation_hdf5_handler = self.set_segmentation_dataset_h5(segmentation)
        for i, segment in tqdm(enumerate(segmentation)):
            segmentation_hdf5_handler[i, :len(segment)] = np.array(segment, dtype=np.float)

    def convert_numpy_array_to_list_of_lists(self, segmentation):
        output = []
        for segmentation_mask in segmentation:
            if isinstance(segmentation_mask, list):
                segmentation_ = squeeze_list(segmentation_mask, -1)  # squeeze list
            elif isinstance(segmentation_mask, dict):
                if isinstance(segmentation_mask["counts"], list):
                    segmentation_ = segmentation_mask["counts"]
                else:
                    raise Exception("Undefined segmentation mask: {}".format(segmentation_mask))
            else:
                segmentation_ = segmentation_mask
            output.append(segmentation_)
        return output

    def set_segmentation_dataset_h5(self, segmentation):
        nrows = len(segmentation)
        ncols = max([len(l) for l in segmentation])
        segmentation_hdf5_handler = self.hdf5_manager.file.create_dataset(
            'segmentation',
            (nrows, ncols),
            dtype=np.float,
            chunks=True,
            compression="gzip",
            compression_opts=4,
            fillvalue=-1
        )
        return segmentation_hdf5_handler


class KeypointsField(BaseField):
    """Keypoints coordinates field metadata process/save class."""

    @display_message_processing('keypoints')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoints',
            data=np.array(list(self.data['full_data']['keypoints'].values), dtype=np.int32),
            dtype=np.int32,
            fillvalue=0
        )


class NumberKeypointsField(BaseField):
    """Number of keypoints field metadata process/save class."""

    @display_message_processing('number of keypoints')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='num_keypoints',
            data=self.data['full_data']['num_keypoints'].values,
            dtype=np.uint8,
            fillvalue=-1
        )


class KeypointNamesField(BaseField):
    """Keypoint names field metadata process/save class."""

    @display_message_processing('keypoint names')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='keypoint_names',
            data=str2ascii(list(self.data['full_data']['keypoints_names'].values)),
            dtype=np.uint8,
            fillvalue=0
        )


class SkeletonField(BaseField):
    """Skeleton field metadata process/save class."""

    @display_message_processing('skeleton')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='skeleton',
            data=np.array(list(self.data['full_data']['skeleton'].values), dtype=np.uint8),
            dtype=np.uint8,
            fillvalue=-1
        )


class CategoryField(BaseField):
    """Category name field metadata process/save class."""

    @display_message_processing('category')
    def process(self):
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='category',
            data=str2ascii(list(self.data['full_data']['name'].values)),
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
            data=str2ascii(list(self.data['full_data']['supercategory'].values)),
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


class ColumnField(BaseColumnField):
    """Column names' field metadata process/save class."""

    fields = [
        'id',
        'category_id',
        'image_id',
        'area',
        'bbox',
        'iscrowd',
        'segmentation',
        'keypoints',
        'num_keypoints',
        'keypoint_names',
        'skeleton',
        'category',
        'supercategory',
        'coco_url',
        'image_filename',
        'height',
        'width',
        'list_images_per_category',
        'list_images_per_supercategory',
        'list_images_per_category',
        'list_ids_per_image',
        'list_ids_per_category',
        'list_ids_per_supercategory'
    ]


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------


class CustomListBaseField(BaseField):
    """Custom base class for list fields."""

    def convert_list_to_array(self, list_ids, dtype=np.int32):
        """Pads a list of listsand converts it into a numpy.ndarray."""
        padded_list = pad_list(list_ids, val=-1)
        return np.array(padded_list, dtype=dtype)


class ImagesPerCategoryIdList(CustomListBaseField):
    """Image ids per category list metadata process/save class."""

    @display_message_processing('image ids per category list')
    def process(self):
        image_ids_per_category = self.get_image_ids_per_category_id()
        image_ids_per_category_array = self.convert_list_to_array(image_ids_per_category)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_images_per_category',
            data=image_ids_per_category_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_image_ids_per_category_id(self):
        image_ids_per_category = self.data['full_data'].groupby('category_id')['image_id'].apply(list)
        return list(image_ids_per_category)


class ImagesPerSuperCategoryList(CustomListBaseField):
    """Image ids per super category list metadata process/save class."""

    @display_message_processing('image ids per supercategory list')
    def process(self):
        image_ids_per_supercategory = self.get_image_ids_per_supercategory()
        image_ids_per_supercategory_array = self.convert_list_to_array(image_ids_per_supercategory)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_images_per_supercategory',
            data=image_ids_per_supercategory_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_image_ids_per_supercategory(self):
        image_ids_per_supercategory = self.data['full_data'].groupby('supercategory')['image_id'].apply(list)
        return list(image_ids_per_supercategory)


class BboxesPerImageList(CustomListBaseField):
    """Boxes per image list metadata process/save class."""

    @display_message_processing('boxes per image list')
    def process(self):
        bbox_per_image_id = self.get_bbox_per_image_ids()
        bbox_per_image_id_array = self.convert_list_to_array(bbox_per_image_id)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_bboxes_per_image',
            data=bbox_per_image_id_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_bbox_per_image_ids(self):
        bbox_per_image_id = self.data['full_data'].groupby('image_id')['id'].apply(list)
        return list(bbox_per_image_id)


class IdsPerImageList(CustomListBaseField):
    """Ids per image list metadata process/save class."""

    @display_message_processing('ids per image list')
    def process(self):
        ids_per_image_id = self.get_ids_per_image_ids()
        ids_per_image_id_array = self.convert_list_to_array(ids_per_image_id)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_ids_per_image',
            data=ids_per_image_id_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_ids_per_image_ids(self):
        ids_per_image_id = self.data['full_data'].groupby('image_id')['id'].apply(list)
        return list(ids_per_image_id)


class IdsPerCategoryList(CustomListBaseField):
    """Ids per category list metadata process/save class."""

    @display_message_processing('ids per category list')
    def process(self):
        ids_per_category_id = self.get_ids_per_category_ids()
        ids_per_category_id_array = self.convert_list_to_array(ids_per_category_id)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_ids_per_category',
            data=ids_per_category_id_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_ids_per_category_ids(self):
        ids_per_category_id = self.data['full_data'].groupby('category_id')['id'].apply(list)
        return list(ids_per_category_id)


class IdsPerSuperCategoryList(CustomListBaseField):
    """Ids per super category list metadata process/save class."""

    @display_message_processing('ids per supercategory list')
    def process(self):
        ids_per_supercategory = self.get_ids_per_supercategory()
        ids_per_supercategory_array = self.convert_list_to_array(ids_per_supercategory)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_ids_per_supercategory',
            data=ids_per_supercategory_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_ids_per_supercategory(self):
        ids_per_category_id = self.data['full_data'].groupby('supercategory')['id'].apply(list)
        return list(ids_per_category_id)
