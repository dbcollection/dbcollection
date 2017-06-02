#!/usr/bin/env python


import os
from setuptools import setup, find_packages, Command
import setuptools.command.build_py


################################################################################
# Package info
################################################################################

VERSION = '0.1.3'
ISRELEASED = True
__version__ = VERSION
cwd = os.path.dirname(os.path.abspath(__file__))


################################################################################
# Custom build commands
################################################################################

class build_py(setuptools.command.build_py.build_py):

    def run(self):
        self.create_version_file()
        setuptools.command.build_py.build_py.run(self)

    @staticmethod
    def create_version_file():
        global VERSION, cwd
        print('-- Building version ' + VERSION)
        version_path = os.path.join(cwd, 'dbcollection', 'version.py')
        with open(version_path, 'w') as f:
            f.write("__version__ = '{}'\n".format(VERSION))


################################################################################
# Dynamically set the conda package version
################################################################################

try:
    if os.environ['CONDA_BUILD']:
        with open('__conda_version__.txt', 'w') as f:
            if ISRELEASED:
                f.write(VERSION)
            else:
                f.write(VERSION + '.dev')
except KeyError:
    pass


################################################################################
# Load requirements
################################################################################

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


################################################################################
# Package setup
################################################################################

setup(
    name='dbcollection',
    version=VERSION,
    author='M. Farrajota',
    url='https://github.com/farrajota/dbcollection',
    download_url='https://github.com/farrajota/dbcollection/archive/0.1.3.tar.gz',
    description='Cross-platform, cross-language dataset metadata manager for machine learning',
    long_description="""dbcollection is a cross-platform (Windows, MacOS, Linux),
        cross-language (Python, Lua/Torch7, Matlab) API to easily manage datasets'
        metadata by using the standard HDF5 file format.
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
    ],
    packages=find_packages(exclude=['tests', 'APIs', 'docs']),
    install_requires=requirements
)