.. _user_managing_datasets:

=================
Managing datasets
=================

In the :ref:`Getting started <getting_started>` chapter you've seen basic operations
on how to load a dataset, check what available datasets are in **dbcollection** and 
to fetch data like image tensors and labels. In the following sections, we'll explore 
in more detail how to use the **dbcollection** dataset management API to deal with loading,
adding or removing datasets with some simple commands. Furthermore, other functionality like 
managing the cache file, finding which datasets are available for download or which tasks does 
it have will be covered as well. 

.. note::
    This section covers all the necessary steps / ways for you to effectively use this package for dealing with datasets.


Main operations
================================

You have a set of operations at your disposal using the **dbcollection's** API to
manage your datasets. These operations are:

- :ref:`Downloading data files from online resources <user_managing_datasets_download>`
- :ref:`Parsing annotations / metadata of datasets <user_managing_datasets_process>`
- :ref:`Loading a dataset as a data loader object <user_managing_datasets_load>`
- :ref:`Adding a custom dataset <user_managing_datasets_add>`
- :ref:`Removing a dataset or task <user_managing_datasets_remove>`
- :ref:`Modifying the cache <user_managing_datasets_config_cache>`
- :ref:`Querying the cache <user_managing_datasets_query_cache>`
- :ref:`Displaying cache information <user_managing_datasets_print_cache>`
- :ref:`Displaying information about available datasets <user_managing_datasets_list_datasets>`

These operations allows users to do (pretty much) anything needed for managing data files. A word
of warning though: users must take into consideration the implications of some of these operations like removing datasets data or modyfing the cache may result in permanent data loss. You should check the section of :ref:`Best practices <user_managing_datasets_best_practices>` if you are unclear on how to proceed in some cases in order to avoid undesired results.


.. _user_managing_datasets_download:

Downloading data files from online resources
=================================================

.. warning::
   This section deals with manually downloading source data files of datasets. 
   For most users this information may not be necessary or relevant, and you can skip this section altogether and move to the one which deals with :ref:`loading datasets <user_managing_datasets_load>`.

   This is because the ``load()`` method automatically downloads or processes any dataset that has not been previously setup, and it is not required to manually download data files in order to load a dataset.

One use of **dbcollection** is to download data files from online sources. This removes the need
to search where to get the data files from and to locate which specific resources are required. 
In some cases is not a very challenging task to do, but in other it can be a daunting task. By 
having the necessary resources defined and ready you can save quite time some time in dealing
with this process. 

To download a dataset you simply need to use the :ref:`download() <core_reference_api_download>` method from the :ref:`core API <core_reference_api>` methods and provide the name of the dataset you want to download. For example, lets download the ``cifar10`` dataset's data files:

.. code-block:: python

   >>> dbc.download('cifar10')

The data files will be stored in a folder named ``cifar10/`` in a pre-defined directory in disk defined by ``dbc.cache.download_dir``. To change this directory you can simpy assign a new path to it: ``dbc.cache.download_dir = 'my/new/path/'``. 

If you want to use a different directory to store the data files you can use the ``data_dir`` input argument to specify the path of the data directory you want to store your files:

.. code-block:: python

   >>> dbc.download('cifar10', data_dir='some/other/path/')

This will also create a folder with the same name as the dataset. This is important because
**dbcollection** searches for this dir names when loading the data files. If the names don't
match then it proceeds to download the source files. 

After all files have been downloaded, by default, they are extracted into the same folder where they have been stored. Most source files are compressed for distribution. The ``download()`` method allows to extract these compressed files to disk without you having to manually do it yourself. 
If the source data files are all what you want to retrieve, then set the 
``extract_data`` input argument to ``False``:

.. code-block:: python

   >>> dbc.download('cifar10', extract_data=False)

.. note::
   This package uses the `patool <https://pypi.python.org/pypi/patool>`_ module for file extraction which supports most data compression formats like TAR, ZIP or RAR.

An important aspect to mention about using this method is that, when using it to download data files of a dataset, it automatically registers in cache where the files are located for that dataset. So, next time you want to load that dataset you don't need to explicitly specify where the data is located in disk (if the files still exist of course).


.. _user_managing_datasets_process:

Parsing annotations / metadata of datasets
=================================================

.. warning::
   This section deals with manually parsing annotations of datasets. 
   For most users this information is not relevant and you can skip this section altogether and move to the next one which deals with :ref:`loading datasets <user_managing_datasets_load>`.

   This is because the ``load()`` method automatically downloads or processes any dataset that has not been previously setup, and it is not required to manually parse annotations of tasks of datasets in order to load a dataset.

Arguably, one of the most important functionalities of **dbcollection** is automatically processing data annotations. 
It is well known that manually parsing data files + annotations of different datasets is no fun.
Moreover, it is time consuming, annoying and repetitive. 
Also, it usually results in disks littered with various cache files which are used to store portions of the annotations accross multiple directories for some specific tasks.  

**dbcollection** provides a way to deal with these issues. Hand-crafted scripts were developed to parse data annotations of specific tasks of datasets for you.  These annotations are stored in a common format and in a single place on your disk that you can easily track.

.. note::
   Not all annotations are necessary for day to day use, so only the most useful ones are stored. If you happen to need an annotation that is not available in our scripts for any particular reason, please feel free to fill an `issue on GitHub <https://github.com/dbcollection/dbcollection/issues>`_ describing what annotation you need, why and for what task + dataset or, better yet, :ref:`contribute with a pull request <pull_request>`. 

Processing metadata of dataset's annotations is done by using the :ref:`process() <core_reference_api_process>` method. 
Continuing with the previous section example, lets process the metadata files for the ``cifar10`` dataset:

.. code-block:: python

   >>> dbc.process('cifar10')

The method will process the data annotations of this dataset and stores the resulting metadata into an ``HDF5`` file stored in disk. By default, all metadata files are stored in your home directory in ``~/dbcollection/<dataset>/<task>.h5``. 

This directory is used to centralize all metadata files in disk and its path can be accessed via ``dbc.cache.cache_dir``. To change the default path, simply assign a new path to it: ``dbc.cache.cache_dir = new/cache/path/``. 

Many datasets have many tasks to choose from and these can be listed by the ``info_datasets()`` method described in :ref:`this section <user_managing_datasets_list_datasets>`. To specify which task to process, we must use the ``task`` input argument and assign it a task name:

.. code-block:: python

   >>> dbc.process('cifar10', task='classification')

This processes the annotations of the ``classification`` task and registers them to cache. 

We must point out that this example is not the most illustrative of them all because ``cifar10`` only has one task which is ``classification``. 

Every dataset has a default task and it is not required to explicitly define one. But, if you want to select a different task, you will need to provide a valid task name for processing.

.. note::
   The ``process()`` method requires that the data files of a dataset have been previously downloaded and registered in the cache. 

   If you have not done this, please see the previous section which explains how to download data files of a dataset or see the section further on this page about manually configuring the cache if you happen to have the necessary data files in disk but on a different folder.

The next section covers the ``load()`` method which deals with loading datasets as data loader objects for extracting (meta)data.


.. _user_managing_datasets_load:

Loading a dataset as a data loader object
=================================================




.. _user_managing_datasets_add:

Adding a custom dataset
=================================================


.. _user_managing_datasets_remove:

Removing a dataset or task
=================================================


.. _user_managing_datasets_config_cache:

Modifying the cache
=================================================

.. _user_managing_datasets_query_cache:

Querying the cache
=================================================


.. _user_managing_datasets_print_cache:

Displaying cache information
=================================================


.. _user_managing_datasets_list_datasets:

Displaying information about available datasets
=================================================


.. _user_managing_datasets_best_practices:

Best practices
=================================================

TODO
