"""
COCO Captions 2015/2016 process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_json

from .load_data_test import load_data_test


class Caption2015(BaseTask):
    """ COCO Captions (2015) preprocessing functions """

    # metadata filename
    filename_h5 = 'caption_2015'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2014'
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'captions_train2014.json'),
        "val" : os.path.join('annotations', 'captions_val2014.json'),
        "test" : os.path.join('annotations', 'image_info_test2014.json')
    }


    def load_data_trainval(self, set_name, image_dir, annotation_path):
        """
        Load train+val data
        """
        data = {}

        # load annotations file
        if self.verbose:
            print('  > Loading annotation file: ' + annotation_path)
        annotations = load_json(annotation_path)

        # progressbar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(annotations['annotations']))

        # parse annotations
        # images
        if self.verbose:
            print('  > Processing image annotations... ')
        images = {}
        for i, annot in enumerate(annotations['images']):
            images[annot['id']] = {
                "width" : annot['width'],
                "height" : annot['height'],
                "file_name" : os.path.join(image_dir, annot['file_name'])
            }


        if self.verbose:
            print('  > Processing data annotations... ')
        for i, annot in enumerate(annotations['annotations']):
            img_id = annot['image_id']
            img_annotation = images[img_id]

            caption = annot["caption"]

            if img_id in data.keys():
                data[img_id]['captions'].append(caption)
            else:
                img_annotation = images[img_id]
                data[img_id] = {
                    "filename" : img_annotation['file_name'],
                    "width" : img_annotation['width'],
                    "height" : img_annotation['height'],
                    "captions" : [caption]
                }

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # reset progressbar
        if self.verbose:
            prgbar.finish()

        return {set_name : [data, annotations]}


    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        for set_name in self.image_dir_path:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)

            # image dir
            image_dir = self.image_dir_path[set_name]

            # annotation file path
            annot_filepath = os.path.join(self.data_path, self.annotation_path[set_name])

            if 'test' in set_name:
                yield load_data_test(set_name, image_dir, annot_filepath, self.verbose)
            else:
                yield self.load_data_trainval(set_name, image_dir, annot_filepath)


    def add_data_to_source(self, handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        data_ = data[0]
        annotations = data[1]
        image_dir = self.image_dir_path[set_name]

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        # images - original
        image_grp = handler.create_group('images')
        for i, annot in enumerate(annotations['images']):
            file_grp = image_grp.create_group(str(i))
            file_grp['file_name'] = str2ascii(os.path.join(image_dir, annot["file_name"]))
            file_grp['coco_url'] = str2ascii(annot["coco_url"])
            file_grp['width'] = np.array(annot["width"], dtype=np.int32)
            file_grp['height'] = np.array(annot["height"], dtype=np.int32)
            file_grp['id'] = np.array(annot["id"], dtype=np.int32)


        # annotations - original
        if set_name != 'test':
            annot_grp = handler.create_group('annotations')
            for i, annot in enumerate(annotations['annotations']):
                file_grp = annot_grp.create_group(str(i))
                file_grp['caption'] = str2ascii(annot["iscrowd"])
                file_grp['id'] = np.array(annot["id"], dtype=np.int32)
                file_grp['image_id'] = np.array(annot["image_id"], dtype=np.int32)

        # grouped/combined data - parsed by me
        grouped_grp = handler.create_group('grouped')
        for i, key in enumerate(data_):
            file_grp = grouped_grp.create_group(str(i))
            file_grp['image_filename'] = str2ascii(data_[key]["filename"])
            file_grp['width'] = np.array(data_[key]["width"], dtype=np.int32)
            file_grp['height'] = np.array(data_[key]["height"], dtype=np.int32)
            if 'captions' in data_[key]:
                file_grp['captions'] = str2ascii(data_[key]["captions"])

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


    def add_data_to_default(self, handler, data, set_name):
        """
        Add data of a set to the default group.
        """
        if "test" in set_name:
            is_test = True
            data_, category, supercategory = data
        else:
            is_test = False
            data_ = data[0]

        image_filenames = []
        width = []
        height = []
        caption = []
        object_id = []

        if is_test:
            object_fields = ["image_filenames", "width", "height"]
        else:
            object_fields = ["image_filenames", "captions", "width", "height"]

        list_captions_per_image = []
        list_object_ids_per_image = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        counter = 0
        for i, key in enumerate(data_):
            annotation = data_[key]
            image_filenames.append(annotation["filename"])
            width.append(annotation["width"])
            height.append(annotation["height"])

            if is_test:
                object_id.append([i, i, i])
                list_object_ids_per_image.append([i])
            else:
                captions_per_image = []
                for cap in annotation["captions"]:
                    caption.append(cap)

                    # object_id
                    # [filename, caption, width, height]
                    object_id.append([i, counter, i, i])

                    captions_per_image.append(counter)

                    # update counter
                    counter += 1

                list_captions_per_image.append(captions_per_image)
                list_object_ids_per_image.append(captions_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['width'] = np.array(width, dtype=np.int32)
        handler['height'] = np.array(height, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)

        if not is_test:
            handler['captions'] = str2ascii(caption)

            handler['list_captions_per_image'] = np.array(pad_list(list_captions_per_image, -1), dtype=np.int32)
        else:
            handler['category'] = str2ascii(category)
            handler['supercategory'] = str2ascii(supercategory)


class Caption2015NoSourceGrp(Caption2015):
    """ COCO Caption (2015) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'caption_2015_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing


#---------------------------------------------------------
# Captions 2016
#---------------------------------------------------------


class Caption2016(Caption2015):
    """ COCO Caption (2016) preprocessing functions """

    # metadata filename
    filename_h5 = 'caption_2016'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2015',
        "test-dev" : "test2015"
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'captions_train2014.json'),
        "val" : os.path.join('annotations', 'captions_val2014.json'),
        "test" : os.path.join('annotations', 'image_info_test2015.json'),
        "test-dev" : os.path.join('annotations', 'image_info_test-dev2015.json')
    }


class Caption2016NoSourceGrp(Caption2016):
    """ COCO Caption (2016) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'caption_2016_d'

    def add_data_to_source(self, handler, data):
        """
        Dummy method
        """
        # do nothing