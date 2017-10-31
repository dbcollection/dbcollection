.. _utils_reference:

utils
================================
.. automodule:: dbcollection.utils


Url download
--------------------------------
.. automodule:: dbcollection.utils.url
.. autofunction:: check_url_exists
.. autofunction:: download_extract_all
.. autofunction:: download_url
.. autofunction:: download_url_requests
.. autofunction:: download_url_google_drive
.. autofunction:: get_hash_value
.. autofunction:: md5_checksum
.. autofunction:: parse_url


File loading
--------------------------------
.. automodule:: dbcollection.utils.file_load
.. autofunction:: load_json
.. autofunction:: load_matlab
.. autofunction:: load_pickle
.. autofunction:: load_txt
.. autofunction:: load_xml


Padding
--------------------------------
.. automodule:: dbcollection.utils.pad
.. autofunction:: pad_list
.. _utils_reference_unpad_list:
.. autofunction:: unpad_list
.. autofunction:: squeeze_list
.. autofunction:: unsqueeze_list


String<->ASCII
--------------------------------
.. automodule:: dbcollection.utils.string_ascii
.. autofunction:: convert_str_to_ascii
.. _utils_reference_convert_ascii_to_str:
.. autofunction:: convert_ascii_to_str
.. autofunction:: str_to_ascii
.. autofunction:: ascii_to_str


HDF5
--------------------------------
.. automodule:: dbcollection.utils.hdf5
.. autofunction:: hdf5_write_data


Dir db constructor
--------------------------------
.. automodule:: dbcollection.utils.os_dir
.. autofunction:: construct_dataset_from_dir
.. autofunction:: construct_set_from_dir
.. autofunction:: dir_get_size


Test
--------------------------------
.. automodule:: dbcollection.utils.test

TestBaseDB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: TestBaseDB
   :members:


Third party modules
--------------------------------
.. automodule:: dbcollection.utils.db

caltech_pedestrian_extractor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: dbcollection.utils.db.caltech_pedestrian_extractor.converter
.. autofunction:: extract_data

