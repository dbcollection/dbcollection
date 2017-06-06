"""
COCO Keypoints 2016 process functions.
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


class Keypoints2016(BaseTask):
    """ COCO Keypoints (2016) preprocessing functions """

    # metadata filename
    filename_h5 = 'keypoint_2016'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2015',
        "test-dev" : 'test2015'
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'person_keypoints_train2014.json'),
        "val" : os.path.join('annotations', 'person_keypoints_val2014.json'),
        "test" : os.path.join('annotations', 'image_info_test2015.json'),
        "test-dev" : os.path.join('annotations', 'image_info_test-dev2015.json')
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

        # categories
        category = annotations['categories'][0]['name']
        supercategory = annotations['categories'][0]['supercategory']
        skeleton = annotations['categories'][0]['skeleton']
        keypoints = annotations['categories'][0]['keypoints']


        if self.verbose:
            print('  > Processing data annotations... ')
        for i, annot in enumerate(annotations['annotations']):
            img_id = annot['image_id']

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
                "category" : category,
                "supercategory" : supercategory,
                "area" : annot['area'],
                "iscrowd" : annot['iscrowd'],
                "segmentation" : segmentation,
                "segmentation_type" : segmentation_type,
                "bbox" : annot['bbox'],
                "num_keypoints" : annot['num_keypoints'],
                "keypoints" : annot['keypoints'],
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

        return {set_name : [data, annotations, category, supercategory, skeleton, keypoints]}


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

        if len(data) > 3:
            category = data[2]
            supercategory = data[3]
            skeleton = data[4]
            keypoints = data[5]

            category_ = str2ascii(category)
            supercategory_ = str2ascii(supercategory)
            keypoints_ = str2ascii(keypoints)
            skeleton_ = np.array(pad_list(skeleton, -1), dtype=np.uint8)

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

        # categories - original
        cat_grp = handler.create_group('categories')
        for i, annot in enumerate(annotations['categories']):
            file_grp = cat_grp.create_group(str(i))
            file_grp['supercategory'] = str2ascii(annot["supercategory"])
            file_grp['name'] = str2ascii(annot["name"])
            file_grp['keypoints'] = str2ascii(annot["keypoints"])
            file_grp['skeleton'] = np.array(annot["skeleton"], dtype=np.uint8)
            file_grp['id'] = np.array(annot["id"], dtype=np.int32)


        # annotations - original
        if set_name != 'test':
            annot_grp = handler.create_group('annotations')
            for i, annot in enumerate(annotations['annotations']):
                file_grp = annot_grp.create_group(str(i))
                file_grp['iscrowd'] = np.array(annot["iscrowd"], dtype=np.int32)
                file_grp['area'] = np.array(annot["area"], dtype=np.float)
                file_grp['id'] = np.array(annot["id"], dtype=np.int32)
                file_grp['category_id'] = np.array(annot["category_id"], dtype=np.int32)
                file_grp['image_id'] = np.array(annot["image_id"], dtype=np.int32)
                file_grp['bbox'] = np.array(annot["bbox"], dtype=np.float)
                file_grp['segmentation'] = np.array(annot["segmentation"], dtype=np.float)
                file_grp['keypoints'] = np.array(annot["keypoints"], dtype=np.int32)
                file_grp['num_keypoints'] = np.array(annot["num_keypoints"], dtype=np.uint8)


        # grouped/combined data - parsed by me
        grouped_grp = handler.create_group('grouped')
        for i, key in enumerate(data_):
            file_grp = grouped_grp.create_group(str(i))
            file_grp['image_filename'] = str2ascii(data_[key]["filename"])
            file_grp['width'] = np.array(data_[key]["width"], dtype=np.int32)
            file_grp['height'] = np.array(data_[key]["height"], dtype=np.int32)

            if 'object' in data_[key]:
                file_grp['keypoint_names'] = keypoints_
                file_grp['skeleton'] = skeleton_
                for j, obj in enumerate(data_[key]["object"]):
                    obj_grp = file_grp.create_group(str(j))
                    obj_grp['category'] = category_
                    obj_grp['supercategory'] = supercategory_
                    obj_grp['area'] = np.array(obj["area"], dtype=np.int32)
                    obj_grp['iscrowd'] = np.array(obj["iscrowd"], dtype=np.int32)
                    obj_grp['bbox'] = np.array(obj["bbox"], dtype=np.float)
                    if obj["segmentation_type"] == 0:
                        obj_grp['segmentation'] = np.array(pad_list(obj["segmentation"], -1), dtype=np.float)
                    else:
                        obj_grp['segmentation'] = np.array(obj["segmentation"], dtype=np.int32)
                    obj_grp['segmentation_type'] = obj["segmentation_type"]
                    obj_grp['num_keypoints'] = np.array(obj["num_keypoints"], dtype=np.uint8)
                    obj_grp['keypoints'] = np.array(obj["keypoints"], dtype=np.int32)

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
            category_ = str2ascii(category)
            supercategory_ = str2ascii(supercategory)
        else:
            is_test = False
            data_, category, supercategory, skeleton, keypoints = data

            category_ = str2ascii(category)
            supercategory_ = str2ascii(supercategory)
            keypoints_ = str2ascii(keypoints)
            skeleton_ = np.array(pad_list(skeleton, -1), dtype=np.uint8)


        image_filenames = []
        width = []
        height = []

        area = []
        iscrowd = [0, 1]
        segmentation_t1 = [[[]]]
        segmentation_t2 = [[]]
        num_keypoints = list(range(0, 17+1))
        keypoints_list = []
        bbox = []
        object_id = []

        if is_test:
            object_fields = ["image_filenames", "width", "height"]
        else:
            object_fields = ["image_filenames", "category", "supercategory",
                             "boxes", "area", "segmentation", "segmentation_type",
                             "iscrowd", "num_keypoints", "keypoints",
                             "width", "height"]

        list_boxes_per_image = []
        list_keypoints_per_image = []
        list_object_ids_per_image = []
        list_image_filenames_per_num_keypoints = []
        list_object_ids_per_keypoint = [] # body part

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))


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
                    keypoints_list.append(obj["keypoints"])

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
                    # [filename, category, supercategory, bbox, area, segmentation 1,
                    # segmentation 2, iscrowd, num_keypoints, keypoints, width, height]
                    object_id.append([i, category.index(obj["category"]),
                                      supercategory.index(obj["supercategory"]),
                                      counter, counter, segmentation_t1_id, segmentation_t2_id,
                                      counter, obj["num_keypoints"], counter, i, i])

                    boxes_per_image.append(counter)

                    # update counter
                    counter += 1

                list_boxes_per_image.append(boxes_per_image)
                list_keypoints_per_image.append(boxes_per_image)
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

            for i in range(len(keypoints)):
                imgs_per_num = [val[0] for _, val in enumerate(object_id) if val[8] == i]
                imgs_per_num = list(set(imgs_per_num)) # get unique values
                imgs_per_num.sort()
                list_image_filenames_per_num_keypoints.append(imgs_per_num)

            for i in range(len(keypoints)):
                objs_per_keypoint = [j for j, val in enumerate(keypoints_list) if val[i*3] > 0 or val[i*3+1] > 0]
                objs_per_keypoint = list(set(objs_per_keypoint)) # get unique values
                objs_per_keypoint.sort()
                list_object_ids_per_keypoint.append(objs_per_keypoint)


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['category'] = category_
        handler['supercategory'] = supercategory_
        handler['width'] = np.array(width, dtype=np.int32)
        handler['height'] = np.array(height, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)

        if not is_test:
            handler['keypoint_names'] = keypoints_
            handler['skeleton'] = skeleton_
            handler['boxes'] = np.array(bbox, dtype=np.float)
            handler['iscrowd'] = np.array(iscrowd, dtype=np.uint8)
            handler['segmentation1'] = np.array(pad_list2(segmentation_t1, -1), dtype=np.float)
            handler['segmentation2'] = np.array(pad_list(segmentation_t2, -1), dtype=np.int32)
            handler['area'] = np.array(area, dtype=np.int32)
            handler['num_keypoints'] = np.array(num_keypoints, dtype=np.uint8)
            handler['keypoints'] = np.array(keypoints_list, dtype=np.int32)

            handler['list_boxes_per_image'] = np.array(pad_list(list_boxes_per_image, -1), dtype=np.int32)
            handler['list_keypoints_per_image'] = np.array(pad_list(list_keypoints_per_image, -1), dtype=np.int32)
            handler['list_image_filenames_per_num_keypoints'] = np.array(pad_list(list_image_filenames_per_num_keypoints, -1), dtype=np.int32)
            handler['list_object_ids_per_keypoint'] = np.array(pad_list(list_object_ids_per_keypoint, -1), dtype=np.int32)


class Keypoints2016NoSourceGrp(Keypoints2016):
    """ COCO Keypoints (2016) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'keypoint_2016_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing