"""
ImageNet ILSVRC 2012 classification raw256 process functions.
"""


from __future__ import print_function, division
import os
import PIL
from PIL import Image
import progressbar

from dbcollection.utils.os_dir import construct_set_from_dir, dir_get_size

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
            "train" : [self.new_dir_train, self.dirnames_train],
            "val" : [self.new_dir_val, self.dirnames_val]
        }

        for set_name in sets:
            # setup new directory
            new_data_dir = os.path.join(self.data_path, sets[set_name][0])
            if not os.path.exists(new_data_dir):
                os.makedirs(new_data_dir)

            # resize all images and save into the new directory
            if self.verbose:
                print(' > Resizing images for the set: {}'.format(set_name))
            self.dir_resize_images(new_data_dir, sets[set_name][1])


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