.. _code_guidelines:

Coding Guidelines
=================

Here we use `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ as our basic style guideline for
all Python code.

For other languages, we try to follow a similar style like in ``PEP8``.
Exception to this rule goes to languages where the general trend diverges too much from the basic guideline used here (e.g., Java),
so adopting those conventions is allowed.


Cross-compatible code
---------------------

Not all functions are available between versions. It's important to
write code that will be compatible from Python 2.6 through the most
recent version of Python 3.


Indentation
-----------

Use 4 spaces for identation. Don't use tabs.


Names
-----

- Variables, functions, methods, packages, modules
    - ``lower_case_with_underscores``
- Classes and Exceptions
    - ``CapWords``
- Protected methods and internal functions
    - ``_single_leading_underscore(self, ...)``
- Private methods
    - ``__double_leading_underscore(self, ...)``
- Constants
    - ``ALL_CAPS_WITH_UNDERSCORES``

DocStrings
----------

We follow `Numpy's docstring style <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_ for documenting methods and classes.
For core API functions and methods, please try to follow as close as possible the conventions used in the code.
For methods defining datasets, a simple docstring is allowed.

Use one-line docstrings for obvious functions.

.. code-block:: python

    """Return the pathname of ``foo``."""


Multiline docstrings should include

- Summary line
- Use case, if appropriate
- Parameters
- Return type and semantics, unless ``None`` is returned
- Exceptions (if any is raised)

.. code-block:: python

    def function_with_types_in_docstring(param1, param2):
        """Example function with types documented in the docstring.

        `PEP 484`_ type annotations are supported. If attribute, parameter, and
        return types are annotated according to `PEP 484`_, they do not need to be
        included in the docstring:

        Parameters
        ----------
        param1 : int
            The first parameter.
        param2 : str
            The second parameter.

        Returns
        -------
        bool
            True if successful, False otherwise.

        .. _PEP 484:
            https://www.python.org/dev/peps/pep-0484/

        """