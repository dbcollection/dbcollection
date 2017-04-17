"""
Base class for download/processing a dataset.
"""


from __future__ import print_function
from dbcollection.utils.url import download_extract_all


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


    def init_tasks_constructors(self):
        """
        Initialize the tasks' class constructor.
        """
        assert any(self.tasks), 'No defined tasks for process. Please insert a task for processing.'
        tasks_init = {}
        for task in self.tasks:
            tasks_init[task] = self.tasks[task](self.data_path, self.cache_path, self.verbose)

        if self.default_task == '':
            self.default_task = self.fetch_task_key()

        tasks_init['default'] = tasks_init[self.default_task]

        return tasks_init


    def process(self, task='default'):
        """
        Process metadata for all tasks
        """
        # init tasks
        tasks_loader = self.init_tasks_constructors()

        info_output = {}
        if task == 'all':
            for i, task in enumerate(tasks_loader):
                if self.verbose:
                    print('Processing ::{}:: task: ({}/{})\n'.format(task, i+1, len(tasks_loader)))
                info_output[task] = tasks_loader[task].run()
        else:
            if self.verbose:
                print('Processing ::{}:: task:\n'.format(task))
            info_output[task] = tasks_loader[task].run()

        return info_output, self.keywords
