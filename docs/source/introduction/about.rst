.. _about:

==================
About dbcollection
==================

What is dbcollection
====================

``dbcollection`` is a package written in **Python** that contains methods for downloading / managing datasets and to fetch data from them
via simple API function calls. This package was developed with ease of use in mind and seamless reuse of data between projects.
It provides to researchers a quick and easy way to deal with the headache of setting up data for training / processing algorithms when working on a new project.

Also, it provides a cross-platform, cross-language framework to share datasets between users
such that anyone can quickly load/fetch data with minimal effort spent, thus taking advantage
of the community effort to build and share solutions for common problems.

In summary, the main goal of this project is to help users save time and effort when developing/deploying/sharing code.


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


What problems does it try to solve
==================================

This project tries to solve some of the problems I've identified
during my research when trying out new datasets. These are some of the
problems ``dbcollection`` tries to solve:

- Downloading, extracting and parsing different datasets without prior knowledge of their inner workings is sometimes error prone.
- Constantly writting the same boilerplate code or adapting existing one for new projects is a hassle.
- Disk space gets littered with data files everywhere as you work on different projects with no centralized storage.
- Wasted time and computer resources (mostly memory) when loading large datasets.
- Many datasets use ``.json`` files to distribute their (meta)data, which is fine for smaller datasets, but they are not an efficient solution to store large amounts of (meta)data for large datasets.
- Usually trying new datasets means that you will have to spend a significant portion of your time learning how to use it so you can load/parse it. And good luck if those datasets are distributed using some complicated, in house format that can only be extracted by using a specific toolbox (e.g., Caltech Pedestrian).
- Having to learn a toolboxe (and languages maybe) to fetch data for a given dataset that you just want to try it out before doing anything serious is not viable at all or, at best, a tedious task.
- If you start using a new language you'll probably write the same scripts to load/parse your datasets.

This project aims to solve most of these problems so anyone using it won't have to deal
with the nightmare that is trying a new dataset. By using ``dbcollection``, you can immediately
start to use any dataset of your choice without much of the pain that involves using a
new dataset, so you can quickly train/test your new, shiny algorithm / model in simple or complex scenarios
without having to waste precious time.


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
