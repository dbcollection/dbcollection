"""
Pascal VOC 2012 object detection processing functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from sklearn.model_selection import train_test_split

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.file_load import load_xml
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Detection(BaseTask):
    """ Pascal VOC 2012 object detection task class """

    # metadata filename
    filename_h5 = 'detection'

    # object classes
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
               'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
               'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

    parts = ['head', 'hand', 'foot']


    def sets_fnames(self):
        """
        Return the train/val/test/trainval set filenames.
        """
        #from .set_indexes import test as test_fnames
        from dbcollection.datasets.pascal.voc_2012.test_filenames import test as test_fnames
        test_fnames.sort()

        image_filenames = os.listdir(os.path.join(self.data_path, self.images_path))
        fnames = [os.path.splitext(fname)[0] for fname in image_filenames]
        fnames.sort()

        #if any([fname in test_fnames for fname in fnames]):
        if test_fnames[0] in fnames:
            # test set detected.
            trainval_fnames = [fname for fname in fnames if not fname in test_fnames]
            trainval_ids = [i for i, fname in enumerate(fnames) if fname in trainval_fnames]

            # split trainval into train + val (50-50 split)
            train_np, val_np = train_test_split(np.array(trainval_fnames), test_size=0.5)
            train_np.sort()
            val_np.sort()

            train_fnames = train_np.tolist()
            val_fnames = val_np.tolist()

            train_ids = [i for i, fname in enumerate(fnames) if fname in train_fnames]
            val_ids = [i for i, fname in enumerate(fnames) if fname in val_fnames]
            test_ids = [i for i, fname in enumerate(fnames) if fname in test_fnames]

            return {
                "train" : [train_fnames, train_ids],
                "val" : [val_fnames, val_ids],
                "trainval" : [trainval_fnames, trainval_ids],
                "test" : [test_fnames, test_ids]
            }
        else:
            # test set not available
            trainval_fnames = fnames
            trainval_ids = list(range(len(trainval_fnames)))

            # split trainval into train + val (50-50 split)
            train_np, val_np = train_test_split(np.array(trainval_fnames), test_size=0.5)
            train_np.sort()
            val_np.sort()

            train_fnames = train_np.tolist()
            val_fnames = val_np.tolist()

            train_ids = [i for i, fname in enumerate(fnames) if fname in train_fnames]
            val_ids = [i for i, fname in enumerate(fnames) if fname in val_fnames]

            return {
                "train" : [train_fnames, train_ids],
                "val" : [val_fnames, val_ids],
                "trainval" : [trainval_fnames, trainval_ids],
            }


    def load_data(self):
        """
        Load data of the dataset.
        """
        self.annotations_path = os.path.join(self.data_path, 'VOCdevkit', 'VOC2012', 'Annotations')
        self.images_path = os.path.join('VOCdevkit', 'VOC2012', 'JPEGImages')

        # set id list
        set_filenames_ids = self.sets_fnames()

        for set_name in set_filenames_ids:

            # index list
            fnames, set_ids = set_filenames_ids[set_name]

            data = []

            if self.verbose:
                print('\n==> Processing metadata for the set: {}'.format(set_name))
                print('> Loading data files...')

            # progressbar
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(fnames))

            for i, fname in enumerate(fnames):
                # setup file names
                annot_filename = os.path.join(self.annotations_path, fname + '.xml')
                image_filename = os.path.join(self.images_path, fname + '.jpg')

                # load annotation
                try:
                    annotation = load_xml(annot_filename)

                    if set_name != 'test':
                        if isinstance(annotation['annotation']['object'], list):
                            for j in range(len(annotation['annotation']['object'])):
                                if 'truncated' not in annotation['annotation']['object'][j]:
                                    annotation['annotation']['object'][j]['truncated'] = 0
                        else:
                            if 'truncated' not in annotation['annotation']['object']:
                                annotation['annotation']['object']['truncated'] = 0
                except OSError:
                    annotation = {}

                data.append([image_filename, set_ids[i], annotation])

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

        def add_data_hdf5(handler, anno, set_name):
            """Add single annotation data to the hdf5 file."""
            handler['category_id'] = self.classes.index(anno['name'])
            handler['name'] = anno['name']
            if not set_name == 'test':
                handler['pose'] = anno['pose']
                handler['truncated'] = anno['truncated']
                handler['difficult'] = anno['difficult']
            handler['bndbox/xmin'] = anno['bndbox']['xmin']
            handler['bndbox/ymin'] = anno['bndbox']['ymin']
            handler['bndbox/xmax'] = anno['bndbox']['xmax']
            handler['bndbox/ymax'] = anno['bndbox']['ymax']

            #if anno['part']:
            #    if isinstance(anno['part'], list):
            #        part_list = anno['part']
            #    else:
            #        part_list = [anno['part']]
            #
            #    for j, part in enumerate(part_list):
            #        part_group = handler.create_group('part/{}/'.format(j))
            #        part_group['name'] = part['name']
            #        part_group['bndbox/xmin'] = part['bndbox']['xmin']
            #        part_group['bndbox/ymin'] = part['bndbox']['ymin']
            #        part_group['bndbox/xmax'] = part['bndbox']['xmax']
            #        part_group['bndbox/ymax'] = part['bndbox']['ymax']

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        for i, data_ in enumerate(data):
            image_filename, fileid, annotation = data_

            file_grp = handler.create_group(str(i))

            file_grp['image_filename'] = image_filename
            file_grp['id'] = fileid

            if any(annotation):
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
                    add_data_hdf5(object_grp, obj, set_name)

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

            if any(annotation) and set_name != 'test':
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

                    #if annotation['annotation']['part']:
                    #    if isinstance(annotation['annotation']['part'], list):
                    #        part_list = annotation['annotation']['part']
                    #    else:
                    #        part_list = [annotation['annotation']['part']]
                    #
                    #    for j, part in enumerate(part_list):
                    #        part_group = handler.create_group('part/{}/'.format(j))
                    #        part_group['name'] = part['name']
                    #        part_group['bndbox/xmin'] = part['bndbox']['xmin']
                    #        part_group['bndbox/ymin'] = part['bndbox']['ymin']
                    #        part_group['bndbox/xmax'] = part['bndbox']['xmax']
                    #        part_group['bndbox/ymax'] = part['bndbox']['ymax']

                    if set_name != 'test':
                        object_id.append([i, class_id, obj_counter, i,
                                          difficult.index(int(obj['difficult'])),
                                          difficult.index(int(obj['truncated']))])
                    #else:
                    #    object_id.append([i, class_id, obj_counter, i])

                    # increment counter
                    obj_counter += 1
            else:
                object_id.append([i])
                obj_id.append(i)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        if not set_name == 'test':
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
        if not set_name == 'test':
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
        else:
            handler['object_ids'] = np.array(object_id, dtype=np.int32)
            handler['object_fields'] = str2ascii(['image_filenames'])

        if self.verbose:
            print('> Done.')


class DetectionNoSourceGrp(Detection):
    """ Pascal VOC 2007 object detection (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'detection_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing