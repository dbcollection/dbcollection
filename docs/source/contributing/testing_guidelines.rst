.. _test_guidelines:

Testing guidelines
==================

First off - thank you for writing test cases - they're really important.

Moreover, testing is an important part of submitted code. You should test your
code by unit/functional tests following our testing guidelines. Note that we
are using the ``pytest`` and the ``mock`` packages for testing, so
install these packages before writing your code::

    $ pip install pytest mock


Typical imports
---------------

.. code-block:: python

    import pytest
    import mock
    import dbcollection


Making your tests behave well
-----------------------------

Test cases are run after every change (as does Travis),
so it's important that you make your tests well-behaved.
With this in mind, it's important that your test cases cover the functionality
of your addition, so that when others make changes, they can be confident
that they aren't introducing errors in your code.

Also, strive to fully test your code, but don't get too obsess over the coverage score.


.. _unit_tests:

Unit tests
----------

We use ``pytest`` for unit testing our code. This framework
makes it easy to write small tests and it has an automatic test discovery mechanism.
This requires that tests have to be written in a certain way:

- ``pytest`` will run all files in the current directory and its subdirectories
  of the form ``test_*.py`` or ``*_test.py``.
- From those files, collected test items require functions or methods outside of a class to start with the prefix ``test_``.

.. note::

    For more information about ``pytest`` testing practices see its `documentation <https://docs.pytest.org/en/latest/goodpractices.html#goodpractices>`_.


Besides the conventions required by ``pytest``, use these general testing guidelines when writting tests:

- Use long, descriptive names.
- Focus on one bit of functionality.
- Should be fast, but a slow test is better than no test.
- All tests must pass. Moreover, don't let incomplete tests pass.


.. _functional_tests:

Functional tests
----------------

Functional tests are higher level tests that should be used to test
new dataset implementations to check for errors, and are necessary
for every submission of a new dataset.

When naming functional tests methods, use the convention ``<api_method>_<dataset_name>``
and store them in the appropriate language folder in the ``tests/`` directory.

Any functional tests must follow a common guideline for clarity purposes.
Please consider using the following convention when writting your tests:

.. code-block:: python

    #!/usr/bin/env python3

    """
    Test loading cifar10.
    """

    import os
    from dbcollection.utils.test import TestBaseDB


    # setup
    name = 'cifar10'
    task = 'classification'
    data_dir = ''
    verbose = True

    # Run tester
    tester = TestBaseDB(name, task, data_dir, verbose)
    tester.run('load')


Hook up travis-ci
-----------------

We use travis for testings the entire library across various python versions.
If you `hook up your fork to run travis <https://docs.travis-ci.com/user/getting-started/>`_,
then it is displayed prominently whether your pull request passes or fails the testing suite.
This is incredibly helpful.

If it shows that it passes, great! We can consider merging.
If there's a failure, this let's you and us know there is something wrong,
and needs some attention before it can be considered for merging.

Sometimes Travis will say a change failed for reasons unrelated to your pull
request. For example there could be a build error or network error.
To get Travis to retest your pull request, do the following::

    $ git commit --amend -C HEAD
    $ git push origin <yourbranch> -f