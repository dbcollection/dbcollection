.. _introduction:

============
Introduction
============

What is dbcollection
====================

It is a package written in **Python** that contains methods for downloading and setup datasets and to fetch data via simple API function calls,
with ease of use in mind and seamless reuse of data between projects. This provides researchers
a quick and easy way to deal with the headache of setting up data for processing when working on a new project.

Also, it provides a cross-platform, cross-language framework to manage datasets,
quickly load/fetch data with minimal resources wasted and a list of diverse
datasets to work with.

The main goal of this project is to help save time for users when developing/deploying/sharing code.



Why does this project exist
===========================

This project started during my PhD where when learning/experimenting new stuff in machine/deep learning was a constant struggle
between setting up new datasets and manually parsing some of the quirks they might had before even doing the actual research I was meant to do.

Also, when moving between projects/frameworks this usually meant that I either had to reimplement it in another language or had to
re-write the same boilerplate code once more (and store it in a cache file to avoid constant computations at startup). This
usually meant time lost doing the same thing over and over again, hard drives filled with 'junk' and, ultimately, it bored me.

By the end of 2016 I've started writting some initial code in Lua to deal with downloading data from urls, extracting it from a myriad of compression formats
like .zip, .tar, etc., process the metadata associated with the dataset in the right format and storing the resulting data into disk as cache
in order to avoid re-computing it every time I'd launch a script.

This worked fairly well and helped to avoid recomputing datasets over and over again and it meant I only needed to do it once.
Afterwards, I've discovered how neat ``HDF5`` files were and all the features they had, and this provided the missing piece I needed for
building a cross-language, cross-platform metadata storing/fetching framework for general purpose data management.


What problems does it solve
===========================

This project tries to solve some of the problems I've identified
during my research when trying out new datasets. These are some of the
problems ``dbcollection`` tries to solve:

- downloading, extracting and parsing different datasets without prior knowledge of their inner workings and possible pitfalls
- constantly writting the same boilerplate code or adapting existing one for new projects
- moving to a new language meant a complete re-writte the same code for loading/parsing datasets
- disk space littered with cached data everywhere
- multiple versions of parsers for specific use cases depending on the project (which meant you'll have to figure out which version fits best your new problem if you are reusing code)
- wasted time and memory when loading large datasets
- .json files are not a good solution for cross-platform, cross-language scenarios (again, because of large datasets)
- using a new dataset means you have to spend a significant part of time learning how to use it in order to load/parse it (and good luck if they use some obscure, in house format that can only be extracted by using a specific toolbox)
- and learning how to use other people's toolboxes is a tedious task, let alone if they are written in one or several different languages.

This project aims to solve most of this problems for its users, such that they don't have to deal
with the nightmare that using a new dataset can be when you just want to train/test your new algorithm in
a more complex scenario or bigger set of data.


How does it work
================

When loading a dataset, the user uses usually a single API method to fetch a data loader object.
The method looks for an entry of the dataset in a cache file stored in your home directory for a matching entry.
If the dataset does not exist in cache, the system proceeds to do the following steps to download and process a dataset:

#.  First, the data files are located in a pre-defined path or in a path provided by the user.
    If no data files are found or no one matches the specific files the package is looking for, it proceeds to download the 
    data files to disk by using pre-defined urls with the source files. Then, the downloaded files are extracted into the same 
    path where the files are located;

#.  Next, the data files are processed and annotations are parsed and converted into numpy arrays which are stored 
    into a ``HDF5`` file;

#.  Then, the dataset's information is added to cache.

After these steps are done, a data loader object is generated based on the metadata ``HDF5`` file
that contains the dataset's metadata information. This object contains several methods for querying
and fetching data from the metadata file.

Since the processed metadata is stored in a ``HDF5`` file, it provides some key features like:

- portable across languages and operating systems;
- fast access to data;
- allows concurrent reads of the same file;
- compression;
- data can be stored in a nested way (like a folder tree)

Also, by using the ``HDF5`` format, it is simple to deploy an API written in other languages that support the
``HDF5`` format to interface with the stored metadata. For more information about this file format see the
`official HDF5 documentation <https://support.hdfgroup.org/HDF5/>`_.

.. note::

    The **dbcollection** package creates a folder in your home directory named ``~/dbcollection/`` where all the metadata
    files are organized and stored. The contents of this folder is tracked by a ``.json`` file also stored in your
    home directory in ``~/dbcollection.json`` which contains all information/configurations about the stored datasets.
