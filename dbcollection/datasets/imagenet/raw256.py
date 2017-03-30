"""
ImageNet ILSVRC 2012 classification raw256 process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.os_dir import construct_set_from_dir, dir_get_size
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list

from .classification import Classification


class Raw256:
    """ ImageNet ILSVRC 2012 Classification raw256 preprocessing functions """

    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose

        self.new_dir_train = 'train256'
        self.new_dir_val = 'val256'

        self.dirnames_train = ['ILSVRC2012_img_train', 'train']
        self.dirnames_val = ['ILSVRC2012_img_val', 'val']


    def dir_resize_images(self, new_data_dir):
        """
        Resize all images from the dir.
        """


    def setup_dirs(self):
        """
        Setup new train/val directories and resize all images.
        """
        for set_dir in [self.new_dir_train, self.new_dir_val]:
            # setup new directory
            new_data_dir = os.path.join(self.data_path, set_dir)
            if not os.path.exists(new_data_dir):
                os.makedirs(new_data_dir)

            # resize all images and save into the new directory
            self.dir_resize_images(new_data_dir)


    def run(self):
        """
        Run task processing.
        """
        # setup new train/val dirs + images
        self.setup_dirs()

        # setup classification class
        Classification(self.data_path, self.cache_path, self.verbose, [self.new_dir_train, self.new_dir_val])

        # use the classification task to fetch data from the new dirs
        return Classification.run('raw256.h5')