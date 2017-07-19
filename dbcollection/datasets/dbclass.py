"""
Base class for download/processing a dataset.
"""


from __future__ import print_function
import os
import h5py

from dbcollection.utils.url import download_extract_all


#---------------------------------------------------------
# Dataset setup
#---------------------------------------------------------

class BaseDataset:
    """ Base class for download/processing a dataset. """

    # download url
    url = [] # list of urls to download
    md5_checksum = '' # list of md5 hashes to validate the urls.
                      # If not available, leave it empty ([] or '')

    # some keywords. These are used to classify datasets for easier
    # categorization in the cache file.
    keywords = []

    # init tasks
    tasks = {} # dictionary of available tasks to process
               # Example: tasks = {'classification':Classification}
    default_task = '' # Should define a default class!
                      # Example: default_task='classification'

    def __init__(self, data_path, cache_path, extract_data, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.extract_data = extract_data
        self.verbose = verbose


    def download(self):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        download_extract_all(self.url, self.md5_checksum, self.data_path,
                             self.extract_data, self.verbose)

        return self.keywords


    def fetch_task_key(self):
        """
        Return the first key that appears on the dictionary.
        """
        for task in self.tasks:
            return task


    def parse_task_name(self, task):
        """
        Parses the task string to look for key suffixes.
        """
        if task.endswith('_s'):
            return task[:-2], '_s'
        else:
            return task, None


    def init_tasks_constructors(self, suffix=None):
        """
        Initialize the tasks' class constructor.
        """
        assert any(self.tasks), 'No defined tasks for process. Please insert a task for processing.'

        tasks_init = {}
        for task in self.tasks:
            tasks_init[task] = self.tasks[task](self.data_path, self.cache_path, suffix, self.verbose)

        if self.default_task == '':
            self.default_task = self.fetch_task_key()

        tasks_init['default'] = tasks_init[self.default_task]

        return tasks_init


    def get_all_tasks(self):
        """
        Returns a list of all available tasks
        """
        # init tasks
        tasks_loader = self.init_tasks_constructors()

        tasks = []
        for i, task in enumerate(tasks_loader):
            tasks.append(task)

        return tasks


    def process(self, task='default'):
        """
        Process metadata for all tasks
        """
        info_output = {}
        if task == 'all':
            tasks_loader = self.init_tasks_constructors()
            for i, task in enumerate(tasks_loader):

                if self.verbose:
                    print('\nProcessing ::{}:: task: ({}/{})'.format(task, i+1, len(tasks_loader)))
                info_output[task] = tasks_loader[task].run()
        else:
            task_, suffix = self.parse_task_name(task)

            if self.verbose:
                print('\nProcessing ::{}:: task:'.format(task_))
            tasks_loader = self.init_tasks_constructors(suffix)
            info_output[task] = tasks_loader[task_].run()

        return info_output, self.keywords


#---------------------------------------------------------
# Task setup
#---------------------------------------------------------

class BaseTask:
    """ Base class for processing a task of a dataset. """

    # name of the task file
    filename_h5 = 'task'


    def __init__(self, data_path, cache_path, suffix=None, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose
        self.suffix = suffix


    def load_data(self):
        """
        Load data of the dataset (create a generator).

        Load data from annnotations and split it to corresponding
        sets (train, val, test, etc.)
        """
        pass  # stub


    def add_data_to_source(self, handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        pass  # stub


    def add_data_to_default(self, handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        pass  # stub


    def process_metadata(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # create/open hdf5 file with subgroups for train/val/test
        if self.suffix:
            file_name = os.path.join(self.cache_path, self.filename_h5 + self.suffix + '.h5')
        else:
            file_name = os.path.join(self.cache_path, self.filename_h5 + '.h5')
        fileh5 = h5py.File(file_name, 'w', libver='latest')

        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(file_name))

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                if self.verbose:
                    print('\nSaving set metadata: {}'.format(set_name))

                # add data to the **source** group
                if self.suffix is '_s':
                    sourceg = fileh5.create_group('source/' + set_name)
                    self.add_data_to_source(sourceg, data[set_name], set_name)

                # add data to the **default** group
                defaultg = fileh5.create_group('default/' + set_name)
                self.add_data_to_default(defaultg, data[set_name], set_name)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()