.. _how_to_contribute:

How to Contribute
=================

Contributing to dbcollection
----------------------------

There are many ways to contribute to the dbcollection project: logging bugs,
submitting pull requests, reporting issues and creating suggestions.



Adding a Feature
----------------

TODO


Adding a Dataset
----------------

TODO


Unit Testing
------------

TODO


Pull Requests
-------------

Good pull requests - patches, improvements, new features - are a fantastic help.
They should remain focused in scope and avoid containing unrelated commits.

To enable us to quickly review and accept your pull requests, always create one
pull request per issue and `link the issue in the pull request <https://github.com/blog/957-introducing-issue-mentions>`_.
Never merge multiple requests in one unless they have the same root cause.
Be sure to follow our :ref:`Coding Guidelines <code_guidelines>` and keep code
changes as small as possible. Avoid pure formatting changes to code that has not been modified otherwise. Pull requests should contain tests whenever possible.


Where to Contribute
^^^^^^^^^^^^^^^^^^^

Check out the full issues list for a list of all potential areas for contributions (if any).
Note that just because an issue exists in the repository does not mean we will accept every contribution to the core project.
There are several reasons to not accept a pull request like:

- Performance - One of dbcollection's main concerns is to deliver a simple, yet moderately fast dataset manager.
  This means it should perform fast enough when downloading/parsing data.
- User experience - Since the goal is to make user's life easy,
  the use experience should feel confortable enough to encourage
  using the package. This means that the interface should provide
  enough information of what's going on, but not overwhelm the user with
  unnecessary information of what's going on the background.
- Architectural - The community and/or feature owner needs to agree with any
  architectural impact a change may make. Things like new language APIs *should*
  be discussed with and agreed upon by the feature owner.

To improve the chances to get a pull request merged you should select an issue that is
labelled with the `help-wanted <https://github.com/farrajota/dbcollection/labels/help-wanted>`_
or `bug <https://github.com/farrajota/dbcollection/labels/bug>`_ labels. If the issue you want to
work on is not labelled with ``help-wanted`` or ``bug``, you can start a conversation with the
issue owner asking whether an external contribution will be considered.



Suggestions
-----------

We're also interested in your feedback for the future of this project.
You can submit a suggestion or feature request through the issue
tracker. To make this process more effective, we're asking that
these include more information to help define them more clearly.