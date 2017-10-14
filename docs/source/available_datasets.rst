.. _available_datasets:

==================
Available datasets
==================

Several datasets are available for users to load/download via this package. The majority of these datasets
are for computer vision tasks, but more datasets for tasks such as natural language processing are being added.

The following list of datasets contains detailed information about how datasets are stored,
along with other properties that you may find useful to know about any available dataset.

.. toctree::
   :glob:
   :maxdepth: 1

   datasets/*

.. note::
    All datasets have been parsed by hand and they contain most of the important annotations. For some, there are also
    available versions where bad annotations have been removed/discarded. This may be due to wrongly annotated data or
    because some fields don't provide any useful information. If you'd like to know more, check out the datasets information
    available here on this page or the source websites of the datasets you are looking for.



.. warning::
    Many datasets have a tree structure of folder of how their annotations is stored.
    Of the available datasets provided by this project, this sturctured information is available
    in the form of ``HDF5`` groups in each set under a main group named ``raw/``. By default, 
    this information is disabled, so in order to grab this information you can use a special suffix 
    attached at the end of a task name to enable this. To do so, simply append to the end of the task name the suffix ``_s``.
    Note that if a dataset does not have this data setup, it will simply skip this step.
