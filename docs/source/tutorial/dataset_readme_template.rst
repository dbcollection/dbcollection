Template of a dataset README.rst file
=====================================

When creating a dataset, its good idea to provide a small documentation of the structure and information of the data.

When creating such documentation, it is good practice to follow a common format to keep things similar.

The following scheme details a template format on how to write the documentation of a new dataset and what information to provide to the end user.

.. code-block:: bash

    Dataset Name
    ============

    <small intro covering the dataset.>

    <bonus: some sample images of the dataset are always good to have.
    Visual aid is often good enough to help dismiss a dataset before delving into the details of the data.>

    Properties
    ^^^^^^^^^^

    - name: <name alias of the dataset>
    - tasks:
        - classification:
    - data size: <total size of the dataset on disk>
    - metadata size: <total size of the processed hdf5 metdata file on disk for all tasks>
    - keywords: <keywords assign to the dataset. Example: object detection, pedestrians, keypoints, etc.>
    - has annotations: (yes - full, yes - partial, no)
        - which: <list of relevant types of annotations it has. Example: labels, bbox, masks, etc.>
    - is downloadable: (yes - full, yes - partial, no)
        - note: <any particular reason needed to be clarified here>

    Data structure (hdf5)
    ^^^^^^^^^^^^^^^^^^^^^

    <hdf5 data structure for each task>


    Source
    ^^^^^^

    <info of the websiter where the dataset was retrieved from.
    It should containg a link to the original website/source.>