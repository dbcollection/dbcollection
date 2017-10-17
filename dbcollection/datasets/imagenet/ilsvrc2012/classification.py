"""
ImageNet ILSVRC 2012 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import PIL
from PIL import Image
import progressbar

from dbcollection.datasets import BaseTask

from dbcollection.utils.file_load import load_txt, load_matlab
from dbcollection.utils.os_dir import construct_set_from_dir, dir_get_size
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Classification(BaseTask):
    """ImageNet ILSVRC 2012 Classification preprocessing functions."""

    # metadata filename
    filename_h5 = 'classification'

    dirnames_train = ['ILSVRC2012_img_train', 'train']
    dirnames_val = ['ILSVRC2012_img_val', 'val']

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
        return load_txt(self.get_file_path('ILSVRC2012_validation_ground_truth.txt'))

    def load_annotations_mat(self):
        """
        Load ILSVRC2012 annotations (.mat file).
        """
        # load annotation file
        filename = self.get_file_path('meta.mat')
        return load_matlab(filename)

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
            filename_ = os.path.join(self.data_path, filename)
            idx = indexes[i] - 1  # matlab data is 1-indexed
            class_name = annot['synsets'][idx][0][1].tolist()[0]

            # add filename and class
            try:
                set_data[class_name].append(filename_)
            except KeyError:
                set_data[class_name] = [filename_]

            if self.verbose:
                # update progress bar
                counter += 1
                if counter % 1000 == 0:
                    prgbar.update(counter)

        # force progressbar to 100%
        if self.verbose:
            prgbar.finish()

        return set_data

    def sort(self, data):
        """
        Sort the data's filenames.
        """
        for cname in data:
            data[cname].sort()
        return data

    def setup_dirs(self):
        """
        Resize all images in a directory.
        """
        # do nothing

    def load_data(self):
        """
        Load the data from the files.
        """
        # setup dirs (used only for raw256)
        self.setup_dirs()

        # load annotations
        if self.verbose:
            print('\n==> Fetching annotations + image files...')
        annotations = self.get_annotations()

        # get correct set paths
        dir_paths = {
            "train": self.get_dir_path(self.dirnames_train),
            "val": self.get_dir_path(self.dirnames_val)
        }

        # cycle the train and val data
        for set_name in dir_paths:
            data_dir = dir_paths[set_name]

            if set_name is 'train':
                data = construct_set_from_dir(data_dir, self.verbose)
            else:
                _, folders = dir_get_size(data_dir)
                if folders > 0:
                    data = construct_set_from_dir(data_dir, self.verbose)
                else:
                    data = self.fetch_val_dir_data(data_dir)

            # sort filenames
            data = self.sort(data)

            yield {set_name: data}

    def store_data_source(self, hdf5_handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        # progress bar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(data)).start()
            counter = 0

        sourceg = hdf5_handler.create_group('source/' + set_name)

        # cycle all classes from the data with the original annotations
        for cname in data:
            images_filenames = [os.path.join(set_name, cname, fname) for fname in data[cname]]
            images_filenames.sort()
            hdf5_write_data(sourceg, cname + '/' + 'image_filenames',
                            str2ascii(images_filenames), dtype=np.uint8, fillvalue=0)

            # update progress bar
            if self.verbose:
                counter += 1
                prgbar.update(counter)

        # force progressbar to 100%
        if self.verbose:
            prgbar.finish()

    def convert_data_to_arrays(self, data, set_name):
        """
        Convert folders/filenames to arrays.
        """
        # load annotations
        annotations = self.get_annotations()

        # intialize lists
        classes = list(data.keys())
        classes.sort()
        label_list = [annotations[cname]['label'] for _, cname in enumerate(classes)]
        description_list = [annotations[cname]['description'] for _, cname in enumerate(classes)]
        object_ids = []
        filenames = []
        list_image_filenames_per_class = []

        # cycle all classes
        count_fname = 0
        for class_id, cname in enumerate(classes):
            range_ini = len(filenames)

            for filename in data[cname]:
                filenames.append(os.path.join(self.data_path, set_name, cname, filename))
                object_ids.append([count_fname, class_id])
                count_fname += 1

            # organize filenames by class id
            list_image_filenames_per_class.append(list(range(range_ini, len(filenames))))

        # pad list with zeros in order to have all lists of the same size
        list_image_filenames_per_class = pad_list(list_image_filenames_per_class, -1)

        return {
            "classes": str2ascii(classes),
            "labels": str2ascii(label_list),
            "image_filenames": str2ascii(filenames),
            "descriptions": str2ascii(description_list),
            "object_fields": str2ascii(['image_filenames', 'classes']),
            "object_ids": np.array(object_ids, dtype=np.int32),
            "list_image_filenames_per_class": np.array(list_image_filenames_per_class,
                                                       dtype=np.int32)
        }

    def add_data_to_source(self, hdf5_handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        self.store_data_source(hdf5_handler, data, set_name)

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        data_array = self.convert_data_to_arrays(data, set_name)
        hdf5_write_data(hdf5_handler, 'image_filenames',
                        data_array["image_filenames"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'classes', data_array["classes"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'labels', data_array["labels"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'descriptions',
                        data_array["descriptions"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data_array["object_ids"], dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data_array["object_fields"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_image_filenames_per_class',
                        data_array["list_image_filenames_per_class"], dtype=np.int32, fillvalue=-1)


# ---------------------------------------------------------
#  Resized images to 256px
# ---------------------------------------------------------

class Raw256(Classification):
    """ImageNet ILSVRC 2012 Classification raw256 preprocessing functions."""

    # metadata filename
    filename_h5 = 'raw256'

    new_dir_train = 'train256'
    new_dir_val = 'val256'

    dirnames_train = ['ILSVRC2012_img_train', 'train']
    dirnames_val = ['ILSVRC2012_img_val', 'val']

    def dir_resize_images(self, new_data_dir, data_dir):
        """
        Resize all images from the dir.
        """
        # fetch all files and folders of the original folder
        data_dir_ = self.get_dir_path(data_dir)
        data = construct_set_from_dir(data_dir_, self.verbose)

        base_size = 256

        # progress bar
        if self.verbose:
            progbar = progressbar.ProgressBar(max_value=len(data)).start()
            counter = 0

        # cycle all folders and files + resize images + store to the new directory
        for cname in data:
            for fname in data[cname]:
                save_dir = os.path.join(new_data_dir, cname)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                img_filename = os.path.join(data_dir_, cname, fname)
                new_img_filename = os.path.join(save_dir, fname)

                # load img
                img = Image.open(img_filename)

                # resize img
                height, width = img.size[0], img.size[1]
                if height > width:
                    wsize = 256
                    hsize = int(height * 256 / width)
                else:
                    hsize = 256
                    wsize = int(width * 256 / height)

                img = img.resize((hsize, wsize), PIL.Image.ANTIALIAS)

                # save img
                img.save(new_img_filename)

            # update progress bar
            if self.verbose:
                counter += 1
                progbar.update(counter)

        # force progressbar to 100%
        if self.verbose:
            progbar.finish()
            print('')

    def setup_dirs(self):
        """
        Setup new train/val directories and resize all images.
        """
        if self.verbose:
            print('==> Setup resized data dirs + images:')

        sets = {
            "train": [self.new_dir_train, self.dirnames_train],
            "val": [self.new_dir_val, self.dirnames_val]
        }

        for set_name in sets:
            # setup new directory
            new_data_dir = os.path.join(self.data_path, sets[set_name][0])
            if not os.path.exists(new_data_dir):
                os.makedirs(new_data_dir)
            else:
                continue  # skip this set

            # resize all images and save into the new directory
            if self.verbose:
                print(' > Resizing images for the set: {}'.format(set_name))
            self.dir_resize_images(new_data_dir, sets[set_name][1])
