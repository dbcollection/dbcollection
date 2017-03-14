"""
ImageNet ILSVRC 2012 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.utils.storage import StorageHDF5
from dbcollection.utils.file_load import load_txt, load_matlab
from dbcollection.utils.os import construct_set_from_dir, dir_get_size
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class Classification:
    """ Imagenet ILSVRC 2012 Classification preprocessing functions """

    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose

        self.fname_val_groundtruth_idx = 'ILSVRC2012_validation_ground_truth.txt'
        self.fname_metadata = 'meta.mat'
        self.dirnames_train = ['ILSVRC2012_img_train', 'train']
        self.dirnames_val = ['ILSVRC2012_img_val', 'val']


    def get_file_path(self, fname):
        """
        Get file path for a file from the the root tree.
        """
        for root, dirnames, filenames in os.walk(self.data_path):
            if fname in filenames:
                return os.path.join(root, fname)

        raise Exception('Could not find file {} in {}'.format(fname, self.data_path))


    def load_annotations_groundtruth(self):
        """
        Load ILSVRC2012 ground truth indexes.
        """
        return load_txt(self.get_file_path(self.fname_val_groundtruth_idx))


    def load_annotations_mat(self):
        """
        Load ILSVRC2012 annotations (.mat file).
        """
        # load annotation file
        return load_matlab(self.get_file_path(self.fname_metadata))


    def get_annotations(self):
        """
        Load+parse annotations .mat file.
        """
        # load annotation file
        annot = self.load_annotations_mat()

        # convert into a dictionary
        annotations = {}
        for i in range(len(annot['synsets'])):
            folder = annot['synsets'][i][0][1].tolist()[0]
            label = annot['synsets'][i][0][2].tolist()[0]
            description = annot['synsets'][i][0][3].tolist()[0]
            annotations[folder] = {
                "label": label,
                "description": description
            }

        return annotations


    def get_dir_path(self, dirname):
        """
        Check if a dir or list of dirs exists
        """
        # get correct set paths
        for name in dirname:
            train_dir = os.path.join(self.data_path, name)
            if os.path.isdir(train_dir):
                return train_dir

        raise Exception('Cannot find dir: {}'.format(dirname))


    def fetch_val_dir_data(self, dirname):
        """
        Fetch the validation dir's files+annotations (original format).
        """
        # fetch all filenames
        filenames = os.listdir(dirname)
        filenames.sort()

        # fetch filenames annotations
        annot = self.load_annotations_mat()
        indexes = self.load_annotations_groundtruth()
        indexes = [int(val) for val in indexes if val != '']

        # progress bar
        if self.verbose:
            counter = 0
            prgbar = progressbar.ProgressBar(max_value=len(filenames))

        # cycle all filenames and assign them the correct class
        set_data = {}
        for i, filename in enumerate(filenames):
            idx = indexes[i]
            class_name = annot['synsets'][idx][0][1].tolist()[0]

            # add filename and class
            try:
                set_data[class_name].append(filename)
            except KeyError:
                set_data[class_name] = [filename]

            if self.verbose:
                # update progress bar
                counter += 1
                if counter % 1000 == 0:
                    prgbar.update(counter)

        return set_data


    def process_set(self, data):
        """
        Process the data into arrays for storage.
        """
        # load annotations
        annotations = self.get_annotations()

        # combine class name, label and description elems into lists
        class_list = list(data.keys())
        label_list = [annotations[classname]['label'] for classname in class_list]
        description_list = [annotations[classname]['description'] for classname in class_list]

        # progress bar
        if self.verbose:
            counter = 0
            prgbar = progressbar.ProgressBar(max_value=len(class_list))


        # group all filenames into a list
        filenames = []
        class_id = []
        object_id = []
        list_class_fname = []
        for cname in data:
            range_ini = len(filenames) + 1
            for filename in data[cname]:
                filenames.append(filename)
                class_id.append(class_list.index(cname))
                object_id.append([len(filenames)-1, class_id[-1]])

            # organize filenames by class id
            list_class_fname.append(list(range(range_ini, len(filenames))))

            # update progress bar
            if self.verbose:
                counter += 1
                prgbar.update(counter)

        # pad list with zeros in order to have all lists of the same size
        max_size = len(max(list_class_fname, key=len))
        list_class_fname = [l + [0]*(max_size-len(l)) for l in list_class_fname]

        return {
            "object_fields": str2ascii(['image_filename', 'class_name']),
            "class_names": str2ascii(class_list),
            "labels": str2ascii(label_list),
            "descriptions": str2ascii(description_list),
            "image_filenames": str2ascii(filenames),
            "class_ids": np.array(class_id, dtype=np.int32),
            "object_ids": np.array(object_id, dtype=np.int32),
            "list_classes_filenames": np.array(list_class_fname, dtype=np.int32)
        }


    def load_data(self):
        """
        Load the data from the files.
        """
        # load annotations
        if self.verbose:
            print('\n==> Fetching annotations...')
        annotations = self.get_annotations()

        # get correct set paths
        train_dir = self.get_dir_path(self.dirnames_train)
        val_dir = self.get_dir_path(self.dirnames_val)

        #============
        # Train set
        #============
        if self.verbose:
            print('\n==> Fetch train set data from dir: {}'.format(train_dir))
        train_data = construct_set_from_dir(train_dir, self.verbose)
        if self.verbose:
            print('\n==> Process train set data... ')
        train_processed = self.process_set(train_data)

        #==========
        # Val set
        #==========
        # check if the val dir is in the original format or in a converted format
        if self.verbose:
            print('\n==> Fetch val set data from dir: {}'.format(val_dir))
        _, folders = dir_get_size(val_dir)
        if folders > 0:
            val_data = construct_set_from_dir(val_dir, self.verbose)
        else:
            val_data = self.fetch_val_dir_data(val_dir)
        if self.verbose:
            print('==> Process train set data... ')
        val_processed = self.process_set(val_data)

        return {
            "train": {
                "nested": train_data,
                "flattened": train_processed
            },
            "val": {
                "nested": val_data,
                "flattened": val_processed
            }
        }


    def hdf5_add_data_source(self, handler, data, set_name):
        """
        Add data to the HDF5 file in a nested format (folder-like).
        """
        # set pointer
        data_ = data[set_name]["nested"]

        # progress bar
        if self.verbose:
            counter = 0
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        # cycle all classes from the data with the original annotations
        for cname in data_:
            for i, filename in enumerate(data_[cname]):
                handler.add_data('source/' + set_name +'/images/' + cname, str(i), str2ascii(filename), np.uint8)

            # update progress bar
            if self.verbose:
                counter += 1
                prgbar.update(counter)

        handler.add_data('source/' + set_name, "classes", data[set_name]["flattened"]["class_names"])
        handler.add_data('source/' + set_name, "labels", data[set_name]["flattened"]["labels"])
        handler.add_data('source/' + set_name, "descriptions", data[set_name]["flattened"]["descriptions"])


    def classification_metadata_process(self):
        """
        Process metadata and store it in a hdf5 file.
        """
        if self.verbose:
            print('\nLoading data...')
        # load data to memory
        data = self.load_data()

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'classification.h5')
        if self.verbose:
            print('\nWritting data to file: {}'.format(file_name))
        fileh5 = StorageHDF5(file_name, 'w')

        if self.verbose:
            print('==> Writing train set data...')

        # add data to the **list** group
        fileh5.add_data('default/train', 'classes', data["train"]["flattened"]["class_names"], np.uint8)
        fileh5.add_data('default/train', 'labels', data["train"]["flattened"]["labels"], np.uint8)
        fileh5.add_data('default/train', 'descriptions', data["train"]["flattened"]["descriptions"], np.uint8)
        fileh5.add_data('default/train', 'image_filenames', data["train"]["flattened"]["image_filenames"], np.uint8)
        fileh5.add_data('default/train', 'class_ids', data["train"]["flattened"]["class_ids"])
        fileh5.add_data('default/train', 'object_ids', data["train"]["flattened"]["object_ids"])
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('default/train', 'object_fields', data["train"]["flattened"]['object_fields'], np.uint8)

        # add data to the **source** group
        self.hdf5_add_data_source(fileh5, data, "train")

        if self.verbose:
            print('\n==> Writing val set data...')

        # add data to the **list** group
        fileh5.add_data('default/val', 'classes', data["val"]["flattened"]["class_names"], np.uint8)
        fileh5.add_data('default/val', 'labels', data["val"]["flattened"]["labels"], np.uint8)
        fileh5.add_data('default/val', 'descriptions', data["val"]["flattened"]["descriptions"], np.uint8)
        fileh5.add_data('default/val', 'image_filenames', data["val"]["flattened"]["image_filenames"], np.uint8)
        fileh5.add_data('default/val', 'class_ids', data["val"]["flattened"]["class_ids"])
        fileh5.add_data('default/val', 'object_ids', data["val"]["flattened"]["object_ids"])
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('default/val', 'object_fields', data["val"]["flattened"]['object_fields'], np.uint8)

        # add data to the **source** group
        self.hdf5_add_data_source(fileh5, data, "val")


        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.classification_metadata_process()