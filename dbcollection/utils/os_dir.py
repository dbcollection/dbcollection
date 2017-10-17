"""
This module contains methods for parsing directories
"""


from __future__ import print_function
import os
import progressbar


img_extensions = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG',
    '.ppm', '.PPM',
    '.bmp', '.BMP',
]


def dir_get_size(dir_path):
    """Returns the number of files and subfolders in a directory.

    Parameters
    ----------
    dir_path : str
        Directory path.

    Returns
    -------
    int
        Number of files in the folder.
    int
        Number of folders in the path.

    """
    files = folders = 0
    for _, dirname, filenames in os.walk(dir_path):
        files += len(filenames)
        folders += len(dirname)
    return files, folders


def construct_set_from_dir(dir_path, verbose=True):
    """Build a dataset from a directory.

    This method creates a dataset from a root folder. The first child folders compose
    the dataset's classes and all files inside correspond to the
    data.

    Parameters
    ----------
    dir_path : str
        Directory path to create the set structure from.
    verbose : bool, optional
        Prints messages to the screen (if True).

    Returns
    -------
    dict
        Set structure with keys as class names and values as image filenames.

    """
    assert os.path.isdir(dir_path), 'Invalid path: {}'.format(dir_path)

    def is_image_file(filename):
        """Check if a filename has an extension of an image."""
        return any(filename.endswith(extension) for extension in img_extensions)

    # init set
    set_data = {}

    if verbose:
        print('Fetching files + subdirs from: {}'.format(dir_path))
        _, num_folders = dir_get_size(dir_path)
        counter = 0
        prgbar = progressbar.ProgressBar(max_value=num_folders)

    # cycle all elems in a dir
    for dname in os.listdir(dir_path):
        subdir_path = os.path.join(dir_path, dname)

        # check if it is a dir
        if not os.path.isdir(subdir_path):
            continue

        # cycle all elems in a dir
        for _, _, fnames in sorted(os.walk(subdir_path)):
            class_name = dname
            set_data[class_name] = []

            # cycle all files inside the dir
            for fname in fnames:
                if is_image_file(fname):
                    set_data[class_name].append(fname)

        if verbose:
            # update progress bar
            counter += 1
            prgbar.update(counter)

    return set_data


def construct_dataset_from_dir(dir_path, verbose=True):
    """Build a dataset from a directory.

    This method creates a dataset from a root folder. The first child
    folders compose the dataset's partition into train/val/test/etc.
    Then, child folders of these compose the dataset's classes and all
    files inside correspond to the data.

    Parameters
    ----------
    dir_path : str
        Directory path to create the dataset structure from.
    verbose : bool, optional
        Prints messages to the screen (if True).

    Returns
    -------
    dict
        Dataset structure.

    """
    assert os.path.isdir(dir_path), 'Invalid path: {}'.format(dir_path)

    # init images list
    dataset = {}

    # cycle all elems in a dir
    for set_name in os.listdir(dir_path):
        dir_set = os.path.join(dir_path, set_name)

        # check if it is a dir
        if not os.path.isdir(dir_set):
            continue

        # fetch all data for this set folder
        if verbose:
            print('Processing dir: {}'.format(dir_set))
        dataset[set_name] = construct_set_from_dir(dir_set)

    return dataset
