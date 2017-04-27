"""
COCO Detection 2015 process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_json


class Detection2015:
    """ COCO Detection (2015) preprocessing functions """


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        # get correct set paths
        image_dir_path = {
            "train" : 'train2014',
            "val" : 'val2014',
            "test" : 'test2014'
        }

        annotation_path = {
            "train" : os.path.join(self.data_path, 'annotations', 'instances_train2014.json'),
            "val" : os.path.join(self.data_path, 'annotations', 'instances_val2014.json'),
            "test" : os.path.join(self.data_path, 'annotations', 'image_info_test2014.json')
        }

        for set_name in image_dir_path:
            if self.verbose:
                print('> Loading data files...')


            # image dir
            image_dir = image_dir_path[set_name]

            # load annotation file
            annotations = load_json(annotation_path[set_name])

            # progressbar
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(annotations['annotations']))

            # parse annotations
            # images
            images = {}
            for i, annot in enumerate(annotations['images']):
                images[annot['id']] = {
                    "width" : annot['width'],
                    "height" : annot['height'],
                    "file_name" : os.path.join(image_dir, annot['file_name'])
                }

            # categories
            categories = {}
            category_list, supercategory_list = [], []
            for i, annot in enumerate(annotations['categories']):
                categories[annot['id']] = {
                    "name" : annot['name'],
                    "supercategory" : annot['supercategory']
                }
                category_list[i] = annot['name']
                supercategory_list[i] = annot['supercategory']
            supercategory_list = list(set(supercategory_list))

            data = {}
            for i, annot in enumerate(annotations['annotations']):

                img_id = annot['image_id']
                category_annot = categories[annot['category_id']]

                obj = {
                    "category" : category_annot['name'],
                    "supercategory" : category_annot['supercategory'],
                    "area" : annot['area'],
                    "iscrowd" : annot['iscrowd'],
                    "segmentation" : annot['segmentation'],
                    "bbox" : annot['bbox']
                }

                if img_id in data.keys():
                    data[img_id]['object'].append(obj)
                else:
                    img_annotation = images[img_id]
                    data[img_id] = {
                        "filename" : img_annotation['file_name'],
                        "width" : img_annotation['width'],
                        "height" : img_annotation['height'],
                        "object" : obj
                    }

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

            # reset progressbar
            if self.verbose:
                prgbar.finish()

            yield {set_name : [data, category_list, supercategory_list]}


    def add_data_to_source(self, handler, data):
        """
        Store classes + filenames as a nested tree.
        """

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, data_ in data[0]:

            file_grp = handler.create_group(str(i))
            file_grp['image_filename'] = data_["filename"]
            file_grp['width'] = data_["width"]
            file_grp['height'] = data_["height"]

            for j, obj in enumerate(data_["object"]):
                obj_grp = file_grp.create_group(str(j))
                obj_grp['category'] = obj["category"]
                obj_grp['supercategory'] = obj["supercategory"]
                obj_grp['area'] = obj["area"]
                obj_grp['iscrowd'] = obj["iscrowd"]
                obj_grp['segmentation'] = obj["segmentation"]
                obj_grp['bbox'] = obj["bbox"]

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


    def add_data_to_default(self, handler, data):
        """
        Add data of a set to the default group.
        """
        image_filenames = []
        width = []
        height = []

        area = []
        iscrowd = [0, 1]
        segmentation = []
        bbox = []
        object_id = []
        object_fields = ["filename", "category", "supercategory", "bbox",
                         "area", "segmentation", "iscrowd", "width", "height"]

        list_image_filenames_per_category = []
        list_image_filenames_per_supercategory = []
        list_boxes_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_category = []
        list_objects_ids_per_supercategory = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        data_, category, supercategory = data

        counter = 0
        for i, annotation in enumerate(data_):

            image_filenames.append(annotation["filename"])
            width.append(annotation["width"])
            height.append(annotation["height"])

            boxes_per_image = []
            for j, obj in enumerate(annotation["object"]):
                area.append(obj["area"])
                bbox.append(obj["bbox"])
                segmentation.append(obj["segmentation"])

                # object_id
                # [filename, category, supercategory, bbox, area, segmentation, iscrowd, width, height]
                object_id.append([i, category.index(obj["category"]),
                                  supercategory.index(obj["supercategory"]),
                                  j, j, j, j, i, i])

                boxes_per_image.append(counter)

                # update counter
                counter += 1

            list_boxes_per_image.append(boxes_per_image)
            list_object_ids_per_image.append(counter)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        if self.verbose:
            print('> Processing lists...')

         # process lists
        for i in range(len(category)):
            imgs_per_class = [val[0] for _, val in enumerate(object_id) if val[1] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_category.append(imgs_per_class)

        for i in range(len(supercategory)):
            imgs_per_class = [val[0] for _, val in enumerate(object_id) if val[2] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_supercategory.append(imgs_per_class)

        for i in range(len(category)):
            imgs_per_class = [j for j, val in enumerate(object_id) if val[1] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_category.append(imgs_per_class)

        for i in range(len(supercategory)):
            imgs_per_class = [j for j, val in enumerate(object_id) if val[2] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_supercategory.append(imgs_per_class)


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['width'] = np.array(width, dtype=np.int32)
        handler['height'] = np.array(height, dtype=np.int32)
        handler['category'] = str2ascii(category)
        handler['supercategory'] = str2ascii(supercategory)
        handler['boxes'] = np.array(bbox, dtype=np.float)
        handler['iscrowd'] = np.array(iscrowd, dtype=np.uint8)
        handler['segmentation'] = np.array(pad_list(segmentation), dtype=np.int32)
        handler['area'] = np.array(area, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_image_filenames_per_category'] = np.array(pad_list(list_image_filenames_per_category, -1), dtype=np.int32)
        handler['list_image_filenames_per_supercategory'] = np.array(pad_list(list_image_filenames_per_supercategory, -1), dtype=np.int32)
        handler['list_boxes_per_image'] = np.array(pad_list(list_boxes_per_image, -1), dtype=np.int32)
        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)
        handler['list_objects_ids_per_category'] = np.array(pad_list(list_objects_ids_per_category, -1), dtype=np.int32)
        handler['list_objects_ids_per_supercategory'] = np.array(pad_list(list_objects_ids_per_supercategory), dtype=np.int32)


    def process_metadata(self, save_name):
        """
        Process metadata and store it in a hdf5 file.
        """

        # create/open hdf5 file with subgroups for train/val/test
        if save_name:
            file_name = os.path.join(self.cache_path, save_name)
        else:
            file_name = os.path.join(self.cache_path, 'detection_2015.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(file_name))

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                if self.verbose:
                    print('\nSaving set metadata: {}'.format(set_name))

                # add data to the **source** group
                sourceg = fileh5.create_group('source/' + set_name)
                self.add_data_to_source(sourceg, data[set_name])

                # add data to the **default** group
                defaultg = fileh5.create_group('default/' + set_name)
                self.add_data_to_default(defaultg, data[set_name])

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self, save_name=None):
        """
        Run task processing.
        """
        return self.process_metadata(save_name)