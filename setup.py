#!/usr/bin/env python


import os
from setuptools import setup, find_packages


# set version
VERSION = '0.1.7'

cwd = os.path.dirname(os.path.abspath(__file__))
version_path = os.path.join(cwd, 'dbcollection', '_version.py')
with open(version_path, 'w') as f:
    f.write("__version__ = '{}'\n".format(VERSION))


# Load requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='dbcollection',
    version=VERSION,
    author='M. Farrajota',
    url='https://github.com/dbcollection/dbcollection',
    download_url='https://github.com/dbcollection/dbcollection/archive/' + VERSION + '.tar.gz',
    description='Cross-platform, cross-language dataset metadata manager for machine learning.',
    long_description="""
        dbcollection is a cross-platform (Windows, MacOS, Linux),
        cross-language (Python, Lua/Torch7, Matlab) API to easily
        manage datasets' metadata by using the standard HDF5 file
        format.
        """,
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=requirements
)