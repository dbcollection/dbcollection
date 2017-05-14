"""
COCO Detection 2015/2016 process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list, pad_list2
from dbcollection.utils.file_load import load_json

from .load_data_test import load_data_test


class Detection2015(BaseTask):
    """ COCO Detection (2015) preprocessing functions """

    # metadata filename
    filename_h5 = 'detection_2015'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2014'
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'instances_train2014.json'),
        "val" : os.path.join('annotations', 'instances_val2014.json'),
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
        image_id = []
        for i, annot in enumerate(annotations['images']):
            images[annot['id']] = {
                "width" : annot['width'],
                "height" : annot['height'],
                "file_name" : os.path.join(image_dir, annot['file_name'])
            }
            image_id.append(annot['id'])

        # categories
        if self.verbose:
            print('  > Processing category annotations... ')
        categories = {}
        category_list, supercategory_list, category_id = [], [], []
        for i, annot in enumerate(annotations['categories']):
            categories[annot['id']] = {
                "name" : annot['name'],
                "supercategory" : annot['supercategory']
            }
            category_id.append(annot['id'])
            category_list.append(annot['name'])
            supercategory_list.append(annot['supercategory'])
        supercategory_list = list(set(supercategory_list))

        if self.verbose:
            print('  > Processing data annotations... ')
        for i, annot in enumerate(annotations['annotations']):
            img_id = annot['image_id']
            category_annot = categories[annot['category_id']]

            if isinstance(annot["segmentation"], list):
                segmentation_type = 0
                segmentation = annot["segmentation"]
            elif isinstance(annot["segmentation"]['counts'], list):
                segmentation_type = 1
                segmentation = annot["segmentation"]["counts"]
            else:
                segmentation_type = 2
                segmentation = annot["segmentation"]

            obj = {
                "category" : category_annot['name'],
                "supercategory" : category_annot['supercategory'],
                "area" : annot['area'],
                "iscrowd" : annot['iscrowd'],
                "segmentation" : segmentation, #annot['segmentation'],
                "segmentation_type" : segmentation_type,
                "bbox" : annot['bbox'],
                "image_id": annot['image_id'],
                "category_id": annot['category_id'],
                "id" : annot["id"]
            }

            if img_id in data.keys():
                data[img_id]['object'].append(obj)
            else:
                img_annotation = images[img_id]
                data[img_id] = {
                    "filename" : img_annotation['file_name'],
                    "width" : img_annotation['width'],
                    "height" : img_annotation['height'],
                    "object" : [obj]
                }

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # reset progressbar
        if self.verbose:
            prgbar.finish()

        return {set_name : [data, category_list, supercategory_list, image_id, category_id]}


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

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        for i, key in enumerate(data_):
            file_grp = handler.create_group(str(i))
            file_grp['image_filename'] = str2ascii(data_[key]["filename"])
            file_grp['width'] = np.array(data_[key]["width"], dtype=np.int32)
            file_grp['height'] = np.array(data_[key]["height"], dtype=np.int32)

            if 'object' in data_[key]:
                for j, obj in enumerate(data_[key]["object"]):
                    obj_grp = file_grp.create_group(str(j))
                    obj_grp['id'] = str2ascii(obj["id"])
                    obj_grp['image_id'] = str2ascii(obj["image_id"])
                    obj_grp['category_id'] = str2ascii(obj["category_id"])
                    obj_grp['category'] = str2ascii(obj["category"])
                    obj_grp['supercategory'] = str2ascii(obj["supercategory"])
                    obj_grp['area'] = np.array(obj["area"], dtype=np.int32)
                    obj_grp['iscrowd'] = np.array(obj["iscrowd"], dtype=np.int32)
                    obj_grp['bbox'] = np.array(obj["bbox"], dtype=np.float)
                    if obj["segmentation_type"] == 0:
                        obj_grp['segmentation'] = np.array(pad_list(obj["segmentation"], -1), dtype=np.float)
                    else:
                        obj_grp['segmentation'] = np.array(obj["segmentation"], dtype=np.int32)
                    obj_grp['segmentation_type'] = obj["segmentation_type"]

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
        if 'test' in  set_name:
            is_test = True
            data_, category, supercategory = data
        else:
            is_test = False
            data_, category, supercategory, image_id, category_id = data

        image_filenames = []
        width = []
        height = []

        obj_id = []

        area = []
        iscrowd = [0, 1]
        segmentation = []
        segmentation_t1 = [[[]]]
        segmentation_t2 = [[]]
        bbox = []
        object_id = []

        if is_test:
            object_fields = ["image_filenames", "width", "height"]
        else:
            object_fields = ["image_filenames", "width", "height", "category", "supercategory",
                             "boxes", "area", "segmentation", "segmentation_type", "iscrowd"]

        list_image_filenames_per_category = []
        list_image_filenames_per_supercategory = []
        list_boxes_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_category = []
        list_objects_ids_per_supercategory = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data[0]))

        counter = 0
        segmentation_t1_counter, segmentation_t2_counter = 0, 0
        for i, key in enumerate(data_):
            annotation = data_[key]
            image_filenames.append(annotation["filename"])
            width.append(annotation["width"])
            height.append(annotation["height"])

            if is_test:
                object_id.append([i, i, i])
                list_object_ids_per_image.append([i])
            else:
                boxes_per_image = []
                for obj in annotation["object"]:
                    area.append(obj["area"])
                    bbox.append(obj["bbox"])
                    obj_id.append(obj["id"])

                    if obj["segmentation_type"] == 0:
                        segmentation_t1.append(obj["segmentation"])
                        segmentation_t1_counter += 1
                        segmentation_t2_id = 0
                        segmentation_t1_id = segmentation_t1_counter
                    else:
                        segmentation_t2.append(obj["segmentation"])
                        segmentation_t2_counter += 1
                        segmentation_t1_id = 0
                        segmentation_t2_id = segmentation_t1_counter

                    # object_id
                    # [filename, category, supercategory, bbox, area, segmentation 1, segmentation 2, iscrowd, width, height]
                    object_id.append([i, i, i, category.index(obj["category"]),
                                      supercategory.index(obj["supercategory"]),
                                      counter, counter, segmentation_t1_id, segmentation_t2_id,
                                      counter])

                    boxes_per_image.append(counter)

                    # update counter
                    counter += 1

                list_boxes_per_image.append(boxes_per_image)
                list_object_ids_per_image.append(boxes_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


        # process lists
        if not is_test:
            if self.verbose:
                print('> Processing lists...')

            for i in range(len(category)):
                imgs_per_category = [val[0] for _, val in enumerate(object_id) if val[1] == i]
                imgs_per_category = list(set(imgs_per_category)) # get unique values
                imgs_per_category.sort()
                list_image_filenames_per_category.append(imgs_per_category)

            for i in range(len(supercategory)):
                imgs_per_supercategory = [val[0] for _, val in enumerate(object_id) if val[2] == i]
                imgs_per_supercategory = list(set(imgs_per_supercategory)) # get unique values
                imgs_per_supercategory.sort()
                list_image_filenames_per_supercategory.append(imgs_per_supercategory)

            for i in range(len(category)):
                obj_per_category = [j for j, val in enumerate(object_id) if val[1] == i]
                obj_per_category = list(set(obj_per_category)) # get unique values
                obj_per_category.sort()
                list_objects_ids_per_category.append(obj_per_category)

            for i in range(len(supercategory)):
                obj_per_supercategory = [j for j, val in enumerate(object_id) if val[2] == i]
                obj_per_supercategory = list(set(obj_per_supercategory)) # get unique values
                obj_per_supercategory.sort()
                list_objects_ids_per_supercategory.append(obj_per_supercategory)


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['category'] = str2ascii(category)
        handler['supercategory'] = str2ascii(supercategory)
        handler['width'] = np.array(width, dtype=np.int32)
        handler['height'] = np.array(height, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)

        if not is_test:
            handler['id'] = np.array(obj_id, dtype=np.int32)
            handler['image_id'] = np.array(image_id, dtype=np.int32)
            handler['category_id'] = np.array(category_id, dtype=np.int32)
            handler['boxes'] = np.array(bbox, dtype=np.float)
            handler['iscrowd'] = np.array(iscrowd, dtype=np.uint8)
            handler['segmentation1'] = np.array(pad_list2(segmentation_t1, -1), dtype=np.float)
            handler['segmentation2'] = np.array(pad_list(segmentation_t2, -1), dtype=np.int32)
            handler['area'] = np.array(area, dtype=np.int32)

            handler['list_image_filenames_per_category'] = np.array(pad_list(list_image_filenames_per_category, -1), dtype=np.int32)
            handler['list_image_filenames_per_supercategory'] = np.array(pad_list(list_image_filenames_per_supercategory, -1), dtype=np.int32)
            handler['list_boxes_per_image'] = np.array(pad_list(list_boxes_per_image, -1), dtype=np.int32)
            handler['list_objects_ids_per_category'] = np.array(pad_list(list_objects_ids_per_category, -1), dtype=np.int32)
            handler['list_objects_ids_per_supercategory'] = np.array(pad_list(list_objects_ids_per_supercategory), dtype=np.int32)


class Detection2015NoSourceGrp(Detection2015):
    """ COCO Detection (2015) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'detection_2015_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing


#---------------------------------------------------------
# Detection 2016
#---------------------------------------------------------


class Detection2016(Detection2015):
    """ COCO Detection (2015) preprocessing functions """

    # metadata filename
    filename_h5 = 'detection_2016'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2015',
        "test-dev" : "test2015"
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'instances_train2014.json'),
        "val" : os.path.join('annotations', 'instances_val2014.json'),
        "test" : os.path.join('annotations', 'image_info_test2015.json'),
        "test-dev" : os.path.join('annotations', 'image_info_test-dev2015.json')
    }


class Detection2016NoSourceGrp(Detection2016):
    """ COCO Detection (2016) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'detection_2016_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing