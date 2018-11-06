"""
This module contains scripts to download/process
all datasets available in dbcollection.

These scripts are self contained, meaning they can be imported
and used to manually setup a dataset.
"""


from __future__ import print_function
import os
import h5py
import numpy as np

from dbcollection.utils.hdf5 import HDF5Manager
from dbcollection.utils.url import download_extract_urls
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class BaseDataset(object):
    """Base class for download/processing a dataset.

    Parameters
    ----------
    data_path : str
        Path to the data directory.
    cache_path : str
        Path to the cache file
    extract_data : bool, optional
        Extracts the downloaded files if they are compacted.
    verbose : bool, optional
         Displays text information to the screen (if true).

    Attributes
    ----------
    data_path : str
        Path to the data directory.
    cache_path : str
        Path to the cache file
    extract_data : bool
        Extracts the downloaded files if they are compacted.
    verbose : bool
        Displays text information to the screen (if true).
    urls : list
        List of URL paths to download.
    keywords : list
        List of keywords to classify datasets.
    tasks : dict
        Dataset's tasks for processing.
    default_task : str
        Default task name.

    """

    urls = ()  # list of urls to download
    keywords = ()  # List of keywords to classify/categorize datasets in the cache.
    tasks = {}  # dictionary of available tasks to process
    default_task = ''  # Defines the default class

    def __init__(self, data_path, cache_path, extract_data=True, verbose=True):
        """Initialize class."""
        assert isinstance(data_path, str), "Must insert a valid data path"
        assert isinstance(cache_path, str), "Must insert a valid cache path"
        self.data_path = data_path
        self.cache_path = cache_path
        self.extract_data = extract_data
        self.verbose = verbose

    def download(self):
        """Downloads and extract files to disk.

        Returns
        -------
        tuple
            A list of keywords.

        """
        download_extract_urls(
            urls=self.urls,
            save_dir=self.data_path,
            extract_data=self.extract_data,
            verbose=self.verbose
        )

    def process(self, task='default'):
        """Processes the metadata of a task.

        Parameters
        ----------
        task : str, optional
            Name of the task.

        Returns
        -------
        dict
            Returns a dictionary with the task name as key and the filename as value.

        """
        task_ = self.parse_task_name(task)
        if self.verbose:
            print("\nProcessing '{}' task:".format(task_))
        hdf5_filename = self.process_metadata(task_)
        return {task_: {"filename": hdf5_filename, "categories": self.keywords}}

    def parse_task_name(self, task):
        """Parses the task name to a valid name."""
        if task == '' or task == 'default':
            return self.default_task
        else:
            return task

    def process_metadata(self, task):
        """Processes the metadata for a task.

        Parameters
        ----------
        task : str
            Name of the task.

        Returns
        -------
        str
            File name + path of the resulting HDFR5 metadata file of the task.
        """
        constructor = self.get_task_constructor(task)
        processer = constructor(data_path=self.data_path,
                                cache_path=self.cache_path,
                                verbose=self.verbose)
        return processer.run()

    def get_task_constructor(self, task):
        """Returns the class constructor for the input task.

        Parameters
        ----------
        task : str
            Name of the task.

        Returns
        -------
        BaseTask
            Constructor to process the metadata of a task.

        """
        assert task
        return self.tasks[task]


class BaseTask(object):
    """Base class for processing the metadata of a task of a dataset.

    Parameters
    ----------
    data_path : str
        Path to the data directory.
    cache_path : str
        Path to the cache file
    verbose : bool, optional
        Displays text information to the screen (if true).

    Attributes
    ----------
    data_path : str
        Path to the data directory of the dataset.
    cache_path : str
        Path to store the HDF5 metadata file of a dataset in the cache directory.
    verbose : bool
        Displays text information to the screen (if true).
    filename_h5 : str
        Name of the HDF5 file.
    hdf5_filepath : str
        File name + path of the HDF5 metadata file in disk.

    """

    filename_h5 = ''  # name of the task file

    def __init__(self, data_path, cache_path, verbose=True):
        """Initialize class."""
        assert data_path, "Must insert a valid data path"
        assert cache_path, "Must insert a valid cache path"
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose
        self.hdf5_filepath = self.get_hdf5_save_filename()
        self.hdf5_manager = None

    def get_hdf5_save_filename(self):
        """Builds the HDF5 file name + path on disk."""
        return os.path.join(self.cache_path, self.filename_h5 + '.h5')

    def run(self):
        """Main Method. Runs the task metadata processing.

        It creates an HDF5 file in disk to store the resulting
        subgroups of the dataset's set partitions (e.g., train/val/test/etc.).
        Then, it loads the dataset's raw metadata from disk into memory as a
        generator, retrieves the data fields obtained in the processing stage
        and saves them into an HDF5 file in disk.

        Returns
        -------
        str
            File name + path of the task's HDF5 metadata file.
        """
        self.setup_hdf5_manager()
        data_generator = self.load_data()
        self.process_metadata(data_generator)
        self.teardown_hdf5_manager()
        return self.hdf5_filepath

    def setup_hdf5_manager(self):
        """Sets up the metadata manager to store the processed data to disk."""
        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(self.hdf5_filepath))
        self.hdf5_manager = HDF5Manager(filename=self.hdf5_filepath)

    def load_data(self):
        """Loads the dataset's (meta)data from disk (create a generator).

        Load data from annnotations and split it to corresponding
        sets (train, val, test, etc.)

        Returns
        -------
        generator
            A sequence of dictionary objects with a key-value pair
            with the name of the set split and the data.

        """
        pass  # stub

    def process_metadata(self, data_generator):
        """Processes the dataset's (meta)data and stores it into an HDF5 file."""
        for data in data_generator:
            for set_name in data:
                if self.verbose:
                    print('\nSaving set metadata: {}'.format(set_name))
                self.process_set_metadata(data[set_name], set_name)

    def process_set_metadata(self, data, set_name):
        """Sets up the set's data fields to be stored in the HDF5 metadata file.

        All fields set in this method are organized as a single big matrix.
        This results in much faster data retrieval than by transversing nested
        groups + datasets in an HDF5 file.

        Parameters
        ----------
        data : dict
            Dictionary containing the data annotations of a set split.
        set_name : str
            Name of the set split.

        """
        pass

    def teardown_hdf5_manager(self):
        """Sets up the MetadataManager object to manage the metadata save process to disk."""
        self.hdf5_manager.close()


class BaseField(object):
    """Base class for the dataset's data fields processor."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save_field_to_hdf5(self, set_name, field, data, **kwargs):
        """Saves data of a field into the HDF% metadata file.

        Parameters
        ----------
        set_name: str
            Name of the set split.
        field : str
            Name of the data field.
        data : np.ndarray
            Numpy ndarray of the field's data.

        """
        self.hdf5_manager.add_field_to_group(
            group=set_name,
            field=field,
            data=data,
            **kwargs
        )


class BaseColumnField(BaseField):
    """Base class for the dataset's column data field processor."""

    fields = []

    def process(self):
        """Processes and saves the columns metadata to hdf5."""
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='__COLUMNS__',
            data=str2ascii(self.fields),
            dtype=np.uint8,
            fillvalue=0
        )


class BaseMetadataField(BaseField):
    """Base class for the dataset's metadata field processor."""

    fields = []

    def process(self):
        """Processes and saves the metadata name and types info to hdf5."""
        self.save_fields_names()
        self.save_fields_types()

    def save_fields_names(self):
        columns = [field['name'] for field in self.fields]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='__COLUMNS__',
            data=str2ascii(columns),
            dtype=np.uint8,
            fillvalue=0
        )

    def save_fields_types(self):
        columns = [field['type'] for field in self.fields]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='__TYPES__',
            data=str2ascii(columns),
            dtype=np.uint8,
            fillvalue=0
        )


class BaseMetadataField(BaseField):
    """Base class for the dataset's metadata field processor."""

    fields = []

    def process(self):
        """Processes and saves the metadata name and types info to hdf5."""
        self.save_fields_names()
        self.save_fields_types()

    def save_fields_names(self):
        columns = [field['name'] for field in self.fields]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='__COLUMNS__',
            data=str2ascii(columns),
            dtype=np.uint8,
            fillvalue=0
        )

    def save_fields_types(self):
        columns = [field['type'] for field in self.fields]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='__TYPES__',
            data=str2ascii(columns),
            dtype=np.uint8,
            fillvalue=0
        )
