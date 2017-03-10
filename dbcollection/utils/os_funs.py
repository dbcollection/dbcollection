"""
OS functions.
"""


from __future__ import print_function
import os
import errno
import shutil
import progressbar


img_extensions = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG',
    '.ppm', '.PPM',
    '.bmp', '.BMP',
]


def delete_dir(dir_path, verbose=False):
    """Delete a directory and its contents.

    Parameters
    ----------
    dir_path : str
        Directory path on disk for deletion.
    verbose : bool
        Displays text information on the screen if True.

    Returns
    -------
        None

    Raises
    ------
    OSError
        If directory cannot be deleted.
    """
    if verbose:
        print('Deleting {} and all its contents...'.format(dir_path))
    try:
        shutil.rmtree(dir_path, ignore_errors=True)
    except OSError as err:
        if err.errno != errno.EEXIST: # errno.ENOENT = no such file or directory
            raise OSError('Unable to delete dir: {}'.format(dir_path))
    else:
        if verbose:
            print('Directory deleted successfully.')


def delete_file(fname):
    """Check if the path exists and remove the file.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
        None

    Raises
    ------
    OSError
        If file cannot be removed.
    """
    try:
        os.remove(fname)
    except OSError as err:
        if err.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise


def dir_get_size(dir_path):
    """Returns the number of files and subfolders in a directory.

    Parameters
    ----------
    dir_path : str
        Directory path on disk.

    Returns
    -------
    int
        Number of files in the folder.
    int
        Number of folders in the path.

    Raises
    ------
        None
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
        Directory path on disk to create the set structure.
    verbose : bool
        Prints messages to the screen (if True).

    Returns
    -------
    dict
        Set structure with keys as class names and values as image filenames.

    Raises
    ------
        None
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
        for root, _, fnames in sorted(os.walk(subdir_path)):
            class_name = dname #os.path.split(root)[-1] # folder name
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
        Directory path on disk to create the dataset structure.
    verbose : bool
        Prints messages to the screen (if True).

    Returns
    -------
    dict
        Dataset structure.

    Raises
    ------
        None
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
