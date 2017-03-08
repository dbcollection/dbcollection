"""
Pascal VOC 2007 download/process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar
from ... import utils, storage


class PascalVOC2007:
    """ Pascal VOC 2007 preprocessing/downloading class """

    # download url
    url = [
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar',
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar',
    ]
    md5_checksum = []

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'object_detection']

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
        from .voc_2007_indexes import train_ids, val_ids, trainval_ids, test_ids

        self.ids = {
            'train' : train_ids,
            'val' : val_ids,
            'trainval' : trainval_ids,
            'test' : test_ids
        }


    def download(self, is_download=True):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        if is_download:
            utils.download_extract_all(self.url, self.md5_checksum, self.data_path, False, self.verbose)

        return self.keywords


    def set_add_data_source(self, hdf5_handler, id_list):
        """
        Load+parse annotations of a set and store the metadata in the
        orignal annotation form (nested).
        """

        def add_data_hdf5(handler, object, root):
            """Add data to the hdf5 file."""
            handler[root + 'name'] = obj['name']
            handler[root + 'pose'] = obj['pose']
            handler[root + 'truncated'] = obj['truncated']
            handler[root + 'difficult'] = obj['difficult']
            handler[root + 'bndbox/xmin'] = obj['bndbox']['xmin']
            handler[root + 'bndbox/ymin'] = obj['bndbox']['ymin']
            handler[root + 'bndbox/xmax'] = obj['bndbox']['xmax']
            handler[root + 'bndbox/ymax'] = obj['bndbox']['ymax']


        # progressbar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(id_list))

        for i, fileid in enumerate(id_list):
            # setup file names
            annot_filename = os.path.join(self.annotations_path, fileid + '.xml')
            image_filename = os.path.join(self.images_path, fileid + '.jpg')

            # load annotation
            annotation = utils.load_xml(annot_filename)

            # add data to the set
            root_path = '{}/'.format(i)
            hdf5_handler[root_path + 'filename'] = image_filename

            hdf5_handler[root_path + 'size/width'] = annotation['annotation']['size']['width']
            hdf5_handler[root_path + 'size/height'] = annotation['annotation']['size']['height']
            hdf5_handler[root_path + 'size/depth'] = annotation['annotation']['size']['depth']

            hdf5_handler[root_path + 'segmented'] = annotation['annotation']['segmented']

            if isinstance(annotation['annotation']['object'], list):
                for j in range(0, len(annotation['annotation']['object'])):
                    subroot_path = root_path + 'object/{}/'.format(j)
                    obj = annotation['annotation']['object'][j]
                    add_data_hdf5(hdf5_handler, obj, subroot_path)
            else:
                subroot_path = root_path + 'object/0/'
                obj = annotation['annotation']['object']
                add_data_hdf5(hdf5_handler, obj, subroot_path)

            # update progressbar
            if self.verbose:
                prgbar.update(i)


    def set_add_data_default(self, hdf5_handler, id_list):
        """
        Load+parse annotations of a set and store the metadata in the
        orignal annotation form.
        """
        # var init
        image_filenames = []
        size = []
        bbox = []
        truncated = [0, 1]
        difficult = [0, 1]
        object_id = []
        object_fields = ['filename', 'class_name', 'bbox', 'size', 'difficult', 'truncated']

        # progressbar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(id_list))

        for i, fileid in enumerate(id_list):
            # setup file names
            annot_filename = os.path.join(self.annotations_path, fileid + '.xml')
            image_filename = os.path.join(self.images_path, fileid + '.jpg')

            # load annotation
            annotation = utils.load_xml(annot_filename)

            image_filenames.append(image_filename)

            width = annotation['annotation']['size']['width']
            height = annotation['annotation']['size']['height']
            depth = annotation['annotation']['size']['depth']
            size.append([depth, height, width])

            if isinstance(annotation['annotation']['object'], list):
                for j in range(0, len(annotation['annotation']['object'])):
                    obj = annotation['annotation']['object'][j]
                    bbox.append([obj['bndbox']['xmin'], obj['bndbox']['ymin'], obj['bndbox']['xmax'], obj['bndbox']['ymax']])
                    object_id.append([len(image_filenames), self.classes.index(obj['name']) + 1, \
                                      len(bbox), len(size), difficult.index(int(obj['difficult'])) + 1, \
                                      difficult.index(int(obj['truncated'])) + 1])
            else:
                obj = annotation['annotation']['object']
                bbox.append([obj['bndbox']['xmin'], obj['bndbox']['ymin'], obj['bndbox']['xmax'], obj['bndbox']['ymax']])
                object_id.append([len(image_filenames), self.classes.index(obj['name']) + 1, \
                                  len(bbox), len(size), difficult.index(int(obj['difficult'])) + 1, \
                                  difficult.index(int(obj['truncated'])) + 1])

            # update the progressbar
            if self.verbose:
                prgbar.update(i)

        # add data to the hdf5 file
        hdf5_handler['image_filenames'] = utils.convert_str_to_ascii(image_filenames)
        hdf5_handler['sizes'] = np.array(size, dtype=np.int32)
        hdf5_handler['classes'] = utils.convert_str_to_ascii(self.classes)
        hdf5_handler['bbox'] = np.array(bbox, dtype=np.float)
        hdf5_handler['truncated'] = np.array(truncated, dtype=np.int32)
        hdf5_handler['difficult'] = np.array(difficult, dtype=np.int32)
        hdf5_handler['object_ids'] = np.array(object_id, dtype=np.int32)
        hdf5_handler['object_fields'] = utils.convert_str_to_ascii(object_fields)


    def detection_metadata_process(self):
        """
        Process metadata for the  and store it in a hdf5 file.
        """
        # set id list
        self.sets_ids()

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'detection.h5')
        fileh5 = storage.StorageHDF5(file_name, 'w')

        for set_name in self.ids.keys():
            print('Processing set: {}'.format(set_name))
            # list of ids
            id_list = self.ids[set_name]

            # create set in the hdf5 file
            fileh5.add_group(set_name)
            fileh5.add_group(set_name + '/source')
            fileh5.add_group(set_name + '/default')

            # add data source (original)
            self.set_add_data_source(fileh5.storage[set_name + '/source/'], id_list)

            # add data default
            self.set_add_data_default(fileh5.storage[set_name + '/default/'], id_list)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def process(self):
        """
        Process metadata for all tasks
        """
        # object detection data parsing
        detection_filename = self.detection_metadata_process()

        info_output = {
            "default" : detection_filename,
            "detection" : detection_filename
        }

        return info_output, self.keywords