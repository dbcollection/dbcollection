.. _code_organization:

=================
Code organization
=================

**dbcollection** consists of a modular code written in Python that can be easily extended to other languages.
It contains core apy methods, a list of dataset constructors and utility functions in separate folders.
These compose the core functionality and features of the dbcollection package which  can be used to
write other APIS using other languages like Lua or Matlab.

Additionally, the main repository contains other relevant components of the project worth mentioning like
the :ref:`docs <documentation_sec>` and :ref:`notebooks <notebooks_sec>` directories.


dbcollection
============

The ``dbcollection/`` directory contains the main project's files. It is partitioned into four other
directories where the :ref:`core api functions <core_subsec>`, :ref:`available datasets <datasets_subsec>`,
:ref:`unit/functional tests <tests_subsec>` and :ref:`utility functions <utils_subsec>` are stored.

.. code-block:: bash

    dbcollection/
        core/
        datasets/
        tests/
        utils/
        __init__.py
        _version.py

.. _core_subsec:

core/
-----

All api methods and classes are stored in this folder.


.. _datasets_subsec:

datasets/
---------

All datasets are stored in this dir, where each dataset is stored in a separate folder with the same name.
Related datasets may be stored in different subfolders under the same dir. For more information see the `GitHub repository <https://github.com/dbcollection/dbcollection>`_.


.. _tests_subsec:

tests/
------

All tests are organized under the ``tests/`` directory by language and functionality. The project uses two
types of tests to check for bugs: `unit tests <https://stackoverflow.com/questions/652292/what-is-unit-testing-and-how-do-you-do-it>`_
and `functional tests <https://stackoverflow.com/questions/2741832/unit-tests-vs-functional-tests>`_.
Unit tests are used to test the core functions of the package and functional tests are used to test
the execution of downloading and installing a dataset.

The directory is organized with the same dir structure as the dbcollection/ dir.
It has the following structure:

.. code-block:: bash

    tests/
        core/
            test_api.py
            test_cache.py
            test_db.py
            test_loader.py
            ...
        functional/
            download/
                cifar10.py
                cifar100.py
                mnist.py
                ...
            load/
                cifar10.py
                cifar100.py
                mnist.py
                ...
            process/
                cifar10.py
                cifar100.py
                mnist.py
                ...
        utils/
            test_pad.py
            test_string_ascii.py
            ...


.. _utils_subsec:

utils/
------

The utility functions dir contains methods to load files, download urls, extract data, parse strings, manage cache data, etc.
Additional functionality should be added in this folder.


.. _documentation_sec:

Documentation
=============

The ``docs/`` directory contains the documentation files. We use `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ to build
our documentation and `Read The Docs <https://readthedocs.org/>`_ to host it.
The structure of ``docs/`` is similar to most docs using Sphinx:

.. code-block:: bash

    docs/
        build/
        source/
        make.bat
        Makefile


.. _notebooks_sec:

Notebooks
=========

The ``notebooks/`` directory contains tutorials/demos/guides on using ``dbcollection`` as a `IPython <https://ipython.org/ipython-doc/3/notebook/>`_/`Jupyter Notebook <http://jupyter.readthedocs.io/en/latest/install.html>`_.
These notebooks show how to use the package and show how it can be integrated with your code/research without
too much hassle in a simple and interactive way.

To keep it simple, all notebooks are stored under ``notebooks/``. All notebooks names should follow this convention
``<type>_<language>_<goal>.ipynb`` (lower-case) where:

- ``type``: This indicates what is the intent of the notebook. You should use a descriptive word that unanimously
  explains what the notebook is all about. You can use one of these following attributes to
  categorize the purpose of the notebook: example, tutorial, demo, guide, etc.
- ``language``: Target language of the notebook.
- ``goal``: What's the end goal of the notebook. This can be a single or multiple words separated by an underscore
  and it should brifly describe what is purpose of the notebook.


Examples of names::

    tutorial_python_dbcollection_api.ipynb
    tutorial_python_dbcollection_tensorflow.ipynb
    example_matlab_install_cifar10.ipynb
    demo_lua_mnist.ipynb