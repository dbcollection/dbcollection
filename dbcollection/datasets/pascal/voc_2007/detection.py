"""
Pascal VOC 2007 object detection processing functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.file_load import load_xml
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Detection(BaseTask):
    """ Pascal VOC 2007 object detection task class """

    # metadata filename
    filename_h5 = 'detection'

    # object classes
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
               'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
               'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']


    def get_set_filenames(self):
        """
        Return the train/val/test/trainval set id lists.
        """
        from .train_filenames import filenames as train_fnames
        from .val_filenames import filenames as val_fnames
        from .trainval_filenames import filenames as trainval_fnames
        from .test_filenames import filenames as test_fnames

        return {
            'train' : train_fnames,
            'val' : val_fnames,
            'trainval' : trainval_fnames,
            'test' : test_fnames
        }


    def load_data(self):
        """
        Load data of the dataset.
        """
        self.annotations_path = os.path.join(self.data_path, 'VOCdevkit', 'VOC2007', 'Annotations')
        self.images_path = os.path.join('VOCdevkit', 'VOC2007', 'JPEGImages')

        # set id list
        set_filenames = self.get_set_filenames()

        for set_name in set_filenames:

            # index list
            filename_list = set_filenames[set_name]

            data = []

            if self.verbose:
                print('\n==> Processing metadata for the set: {}'.format(set_name))
                print('> Loading data files...')

            # progressbar
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(filename_list))

            for i, filename in enumerate(filename_list):
                # setup file names
                annot_filename = os.path.join(self.annotations_path, filename + '.xml')
                image_filename = os.path.join(self.images_path, filename + '.jpg')

                # load annotation
                annotation = load_xml(annot_filename)

                data.append([image_filename, int(filename), annotation])

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

            # reset progressbar
            if self.verbose:
                prgbar.finish()

            yield {set_name : data}


    def add_data_to_source(self, handler, data, set_name):
        """
        Add data of a set to the source group.
        """

        def add_data_hdf5(handler, anno):
            """Add data to the hdf5 file."""
            handler['category_id'] = self.classes.index(anno['name'])
            handler['name'] = anno['name']
            handler['pose'] = anno['pose']
            handler['truncated'] = anno['truncated']
            handler['difficult'] = anno['difficult']
            handler['bndbox/xmin'] = anno['bndbox']['xmin']
            handler['bndbox/ymin'] = anno['bndbox']['ymin']
            handler['bndbox/xmax'] = anno['bndbox']['xmax']
            handler['bndbox/ymax'] = anno['bndbox']['ymax']

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, data_ in enumerate(data):
            image_filename, fileid, annotation = data_

            file_grp = handler.create_group(str(i))

            file_grp['image_filename'] = image_filename
            file_grp['id'] = fileid
            file_grp['size/width'] = annotation['annotation']['size']['width']
            file_grp['size/height'] = annotation['annotation']['size']['height']
            file_grp['size/depth'] = annotation['annotation']['size']['depth']
            file_grp['segmented'] = annotation['annotation']['segmented']

            if isinstance(annotation['annotation']['object'], list):
                obj_list = annotation['annotation']['object']
            else:
                obj_list = [annotation['annotation']['object']]

            for j, obj in enumerate(obj_list):
                object_grp = file_grp.create_group('object/{}/'.format(j))
                add_data_hdf5(object_grp, obj)

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
        object_fields = ['image_filenames', 'classes', 'boxes', 'sizes', 'difficult', 'truncated']
        image_filenames = []
        size = []
        bbox = []
        truncated = [0, 1]
        difficult = [0, 1]
        object_id = []

        obj_id = []  # for mscoco
        image_id = [] # for mscoco
        category_id = list(range(1, len(self.classes)+1)) # for mscoco

        list_image_filenames_per_class = []
        list_boxes_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_class = []
        list_objects_ids_no_difficult = []
        list_objects_ids_difficult = []
        list_objects_ids_no_truncated = []
        list_objects_ids_truncated = []


        if self.verbose:
            print('> Adding data to default group...')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        # cycle all data files/annotations
        obj_counter = 0
        for i, data_ in enumerate(data):
            image_filename, fileid, annotation = data_

            image_filenames.append(image_filename)
            image_id.append(fileid)

            width = annotation['annotation']['size']['width']
            height = annotation['annotation']['size']['height']
            depth = annotation['annotation']['size']['depth']
            size.append([depth, height, width])

            if isinstance(annotation['annotation']['object'], list):
                obj_list = annotation['annotation']['object']
            else:
                obj_list = [annotation['annotation']['object']]

            # cycle all objects
            for _, obj in enumerate(obj_list):
                class_id = self.classes.index(obj['name'])
                obj_id.append(obj_counter)
                bbox.append([obj['bndbox']['xmin'], obj['bndbox']['ymin'],
                             obj['bndbox']['xmax'], obj['bndbox']['ymax']])

                object_id.append([i, class_id, obj_counter, i,
                                  difficult.index(int(obj['difficult'])),
                                  difficult.index(int(obj['truncated']))])

                # increment counter
                obj_counter += 1

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        if self.verbose:
            print('> Processing lists...')

        # process lists
        for i in range(len(self.classes)):
            imgs_per_class = [val[0] for j, val in enumerate(object_id) if val[1] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_class.append(imgs_per_class)

        for i in range(len(image_filenames)):
            boxes_per_img = [val[2] for j, val in enumerate(object_id) if val[0] == i]
            boxes_per_img = list(set(boxes_per_img)) # get unique values
            boxes_per_img.sort()
            list_boxes_per_image.append(boxes_per_img)

        for i in range(len(image_filenames)):
            objs_per_img = [j for j, val in enumerate(object_id) if val[0] == i]
            objs_per_img = list(set(objs_per_img)) # get unique values
            objs_per_img.sort()
            list_object_ids_per_image.append(objs_per_img)

        for i in range(len(self.classes)):
            objs_per_class = [j for j, val in enumerate(object_id) if val[1] == i]
            objs_per_class = list(set(objs_per_class)) # get unique values
            objs_per_class.sort()
            list_objects_ids_per_class.append(objs_per_class)

        objs_no_difficult = [j for j, val in enumerate(object_id) if val[4] == 0]
        objs_no_difficult.sort()
        list_objects_ids_no_difficult = objs_no_difficult

        objs_difficult = [j for j, val in enumerate(object_id) if val[4] == 1]
        objs_difficult.sort()
        list_objects_ids_difficult = objs_difficult

        objs_no_truncated= [j for j, val in enumerate(object_id) if val[5] == 0]
        objs_no_truncated.sort()
        list_objects_ids_no_truncated = objs_no_truncated

        objs_truncated = [j for j, val in enumerate(object_id) if val[5] == 1]
        objs_truncated.sort()
        list_objects_ids_truncated = objs_truncated


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['id'] = np.array(obj_id, dtype=np.int32)
        handler['image_id'] = np.array(image_id, dtype=np.int32)
        handler['category_id'] = np.array(category_id, dtype=np.int32)
        handler['sizes'] = np.array(size, dtype=np.int32)
        handler['classes'] = str2ascii(self.classes)
        handler['boxes'] = np.array(bbox, dtype=np.float)
        handler['truncated'] = np.array(truncated, dtype=np.int32)
        handler['difficult'] = np.array(difficult, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_image_filenames_per_class'] = np.array(pad_list(list_image_filenames_per_class, -1), dtype=np.int32)
        handler['list_boxes_per_image'] = np.array(pad_list(list_boxes_per_image, -1), dtype=np.int32)
        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)
        handler['list_objects_ids_per_class'] = np.array(pad_list(list_objects_ids_per_class, -1), dtype=np.int32)
        handler['list_objects_ids_no_difficult'] = np.array(list_objects_ids_no_difficult, dtype=np.int32)
        handler['list_objects_ids_difficult'] = np.array(list_objects_ids_difficult, dtype=np.int32)
        handler['list_objects_ids_no_truncated'] = np.array(list_objects_ids_no_truncated, dtype=np.int32)
        handler['list_objects_ids_truncated'] = np.array(list_objects_ids_truncated, dtype=np.int32)