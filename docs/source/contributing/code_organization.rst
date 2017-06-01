.. _code_organization:

Code Organization
=================

dbcollection consists of a modular code written in Python that can be easily extended.
It contains a list of dataset constructors and utility functions in separate folders.
These compose the core features of the dbcollection package which other APIs rely on and
are built upon.

Additionally, the main repository contains other relevant components of the project worth mentioning like
the :ref:`APIs <apis_sec>`, :ref:`docs <documentation_sec>`, :ref:`tests <tests_sec>` and :ref:`notebooks <notebooks_sec>` directories.


dbcollection
------------

The ``dbcollection/`` directory contains the main project's files. It is partitioned into two other directories where the
:ref:`utility functions <utils_subsec>` and :ref:`datasets <datasets_subsec>` are stored.

.. code-block:: bash

    dbcollection/
        datasets/
        utils/
        __init__.py
        manager.py


.. _utils_subsec:

utils/
^^^^^^

The utility functions dir contains methods to load files, download urls, extract data, parse strings and manage cache data.
Additional functionality should be added in this folder.


.. _datasets_subsec:

datasets/
^^^^^^^^^

All datasets are stored in this dir, where each dataset is stored in a separate folder with the same name. Related datasets
may be stored in different subfolders under the same dir. For more information see the `GitHub repository <https://github.com/farrajota/dbcollection>`_.



.. _apis_sec:

APIs
----

Support for other languages are stored in ``APIS/<language>/``. These are essencially wrapper code for the executting
python scripts that call APIs of ``dbcollection``. This simplifies the necessary code to reproduce the same actions on
another language.

For every language, a ``README.rst`` and ``DOCUMENTATION.rst`` file must exist containing information on how to install
and use the library.


.. code-block:: bash

    APIs/
        lua/
            DOCUMENTATION.rst
            README.rst
            ...
        matlab/
            DOCUMENTATION.rst
            README.rst
            ...
        ...


.. _documentation_sec:

Documentation
-------------

The ``docs/`` directory contains the documentation files. We use `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ to build
our documentation and `Read The Docs <https://readthedocs.org/>`_ to host it.
The structure of ``docs/`` is similar to most docs using Sphinx:

.. code-block:: bash

    docs/
        build/
        source/
        make.bat
        Makefile


.. _tests_sec:

Tests
-----

All tests are organized under the ``tests/`` directory by language and functionality. The project uses two types of tests to
check for bugs: `unit tests <https://stackoverflow.com/questions/652292/what-is-unit-testing-and-how-do-you-do-it>`_
and `functional tests <https://stackoverflow.com/questions/2741832/unit-tests-vs-functional-tests>`_. Unit tests are used to test
the core functions of the package and functional tests are used to test the execution of downloading and installing a dataset.

The directory is organized as follows:

.. code-block:: bash

    tests/
        lua/
            unit/
            functional/
        matlab/
            unit/
            functional/
        python/
            unit/
                test_A.py
                test_B.py
                test_C.py
                ...
            functional/


.. _notebooks_sec:

Notebooks
---------

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