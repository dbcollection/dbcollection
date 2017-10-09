.. _how_to_contribute:

How to contribute
=================

This section describes a way to contribute to the project. You are welcome to provide with code or ideas
to help improve the pool of functionality this package offers. You can also help by answering questions or
helping out with documentation if you prefer.

.. note::
    The main goal behind contributing to this project is to provide tools for the community to help 
    accelerate research and share code with others in a simple and easy way.


Contributing to the project
---------------------------

There are many ways to contribute to the dbcollection project: finding bugs,
submitting pull requests, reporting issues and creating suggestions.


Using the issue tracker
-----------------------

The issue tracker is the preferred channel for :ref:`bug reports <submit_bugs>`,
:ref:`features requests <feature_request>` and :ref:`submitting pull requests <pull_request>`.
You can also use `Stack Overflow <https://stackoverflow.com/questions/tagged/dbcollection>`_
to get feedback about your questions.


.. _feature_request:

Feature requests
----------------

Feature requests are welcome to be filed. The purpose of feature requests is for others who are looking to implement
a feature are aware of the interest in the feature. At the time of writting, this project is solely
maintained by a single maintainer (me, on my free time), so please be considerate if it takes a little longer to get feedback
on your requests.


.. _pull_request:

Pull requests
-------------

Good pull requests - patches, improvements, new features, new datasets - are a fantastic help.
They should remain focused in scope and avoid containing unrelated commits.

To enable us to quickly review and accept your pull requests, always create one
pull request per issue and `link the issue in the pull request <https://github.com/blog/957-introducing-issue-mentions>`_.
Never merge multiple requests in one unless they have the same root cause.
Be sure to follow our :ref:`Coding Guidelines <code_guidelines>` and :ref:`Testing Guidelines <test_guidelines>` and keep code
changes as small as possible. Avoid pure formatting changes to code that has not been modified otherwise.
Pull requests should contain tests whenever possible.


You can use the following process to create a pull request for this project:

#. `Fork <https://help.github.com/articles/fork-a-repo/>`_  the project, clone your fork, and configure the remotes::

    $ # Clone your fork of the repo into the current directory
    $ git clone https://github.com/<your-username>/dbcollection.git
    $ # Navigate to the newly cloned directory
    $ cd dbcollection
    $ # Assign the original repo to a remote called "upstream"
    $ git remote add upstream https://github.com/farrajota/dbcollection.git

#. If you have cloned the repository a while ago, get the latest changes from upstream::

    $ git checkout master
    $ git pull upstream master

#. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix::

    $ git checkout -b <topic-branch-name>

#. Commit your changes in logical chunks. Use `Git's interactive rebase <https://help.github.com/articles/about-git-rebase/>`_
   feature to tidy up/organize your commits before making them public.
   This helps to keep the commit history in logical blocks and clean. For example:

   - If you are adding a new function or a dataset, keep the function/dataset + tests + doc to a single commit unless logically warranted.
   - If you are fixing a bug, keep the bugfix to a single commit unless logically warranted.

   .. note::

        If you are fairly new to git or not very familiar with git conventions, please try to adhere to these
        `git commit message guidelines <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_
        before committing to the project.

#. Locally merge (or rebase) the upstream development branch into your topic branch::

    $ git pull [--rebase] upstream master

#. Push your topic branch up to your fork::

    $ git push origin <topic-branch-name>

#. `Open a Pull Request <https://help.github.com/articles/about-pull-requests/>`_  with a clear title and description.


Where to contribute
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