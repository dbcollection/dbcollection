dbcollection
============

|Join the chat at https://gitter.im/dbcollection/dbcollection|

|Build Status| |CircleCI| |Build status| |codecov| |License: MIT|
|Documentation Status| |PyPI version| |Anaconda-Server Badge|

**dbcollection** is a library for downloading/parsing/managing datasets via simple methods.
It was built from the ground up to be cross-platform (**Windows**, **Linux**, **MacOS**) and
cross-language (**Python**, **Lua**, **Matlab**, etc.). This is achieved by using the popular ``HDF5``
file format to store (meta)data of manually parsed datasets and the power of Python for
scripting. By doing so, this library can target any platform that supports Python and
any language that has bindings for ``HDF5``.

This package allows to easily manage and load datasets by using ``HDF5`` files to store
metadata. By storing all the necessary metadata to disk, managing either big or small
datasets has an equal or very similar impact on the system's resource usage.
Also, once a dataset is setup, it is setup forever! This means users can reuse any
previously set dataset as many times as needed without having to set it each time they
are used.

**dbcollection** allows users to focus on more important tasks like prototyping new models
or testing them in different datasets without having to incur the loss of spending time managing
datasets or creating/modyfing scripts to load/fetch data by taking advantage
of the work of the community that shared these resources.

Main features
-------------

Here are some of key features dbcollection provides:

- Simple API to load/download/setup/manage datasets.
- Simple API to fetch data from a dataset.
- Store and pull data from disk or from memory, you choose!
- Datasets only need to be set/processed once, so next time you use it it will load instantly!
- Cross-platform (**Windows**, **Linux**, **MacOs**).
- Cross-language (**Python**, **Lua/Torch7**, **Matlab**).
- Easily extensible to other languages that support ``HDF5`` files format.
- Concurrent/parallel data access thanks to ``HDF5``.
- Contains a diverse (and growing!) list of popular datasets for machine-, deep-learning tasks
  (*object detection*, *action recognition*, *human pose estimation*, etc.)

Supported languages
-------------------

-  Python (>=2.7 or >=3.5)
-  Lua/Torch7 (`link`_)
-  Matlab (>=2014a)
   (`link <https://github.com/dbcollection/dbcollection-matlab>`__)

Package installation
--------------------

From PyPi
~~~~~~~~~

Installing ``dbcollection`` using pip is simple. For that purpose,
simply do the following command:

::

    $ pip install dbcollection

From Conda
~~~~~~~~~~

You can also install ``dbcollection`` via anaconda:

::

    $ conda install -c farrajota dbcollection

From source
~~~~~~~~~~~

To install **dbcollection** from source you need to do the following
setps:

-  Clone the repo to your hard drive:

::

    $ git clone --recursive https://github.com/dbcollection/dbcollection

-  ``cd`` to the dbcollection folder and do the command

::

    $ python setup.py install

Getting started
---------------

Basic usage
~~~~~~~~~~~

Using the module is pretty straight-forward. To import it just do:

.. code:: python

    >>> import dbcollection as dbc

To load a dataset, you only need to use a single method that returns a
data loader object which can then be used to fetch data from.

.. code:: python

    >>> mnist = dbc.load('mnist')

This data loader object contains information about the dataset’s name,
task, data, cache paths, set splits, and some methods for querying and
loading data from the ``HDF5`` metadata file.

For example, if you want to know how the data is structured inside the
metadata file, you can simply do the following:

.. code:: python

    >>> mnist.info()

    > Set: test
       - classes,        shape = (10, 2),          dtype = uint8
       - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
       - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
       - object_fields,  shape = (2, 7),           dtype = uint8
       - object_ids,     shape = (10000, 2),       dtype = uint8

       (Pre-ordered lists)
       - list_images_per_class,  shape = (10, 1135),  dtype = int32

    > Set: train
       - classes,        shape = (10, 2),          dtype = uint8
       - images,         shape = (60000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
       - labels,         shape = (60000,),         dtype = uint8,  (in 'object_ids', position = 1)
       - object_fields,  shape = (2, 7),           dtype = uint8
       - object_ids,     shape = (60000, 2),       dtype = uint8

       (Pre-ordered lists)
       - list_images_per_class,  shape = (10, 6742),  dtype = int32

To fetch data samples from a field, its is as easy as calling a method
with the set and field names and the row id(s) you want to select. For
example, to retrieve the 10 first images all you need to do is the
following:

.. code:: python

    >>> imgs = mnist.get('train', 'images', range(10))
    >>> imgs.shape
    (10, 28, 28)

..

    Note: For more information about using this module, please check the
    documentation or the available notebooks for guidance.

Notebooks
~~~~~~~~~

For a more pratical introduction to **dbcollection’s** module for
managing datasets and fetching data, there are some python notebooks
available in the ``notebooks/`` folder for a more hands-on tutorial on
how to use this package.

Documentation
-------------

The package documentation is hosted on `Read The Docs`_.

It provides a more detailed guide on how to use this package as well as
additional information that you might find relevant about this project.

Contributing
------------

All contributions, bug reports, bug fixes, documentation improvements,
enhancements and ideas are welcome. If you would like to see additional
languages being supported, please consider contributing to the project.

If you are interested in fixing issues and contributing directly to the
code base, please see the document `How to Contribute`_.

Feedback
--------

For now, use the `Github issues`_ for requests/bug issues or use our `Gitter room`_
for any other questions you may have.

License
-------

`MIT License`_

.. _link: https://github.com/dbcollection/dbcollection-torch7

.. |Join the chat at https://gitter.im/dbcollection/dbcollection| image:: https://badges.gitter.im/dbcollection/dbcollection.svg
   :target: https://gitter.im/dbcollection/dbcollection?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Build Status| image:: https://travis-ci.org/dbcollection/dbcollection.svg?branch=master
   :target: https://travis-ci.org/dbcollection/dbcollection
.. |CircleCI| image:: https://circleci.com/gh/dbcollection/dbcollection/tree/master.svg?style=svg
   :target: https://circleci.com/gh/dbcollection/dbcollection/tree/master
.. |Build status| image:: https://ci.appveyor.com/api/projects/status/85gpibosxhjo8yjl/branch/master?svg=true
   :target: https://ci.appveyor.com/project/farrajota/dbcollection-x3l0d/branch/master
.. |codecov| image:: https://codecov.io/gh/dbcollection/dbcollection/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/dbcollection/dbcollection
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |Documentation Status| image:: https://readthedocs.org/projects/dbcollection/badge/?version=latest
   :target: http://dbcollection.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/dbcollection.svg
   :target: https://badge.fury.io/py/dbcollection
.. |Anaconda-Server Badge| image:: https://anaconda.org/farrajota/dbcollection/badges/version.svg
   :target: https://anaconda.org/farrajota/dbcollection

.. _Read The Docs: http://dbcollection.readthedocs.io/en/latest/
.. _How to Contribute: https://github.com/dbcollection/dbcollection/blob/master/docs/source/contributing/how_to_contribute.rst
.. _Github issues: https://github.com/dbcollection/dbcollection/issues
.. _Gitter room: https://gitter.im/dbcollection/dbcollection
.. _MIT License: LICENSE.txt
