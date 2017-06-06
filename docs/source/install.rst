.. _install:

Install Guide
=============


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

    $ git clone --recursive https://github.com/farrajota/dbcollection


#. ``cd`` to the dbcollection folder and do the command::

    $ cd dbcollection/
    $ python setup.py install

and voilá, the package should now be installed on your system.
