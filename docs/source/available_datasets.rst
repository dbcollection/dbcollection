.. _available_datasets:

==================
Available datasets
==================

Here you can find a list of all available datasets for load/download on this package. The majority of these datasets
are for computer vision tasks, but other tasks such as natural language processing are being added to this list.
If you have any suggestion for a well needed dataset, please feel free to write an `issue on GitHub <https://github.com/dbcollection/dbcollection/issues>`_
detailing the new proposal or submit a pull request with an implementation of your proposal.
For more information about contributing to this project, please check out the :ref:`Contributing <contributing_index>` section of this docs.

The following list of datasets contains detailed information about how datasets are stored,
along with other properties that you may find useful to know about when using them.

.. toctree::
   :glob:
   :maxdepth: 1

   datasets/*

.. note::
    All datasets have been parsed by hand and contain most of their relevant annotations. For some, there are also
    some versions where badly/wrongly annotated information has been discarded. This may be due to wrongly annotated data or
    because some fields don't provide any useful information as is. If you would like to know more, check out the datasets information
    available on this page or check the dataset's source website you would like to learn more about.


.. warning::
    Many datasets have a tree structure of folder of how their annotations is stored.
    Of the available datasets provided by this project, this sturctured information is available
    in the form of ``HDF5`` groups in each set under a main group named ``raw/``. By default,
    this information is disabled, so in order to grab this information you can use a special suffix
    attached at the end of a task name to enable this. To do so, simply append to the end of the task name the suffix ``_s``.
    Note that if a dataset does not have this data setup, it will simply skip this step.
