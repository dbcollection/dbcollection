"""
Pascal VOC 2007 object detection processing functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.file_load import load_xml
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Detection:
    """ Pascal VOC 2007 object detection task class """

    # object classes
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',  \
               'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',\
               'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose

        # paths
        self.annotations_path = os.path.join(self.data_path, 'VOCdevkit', 'VOC2007', 'Annotations')
        self.images_path = os.path.join('VOCdevkit', 'VOC2007', 'JPEGImages')


    def sets_ids(self):
        """
        Return the train/val/test/trainval set id lists.
        """
        from .set_indexes import train_ids, val_ids, trainval_ids, test_ids

        return {
            'train' : train_ids,
            'val' : val_ids,
            'trainval' : trainval_ids,
            'test' : test_ids
        }


    def load_data(self):
        """
        Load data of the dataset.
        """
        # set id list
        set_indexes = self.sets_ids()

        for set_name in set_indexes:

            # index list
            id_list = set_indexes[set_name]

            data = []

            if self.verbose:
                print('\n==> Processing metadata for the set: {}'.format(set_name))

            # progressbar
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(id_list))

            for i, fileid in enumerate(id_list):
                # setup file names
                annot_filename = os.path.join(self.annotations_path, fileid + '.xml')
                image_filename = os.path.join(self.images_path, fileid + '.jpg')

                # load annotation
                annotation = load_xml(annot_filename)

                data.append([image_filename, annotation])

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

            # reset progressbar
            if self.verbose:
                prgbar.finish()

            yield {set_name : data}


    def add_data_to_source(self, handler, data):
        """
        Add data of a set to the source group.
        """

        def add_data_hdf5(handler, object):
            """Add data to the hdf5 file."""
            handler['name'] = object['name']
            handler['pose'] = object['pose']
            handler['truncated'] = object['truncated']
            handler['difficult'] = object['difficult']
            handler['bndbox/xmin'] = object['bndbox']['xmin']
            handler['bndbox/ymin'] = object['bndbox']['ymin']
            handler['bndbox/xmax'] = object['bndbox']['xmax']
            handler['bndbox/ymax'] = object['bndbox']['ymax']

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, data_ in enumerate(data):
            image_filename, annotation = data_

            file_grp = handler.create_group(str(i))

            file_grp['image_filename'] = image_filename
            file_grp['size/width'] = annotation['annotation']['size']['width']
            file_grp['size/height'] = annotation['annotation']['size']['height']
            file_grp['size/depth'] = annotation['annotation']['size']['depth']
            file_grp['segmented'] = annotation['annotation']['segmented']

            if isinstance(annotation['annotation']['object'], list):
                for j in range(len(annotation['annotation']['object'])):
                    object_grp = file_grp.create_group('object/{}/'.format(j))
                    obj = annotation['annotation']['object'][j]
                    add_data_hdf5(object_grp, obj)
            else:
                object_grp = file_grp.create_group('object/0/')
                obj = annotation['annotation']['object']
                add_data_hdf5(object_grp, obj)

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
        object_fields = ['image_filenames', 'classes', 'bboxes', 'sizes', 'difficult', 'truncated']
        image_filenames = []
        size = []
        bbox = []
        truncated = [0, 1]
        difficult = [0, 1]
        object_id = []

        list_image_filenames_per_class = []
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
            image_filename, annotation = data_

            image_filenames.append(image_filename)

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
                bbox.append([obj['bndbox']['xmin'], obj['bndbox']['ymin'],
                             obj['bndbox']['xmax'], obj['bndbox']['ymax']])

                object_id.append([i, self.classes.index(obj['name']), obj_counter,
                                  i, difficult.index(int(obj['difficult'])),
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
        imgs_per_class = [val[0] for i in range(len(self.classes)) for j, val in enumerate(object_id) if val[1] == i]
        imgs_per_class = list(set(imgs_per_class)) # get unique values
        list_image_filenames_per_class.append(imgs_per_class)

        objs_per_img = [j for i in range(len(image_filenames)) for j, val in enumerate(object_id) if val[0] == i]
        objs_per_img.sort()
        list_object_ids_per_image.append(objs_per_img)

        objs_per_img = [j for i in range(len(self.classes)) for j, val in enumerate(object_id) if val[1] == i]
        objs_per_img.sort()
        list_objects_ids_per_class.append(objs_per_img)

        objs_no_difficult = [j for j, val in enumerate(object_id) if val[4] == 0]
        objs_no_difficult.sort()
        list_objects_ids_no_difficult.append(objs_no_difficult)

        objs_difficult = [j for j, val in enumerate(object_id) if val[4] == 1]
        objs_difficult.sort()
        list_objects_ids_difficult.append(objs_difficult)

        objs_no_truncated= [j for j, val in enumerate(object_id) if val[5] == 0]
        objs_no_truncated.sort()
        list_objects_ids_no_truncated.append(objs_no_truncated)

        objs_truncated = [j for j, val in enumerate(object_id) if val[5] == 1]
        objs_truncated.sort()
        list_objects_ids_truncated.append(objs_truncated)


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['sizes'] = np.array(size, dtype=np.int32)
        handler['classes'] = str2ascii(self.classes)
        handler['bboxes'] = np.array(bbox, dtype=np.float)
        handler['truncated'] = np.array(truncated, dtype=np.int32)
        handler['difficult'] = np.array(difficult, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_image_filenames_per_class'] = np.array(pad_list(list_image_filenames_per_class, 1), dtype=np.int32)
        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, 1), dtype=np.int32)
        handler['list_objects_ids_per_class'] = np.array(pad_list(list_objects_ids_per_class, 1), dtype=np.int32)
        handler['list_objects_ids_no_difficult'] = np.array(pad_list(list_objects_ids_no_difficult, 1), dtype=np.int32)
        handler['list_objects_ids_difficult'] = np.array(pad_list(list_objects_ids_difficult, 1), dtype=np.int32)
        handler['list_objects_ids_no_truncated'] = np.array(pad_list(list_objects_ids_no_truncated, 1), dtype=np.int32)
        handler['list_objects_ids_truncated'] = np.array(pad_list(list_objects_ids_truncated, 1), dtype=np.int32)


        if self.verbose:
            print('> Done.')


    def process_metadata(self):
        """
        Process metadata for the  and store it in a hdf5 file.
        """
        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'detection.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

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


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()