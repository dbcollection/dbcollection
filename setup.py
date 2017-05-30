#!/usr/bin/env python


import os
from setuptools import setup, find_packages


long_description="""dbcollection is a cross-platform (Windows, MacOS, Linux),
cross-language (Python, Lua/Torch7, Matlab) API to easily manage datasets'
metadata by using the standard HDF5 file format.
"""

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dbcollection',
    version='0.1.2',
    author='Miguel Farrajota',
    url='https://github.com/farrajota/dbcollection',
    download_url='https://github.com/farrajota/dbcollection/archive/0.1.2.tar.gz',
    description='Cross-platform, cross-language dataset metadata manager for machine learning',
    long_description=long_description,
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
    ],
    packages=find_packages(exclude=['test', 'APIs', '.vscode']),
    install_requires=requirements
)