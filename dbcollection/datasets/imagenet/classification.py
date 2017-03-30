"""
ImageNet ILSVRC 2012 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.file_load import load_txt, load_matlab
from dbcollection.utils.os_dir import construct_set_from_dir, dir_get_size
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Classification:
    """ ImageNet ILSVRC 2012 Classification preprocessing functions """

    def __init__(self, data_path, cache_path, verbose=True, paths=None):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose

        self.fname_val_groundtruth_idx = 'ILSVRC2012_validation_ground_truth.txt'
        self.fname_metadata = 'meta.mat'
        if paths:
            assert os.path.isdir(paths[0]), 'Train directory does not exist: {}'.format(paths[0])
            assert os.path.isdir(paths[0]), 'Validation directory does not exist: {}'.format(paths[1])
            self.dirnames_train = [paths[0]]
            self.dirnames_val = [paths[1]]
        else:
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
            prgbar = progressbar.ProgressBar(max_value=len(filenames)).start()

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

        # force progressbar to 100%
        prgbar.finish()

        return set_data


    def load_data(self):
        """
        Load the data from the files.
        """
        # load annotations
        if self.verbose:
            print('\n==> Fetching annotations...')
        annotations = self.get_annotations()

        # get correct set paths
        dir_paths = {
            "train" : self.get_dir_path(self.dirnames_train),
            "val" : self.get_dir_path(self.dirnames_val)
        }

        # cycle the train and val data
        for set_name in dir_paths:
            data_dir = dir_paths[set_name]
            if self.verbose:
                print('\n==> Fetch set {} data from dir: {}'.format(set_name, data_dir))

            if set_name is 'train':
                data = construct_set_from_dir(data_dir, self.verbose)
            else:
                _, folders = dir_get_size(data_dir)
                if folders > 0:
                    data = construct_set_from_dir(data_dir, self.verbose)
                else:
                    data = self.fetch_val_dir_data(data_dir)

            yield {set_name : data}


    def store_data_source(self, handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        # progress bar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(data)).start()
            counter = 0

        sourceg = handler.create_group('source/' + set_name)

        # cycle all classes from the data with the original annotations
        for cname in data[set_name]:

            images_filenames = [os.path.join(set_name, cname, fname) for fname in data[set_name][cname]]
            images_filenames.sort()
            sourceg.create_dataset('image_filenames', data=str2ascii(images_filenames), dtype=np.uint8)

            # update progress bar
            if self.verbose:
                counter += 1
                prgbar.update(counter)

        # force progressbar to 100%
        prgbar.finish()


    def convert_data_to_arrays(self, data):
        """
        Convert folders/filenames to arrays.
        """
        # load annotations
        annotations = self.get_annotations()

        # intialize lists
        classes = list(data.keys())
        classes.sort()
        label_list = [annotations[cname]['label'] for cname in classes]
        description_list = [annotations[cname]['description'] for cname in classes]
        object_ids = []
        filenames = []
        list_image_filenames_per_class = []

        # progress bar
        if self.verbose:
            progbar = progressbar.ProgressBar(max_value=len(classes)).start()
            counter = 0

        # cycle all classes
        count_fname = 0
        for class_id, cname in enumerate(classes):
            range_ini = len(filenames)

            for filename in data[cname]:
                filenames.append(filename)
                object_ids.append([count_fname, class_id])
                count_fname += 1

            # organize filenames by class id
            list_image_filenames_per_class.append(list(range(range_ini, len(filenames))))

            # update progress bar
            if self.verbose:
                counter += 1
                progbar.update(counter)

        # force progressbar to 100%
        if self.verbose:
            progbar.finish()

        # pad list with zeros in order to have all lists of the same size
        list_image_filenames_per_video = pad_list(list_image_filenames_per_class, -1)

        return {
            "object_fields": str2ascii(['image_filename', 'class_name']),
            "classes": str2ascii(classes),
            "labels": str2ascii(label_list),
            "descriptions": str2ascii(description_list),
            "image_filenames": str2ascii(filenames),
            "object_ids": np.array(object_ids, dtype=np.int32),
            "list_image_filenames_per_class": np.array(list_image_filenames_per_class, dtype=np.int32)
        }


    def process_metadata(self, save_name):
        """
        Process metadata and store it in a hdf5 file.
        """
        # create/open hdf5 file with subgroups for train/val/test
        if save_name:
            file_name = os.path.join(self.cache_path, save_name)
        else:
            file_name = os.path.join(self.cache_path, 'classification.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(file_name))

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                if self.verbose:
                    print('Saving set metadata: {}'.format(set_name))

                # add data to the **source** group
                self.store_data_source(fileh5, data, set_name)

                 # add data to the **default** group
                data_array = self.convert_data_to_arrays(data[set_name])
                defaultg = fileh5.create_group('default/' + set_name)
                for field_name in data_array:
                    defaultg.create_dataset(field_name, data=data_array[field_name])

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self, save_name=None):
        """
        Run task processing.
        """
        return self.process_metadata(save_name)