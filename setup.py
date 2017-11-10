#!/usr/bin/env python


import os
from setuptools import setup, find_packages


# set version
VERSION = '0.2.0'

# Load requirements
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='dbcollection',
    version=VERSION,
    author='M. Farrajota',
    url='https://github.com/dbcollection/dbcollection',
    download_url='https://github.com/dbcollection/dbcollection/archive/' + VERSION + '.tar.gz',
    description="A collection of popular datasets for deep learning.",
    long_description="""
        dbcollection is a library for downloading/parsing/managing datasets via simple methods.
        It was built from the ground up to be cross-platform (Windows, Linux, MacOS) and
        cross-language (Python, Lua, Matlab, etc.). This is achieved by using the popular HDF5
        file format to store (meta)data of manually parsed datasets and Python for scripting.
        By doing so, this library can target any platform that supports Python and any language
        that has bindings for HDF5.

        This package allows to easily manage and load datasets in an easy and simple
        way by using HDF5 files as metadata storage. By storing all the necessary metadata
        to disk, it allows for huge datasets to be used in systems with reduced
        memory usage. Also, once a dataset is setup, it is setup forever! Users can reuse it
        as many times as they want/need for a myriad of tasks without having to setup a
        dataset each time they hack some code. This lets users focus on more important tasks
        fast prototyping without having to spend time managing datasets or creating/modyfing
        scripts to load/fetch data from disk.

        Main features
        -------------

        Here are some of key features dbcollection provides:

        - Simple API to load/download/setup/manage datasets
        - Simple API to fetch data of a dataset
        - All data is stored in disk, resulting in reduced RAM usage (useful for large datasets)
        - Datasets only need to be setup once
        - Cross-platform (Windows, Linux, MacOs).
        - Easily extensible to other languages that have support for HDF5 files
        - Concurrent/parallel data access is possible thanks to the HDF5 file format
        - Diverse list of popular datasets are available for use
        - All datasets were manually parsed by someone, meaning that some of the quirks were
          already solved for you
        """,
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    platforms='any',
    packages=find_packages(exclude=['docs',
                                    'notebooks',
                                    'ci',
                                    'conda-recipe',
                                    'dbcollection.tests']),
    install_requires=requirements,
    include_package_data=True,
)
