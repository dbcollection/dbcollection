.. _dev_create_new_dataset:

Creating a new dataset
======================

Creating a new dataset requires you to set the download and setup
scripts in a certain way. To create a new dataset simply create a
directory with the name of the dataset you will want to be called.

.. note:: Please use **snake_case** when naming the directory by using
          all characters in lower case and separated by an underscore.

Inside the folder there should be a ``__init__.py`` and one or more
files containing code to parse the data for a given task.
The `__init__.py`` file contains information about the urls, tasks
and keywords configs of the dataset. This requires you to set a special
class to define these parameters. To set this class you can use the
following setup:

.. code-block:: python

    """
    Brief description of the dataset
    """

    from dbcollection.datasets.dbclass import BaseDataset
    from .taskfile import TaskName

    class Dataset(BaseDataset):
        """ Name of the dataset """

        urls = ['http://url.something']
        keywords = ['some', 'keywords', 'for', 'grouping']
        tasks = {'some_task_name': TaskName}
        default_task = 'some_task_name'


To setup the new dataset's class you need to:


#. Write a short docstring indicating the purpose of the dataset (for image
   classification, object detection, action recognition, natural language
   processing, etc.)

#. Import ``BaseDataset`` from ``dbcollection.datasets.dbclass``

#. Import your task classes from your task files. In the above example
   the task ``TaskName`` was imported from a ``taskfile.py`` in the same
   directory as the ``__init__.py`` file.

#. Define a class called ``Dataset`` and inherit from ``BaseDataset``.
   It is required to name the class as ``Dataset`` in order for it to be
   included in the dataset list along with the rest of the other datasets.

#. Define a docstring inside the class with the name of the dataset.

#. Setup the ``urls``, ``keywords``, ``tasks`` and ``default_task`` fields.
   The ``urls`` field contains a list of urls of the data files to be downloaded.
   The ``keywords`` field contains a list of strings for helping in searching/grouping
   datasets for catalogging the existing datasets and their functionality. The
   ``tasks`` field is a dictionary containing all available tasks for the dataset, and
   the ``default_task`` simply tells which task name is the default if no name is
   set when loading/processing a dataset.
   These fields are more explained in more detail in the following sections.


.. note:: The task(s) file(s) does/do not require to have the same name of the task, but it is best practice to use the same name as the task to avoid confusion.


Data files download
-------------------

To download an url you can either specify a string or a dict.
The strings contains the url of the file to download, and it will
be stored with the same designation as the url filename. For example,
to download the ``cifar10`` files you could set the urls to::

    urls = ['https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz']

This will download the above url and save it to the file ``cifar-10-python.tar.gz``.
To download more than one file simply add url strings to the list, and
the urls will be sequentially downloaded and stored to disk.

Some data files (like with the above example) may have a MD5 checksum to
assess file integrity. This is contemplated here by using a dictionary
instead of a string to set the url information. Also, by using a dictionary,
some fine-grain configurations can be done like saving a file with a different
name, defining a checksum, storing it in another directory, etc. Instead of
defining the urls as a list of strings, you can define it as also a list
of dictionaries or a mix of both. To add information of the MD5 checksum to
the example above, you can do::

    urls = [{'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
             'md5hash': 'c58f30108f718f92721af3b95e74349a'}]


Other configuration fields are available. Here is a list of the available
fields:

- ``url``: url link of a file (optional if googledrive is set).
- ``md5hash``: MD5 hash checksum for the url file (optional).
- ``save_name``: name of the downloaded url (optional).
- ``extract_dir``: create a directory in the dataset's data dir and extract all data files into it.
- ``googledrive``: use a hash to download a file from google drive (optional if url is set).


Separate tasks by file
----------------------

TODO


Add tasks to the list
---------------------

TODO

Set some keywords
-----------------

TODO

Default task
------------

TODO

Documentation
-------------

TODO

Create a ``README.rst`` documenting the type and structure of the proposed dataset.
