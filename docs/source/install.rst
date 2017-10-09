.. _install:

Install guide
=============

Installing ``dbcollection`` is quite simple. You can do it in several ways, but we advise users to
install this package via ``pip`` or ``conda``. If you want the latest features or bug fixes then you can
install this package from the source.

This package is available for ``windows``, ``linux`` and ``macos``, and **Python** ``>=2.7`` and ``>=3.5`` are
supported.


Install dbcollection via pip
----------------------------

Installing ``dbcollection`` using pip is simple. For that purpose, simply do the following command::

$ pip install dbcollection

This will install the latest version of the ``dbcollection`` package on your system.


Install dbcollection via conda
------------------------------

You can also install ``dbcollection`` via anaconda::

$ conda install -c farrajota dbcollection

.. warning::

    Only Conda packages with Python >= 2.7 and >=3.4 are supported for Linux/MacOS/Windows.


Install dbcollection from source
--------------------------------

To install the ``dbcollection`` package from source, you need to do the following steps:

#. Clone the repo to your hard drive::

    $ git clone --recursive https://github.com/dbcollection/dbcollection


#. ``cd`` to the dbcollection folder and do the command::

    $ cd dbcollection/
    $ python setup.py install

and voilá, the package should now be installed on your system.


Other languages
---------------

There are some wrappers written for use with other languages available if
you want to use this package. For now, these are the supported wrappers that
emulate the functionality of this package:

- `Lua/Torch7 <https://github.com/dbcollection/dbcollection-torch7#installation>`_

- `Matlab <https://github.com/dbcollection/dbcollection-matlab#installation>`_