.. _create_new_dataset:

======================
Creating a new dataset
======================

Creating a new dataset requires you to set the download, setup and parse
scripts in a certain way. In order to properly setup a new dataset, you need to accomplish these three following steps:

#. First, create a directory under the ``datasets/`` dir so it can be loaded to the list of available datasets.

#. Then, set up a ``__init__.py`` file for storing the configurations of the new dataset (urls, keywords, tasks) and to create unique ``.py`` files for each task your dataset will have.

#. Finally, include a ``README.rst`` documentation file for the dataset in the same directory. This should provide a 'how to use' manual for users to understand the data structure of the ``HDF5`` metadata files.

With these steps you are done with creating a dataset. The package will automatically search for directories under ``datasets/`` which have a specific class in the ``__init__.py`` file and includes it into a list of datasets.

In the following sections we'll take a closer look on how to properly configure and set up these files and directories.


Setting up the dataset's directory
==================================

To create a new dataset you need to create a
directory with the same name of the dataset you want it be called under 
the ``datasets/`` directory.

You can use multiple nested directories to store your dataset in cases 
where other related datasets will be grouped under a common dir. For example,
the ``cifar10`` and ``cifar100`` datasets are stored under the ``cifar/`` directory:


::

    dbcollection/
    ├── core/
    │      ...
    ├── datasets/
    │   ├── cifar/  
    │   │   ├── cifar10/    
    │   │   └── cifar100/           
    │   └── ...  
    ├── tests/
    │      ...
    │
    └── utils/
           ...

This enables the package to group several different (or similar) versions of the same dataset under the same parent folder for organizational purposes, thus maintaing a clear structure for future additions of datasets in the root ``datasets/`` directory that may contain many related datasets.

.. note:: 

   Please use **snake_case** when naming the directory by using
   all characters in lower case and separated by an underscore. 
   See the :ref:`Coding guidelines <code_guidelines>` section for 
   more information.


Setting up the ``__init__.py`` file
===================================

Inside the folder there should be a ``__init__.py`` and one or more files containing code to parse the data for a given task.

The file contains information about the urls, tasks
and keywords of the dataset. To set up these configs you need to import a :ref:`BaseDataset <datasets_reference_base>` class to define these parameters. To set this class you can use the following setup:

.. code-block:: python

    """
    Brief description of the dataset
    """

    from dbcollection.datasets import BaseDataset
    from .taskfile import TaskName

    urls = ('http://url.something',)
    keywords = ('some', 'keywords', 'for', 'grouping')
    tasks = {'some_task_name': TaskName}
    default_task = 'some_task_name'

    class Dataset(BaseDataset):
        """Name of the dataset."""
        urls = urls
        keywords = keywords
        tasks = tasks
        default_task = default_task


To setup the new dataset's class you need to:


#. Write a short docstring indicating the purpose of the dataset (for image
   classification, object detection, action recognition, natural language
   processing, etc.);

#. Import ``BaseDataset`` from ``dbcollection.datasets``;

#. Import the task classes from their corresponding files. In the above example,
   the task ``TaskName`` was imported from ``taskfile.py`` which must be located
   in the same directory as the ``__init__.py`` file;

#. Define a class called ``Dataset`` that inherits from ``BaseDataset``.
   (It is required to name the class as ``Dataset`` in order for it to be
   included in the dataset list along with the rest of the other datasets);

#. Define a docstring for the class with the name of the dataset;

#. Set the ``urls``, ``keywords``, ``tasks`` and ``default_task`` fields.
   The ``urls`` field contains a list of urls of the source data files to be downloaded.
   The ``keywords`` field contains a list of strings which are used for helping in searching/grouping
   datasets for cataloging the existing datasets and their functionality. The
   ``tasks`` field is a dictionary containing all available tasks constructors for the dataset, and
   the ``default_task`` field indicates which task should be loaded as the default if no name is
   set when loading/processing a dataset.

.. note:: 

   The task(s) file(s) does/do not require to have the same name of the task, but it is best practice to use the same name as the task to avoid confusion.


Additional information about setting up URLs for different sources
------------------------------------------------------------------

When configuring an url for download, you can either specify a string or a dict.

If using a string, the url of the file to download will
be stored with the same filename as the url. 
Lets take the case of downloading data files for the ``cifar10`` dataset. To download the data file, you simply need to set the urls list as the following example:

.. code-block:: python

   urls = ('https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',)

This will download the above url and save it to disk as ``cifar-10-python.tar.gz``.

To download more files simply add url strings to the list and
they will be sequentially downloaded and stored to disk.

We could write the previous example as using a dictionary instead of a string:

.. code-block:: python

   urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'},)

This way contains additional options that you can use for dealing with urls. For example, if a MD5 hash checksum is available, you can use it to validate the integrity of the downloaded file:

.. code-block:: python

   urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
            'md5hash': 'c58f30108f718f92721af3b95e74349a'},)

We could also change the name of the saved filename. For that, we need to set a ``save_name`` field with the name of the file we would like to store the url data to disk.

.. code-block:: python

   urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
            'md5hash': 'c58f30108f718f92721af3b95e74349a',
            'save_name': 'cifar-10.tar.gz'},)

In some cases, for example, due to file names clashing, you may need to extract the downloaded url files into a different directory instead of the directory where the data file is stored. You can use the ``extract_dir`` field to specify a child directory name to extract these files into a separate directory in order to avoid the previous problem:

.. code-block:: python

   urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
            'md5hash': 'c58f30108f718f92721af3b95e74349a',
            'save_name': 'cifar-10.tar.gz',
            'extract_dir': 'extract_cifar10'},)

Another use case you may want to know is how to download url files from google drive. Fortunately for you, this is implemented here via the ``googledrive`` field. Note that this requires you to specify a filename in ``save_name``. For example, downloading an url from google drive you can do the following:

.. code-block:: python

   urls = ({'googledrive': '0B4K3PZp8xXDJN0Fpb0piVjQ3Y3M',
            'save_name': 'flic.zip'},)

.. note::

   For more information about downloading urls see the :ref:`Url download <utils_reference_url>` section in the Reference manual.


Creating a task for parsing annotations
=======================================

To create a script to parse / process annotations for a specific task you need to create a file (or as many files as you need) in the same directory as the ``__init__.py`` file. 

Here you'll load and process all your annotations and define how data will be stored in the ``HDF5`` metadata file. The following template shows a basic setup of such task file which you can use as guidance when creating your own. You should also take a look at how other datasets' tasks are setup in order to have a better grasp on how to setup yours.

.. code-block:: python

   """
   Name of the dataset and the task
   """


   # import necessary packages here
   from __future__ import print_function, division  # for python 2.7 compatibility
   import os
   import numpy as np
   ...

   # import the BaseTask class for inheriting its methods
   from dbcollection.datasets import BaseTask

   # import additional utility methods for parsing strings, padding lists or storing data
   from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
   from dbcollection.utils.pad import pad_list
   from dbcollection.utils.hdf5 import hdf5_write_data


   class Classification(BaseTask):
       """Name of the dataset + task."""
 
       # metadata filename of the task
       filename_h5 = 'classification'

       # Main method to load data from files
       def load_data(self):
           """
           Load the data from the files.
           """
           # Load annotations or setup other data fields here

       # Main method to store data to the HDF5 metadata file
       def add_data_to_default(self, hdf5_handler, data, set_name=None):
           """
           Add data of a set to the default group.

           For each field, the data is organized into a single big matrix.
           """
           # Store metadata here

       # optional method for storing data in the raw format (can leave as blank)
       def add_data_to_source(self, hdf5_handler, data, set_name=None):
           """
           Store data annotations in a nested tree fashion.

           It closely follows the tree structure of the data.
           """
           pass

.. note::

   Check out how ``cifar10`` or ``mnist`` are setup for a basic script on how to parse annotations and structure how data is stored in the ``HDF5`` metadata file.


How to store data into ``HDF5`` files
-------------------------------------

One important note about storing data into ``HDF5`` files is how to do it. Due to the way the **dbcollection's** API is defined, you must need to store all information of a field into a single array. This way, each row indicated a sample and the columns the structure of the data itself.

For most cases, you will need to pad data in order to have arrays of the same shape. This has been discussed in :ref:`this section here <user_fetching_data_parsing_data>` which you should take a look if you have questions about (un)padding data. Also, you should take a look at :ref:`Padding <utils_reference_padding>` section in the Reference manual.

Another relevant information to mention is how to save the data fields into the ``HDF5`` file. You can either use ``h5py`` syntax to allocate the data fields in the right position or you can use the :ref:`hdf5_write_data() <utils_reference_hdf5_write_data>` from ``dbcollection.utils.hdf5`` to simplify this process. 

Besides these utility methods there are other useful ones in ``dbcollection.utils`` module that you should take a look when creating your own task, specially the :ref:`utils <utils_reference>` section in the Reference manual for a list of available methods.


Writting the ``README.rst`` documentation file
==============================================

When creating a dataset, it is very important to provide a small documentation of the structure and information of the data.

When creating such manual, it is good practice to follow a common format to keep things consistent.

The following scheme details a template format on how to write a ``README.rst`` documentation file in the ``reStructuredText`` format for a new dataset and what information to provide to the end user in order to describe how to use it.


::

   .. _<dataset_name>_readme:

   ==============
   <dataset_name>
   ==============

   Brief description of the dataset's format / main features.


   Use cases
   =========

   Main use cases.

   (E.g., Image classification.)


   Properties
   ==========

   - ``name``: <dataset_name> (same as the directory)
   - ``keywords``: "some", "keywords".
   - ``dataset size``: size of the source data files in disk (e.g., 11,6 MB)
   - ``is downloadable``: **yes**, **no** or **partial**
   - ``tasks``:
       - :ref:`<task_name1> <link_task1>`: **(default)**  <-- indicates that it is the default task
           - ``primary use``: main use case (e.g., image classification)
           - ``description``: brief description of the annotations available
           - ``sets``: list of set splits (e.g., train, test)
           - ``metadata file size in disk``: size of the task's metadata file in disk (e.g., 6,8 MB)
           - ``has annotations``: **yes** or **no**
               - ``which``:
                   - brief description of the annotation (e.g., labels for each image class/category.)
                     ...
                   
       - :ref:`<task_name2> <link_task2>`:
          ...
       - :ref:`<task_name3> <link_task3>`:
          ...


   Metadata structure (HDF5)
   =========================

   .. _link_task1::

   Task: <task_name1>
   --------------------

   ::

       /
       ├── <set1>/
       │   ├── field1         # dtype=np.uint8, shape=(10,2)   (note: string in ASCII format)
       │   ├── field2         # dtype=np.uint8, shape=(60000,28,28)
       │   ├── field3         # dtype=np.uint8, shape=(60000,)
       │   ├── object_fields  # dtype=np.uint8, shape=(2,7)    (note: string in ASCII format)
       │   ├── object_ids     # dtype=np.int32, shape=(60000,2)
       │   └── list_field1_per_field2   # dtype=np.int32, shape=(10,6742))
       │
       └── <set2>/
           ├── field1         # dtype=np.uint8, shape=(10,2)   (note: string in ASCII format)
           ├── field2         # dtype=np.uint8, shape=(10000,28,28)
           ├── field3         # dtype=np.uint8, shape=(10000,)
           ├── object_fields  # dtype=np.uint8, shape=(2,7)    (note: string in ASCII format)
           ├── object_ids     # dtype=np.int32, shape=(10000,2)
           └── list_field1_per_field2   # dtype=np.int32, shape=(10,1742))


   Fields
   ^^^^^^

   - ``<field1>``: <description of the field> (e.g., class names)
       - ``available in``: <sets> (e.g., train, test)
       - ``dtype``: <numpy data type> (e.g., np.uint8)
       - ``is padded``: True or False
       - ``fill value``: 0 , 1, -1, etc.
       - ``note``: an important note about this data field ( e.g., strings stored in ASCII format)
   - ``<field2>``: <description of the field>
       - ``available in``: <sets> 
       - ``dtype``: <numpy data type> 
       - ``is padded``: True or False
       - ``fill value``: 0 , 1, -1, etc.
       - ``note``: pre-ordered list (another example)
   - ...

   Disclaimer
   ==========

   Disclaimer about the creators of the dataset.

   Info of the website where the dataset was retrieved from.
   It should containg a link to the original website/source.

