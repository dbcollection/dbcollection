#!/usr/bin/env python


from setuptools import setup, find_packages


long_description="""dbcollection is a cross-platform (Windows, MacOS, Linux),
cross-language (Python, Lua/Torch7, Matlab) API to easily manage datasets'
metadata by using the standard HDF5 file format.
"""


with open('LICENSE.txt') as f:
    license_mit = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='dbcollection',
    version='0.1.0',
    author='Miguel Farrajota',
    url='https://github.com/farrajota/dbcollection',
    description='Cross-platform, cross-language dataset metadata manager for machine learning',
    long_description=long_description,
    license=license_mit,
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['test', 'APIs', '.vscode']),
    install_requires=requirements
)