#!/usr/bin/env python

"""
Parts of this file were taken from the luigi project
(https://github.com/spotify/luigi) as reference.
"""


import os
from setuptools import setup, find_packages


# set version
VERSION = '0.2.2'


def get_requirements():
    """Loads contents from requirements.txt."""
    requirements = []
    with open('requirements.txt') as f:
        data = f.read().splitlines()
    if any(data):
        requirements = [item.split(" ")[0] for item in data]
    return requirements


LONG_DESCRIPTION = ''

readme_note = """\
.. note::
   For the latest source, discussion, etc, please visit the
   `GitHub repository <https://github.com/dbcollection/dbcollection>`_\n\n
"""

with open('README.rst') as fobj:
    LONG_DESCRIPTION = readme_note + fobj.read()


setup(
    name='dbcollection',
    version=VERSION,
    author='M. Farrajota',
    url='https://github.com/dbcollection/dbcollection',
    download_url='https://github.com/dbcollection/dbcollection/archive/' + VERSION + '.tar.gz',
    description="A collection of popular datasets for deep learning.",
    long_description=LONG_DESCRIPTION,
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
                                    'tests']),
    install_requires=get_requirements(),
    include_package_data=True,
)
