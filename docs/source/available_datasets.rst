Available Datasets
==================

.. toctree::
   :glob:
   :maxdepth: 1

   datasets/*

.. note::
    All datasets have been parsed by hand and they contain the most of the original raw annotations and, for some, there is
    available cleaned annotations as well. Some annotations have been discarded because they are not useful enough to the
    task which the dataset has been designed for and offer mostly context information (like urls), so check out the datasets info
    for more information about which annotations a dataset contains.

.. warning::
    Most datasets store the original data in a nested folder format in the ``source`` group in the ``hdf5`` metadata file.
    For some APIS, due to the size of the dataset, this nested folder may contain alot of data stored in a nested format,
    which causes some APIs to load the nested structured as the file is loaded to memory (``lua/torch7`` API suffers from
    this issue). To overcome this problem, all tasks have a version withouth this group in their metadata file.
    To load this version, simply append to the end of the task name the suffix ``_d``. Loading times should improve for this
    case.
