.. _user_managing_datasets:

=================
Managing datasets
=================

In the (:ref:`Getting started <user_getting_started>`) chapter you've seen how to
do basic operations for loading a dataset, to check what datasets are available in
**dbcollection** and how to fetch data using it. In the next sections we'll explore other
methods for managing your datasets that might come in handy for some situations.

Main operations
================================

You have a set of operations at your disposal using the **dbcollection's** API to
manage your datasets. These operations are:

- downloading data files from online resources
- processing tasks to generate/parse metadata **HDF5** files
- loading a data loader object of a dataset to query and retrieve data from the metadata file
- adding a custom dataset to the list
- removing a dataset or only a task of a dataset from the cache
- configuring/modifying the cache file
- querying the cache file
- displaying cache information

With these you can pretty much do anything you want with your data like deleting a dataset's task or
completely remove any files associated with a dataset (even data files), you can even add custom datasets that
do not exist in the list of available datasets, or simply list information about what datasets
currently exist on your system for loading.


Downloading data files from online resources
=================================================

One use of **dbcollection** is to download data files
from online sources. This is achieved by using the following method:

.. autofunction:: dbcollection.core.api.download





Parsing a dataset's task metadata
=================================================




Loading a dataset as a data loader object
=================================================



Adding a custom dataset
=================================================



Removing a dataset or task
=================================================



Modifying the cache
=================================================



Querying the cache
=================================================




Displaying the cache's contents
=================================================



Listing information of available datasets
=================================================




Best practices
=================================================

TODO