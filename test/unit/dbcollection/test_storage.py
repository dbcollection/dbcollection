"""
dbcollection/storage.py unit testing.
"""


# import data.py
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..','dbcollection'))
sys.path.append(lib_path)
import storage

import unittest
from unittest import mock
from unittest.mock import patch, mock_open


#-----------------------
# Unit Test definitions
#-----------------------

class StorageHDF5Test(unittest.TestCase):
    """
    Test class.
    """

    @patch("storage.StorageHDF5.open_file")
    @patch("storage.StorageHDF5.add_group")
    def setUp(self, mock_group, mock_file):
        """
        Initialize class.
        """
        # dummy file name
        sample_file_name = 'dir/myfile.h5'
        sample_mode = 'w'

        # mock function
        mock_file.return_value = {'test':{}}
        mock_group.return_value = True

        # Load a hdf5 file manager
        self.storage = storage.StorageHDF5(sample_file_name, sample_mode)

        # check if the filenames are the same
        self.assertEqual(self.storage.fname, sample_file_name, 'File names should be equal')
        self.assertEqual(self.storage.mode, sample_mode, 'Mode string/char should be equal')


    @patch("h5py.File")
    def test_open_file(self, mock_h5file):
        """
        Test opening a hdf5 file.
        """
        # some dummy file name
        sample_file_name = 'myfile.h5'
        sample_mode = "w"

        # mock function (modify output)
        mock_h5file.return_value = True

        # open the file
        res = self.storage.open_file(sample_file_name, sample_mode)

        # check if the file open successfuly
        self.assertTrue(res, 'Should have given True')


    @patch("storage.StorageHDF5.add_group")
    def test_add_group(self, mock_add_group):
        """
        Test creating groups in the hdf5 file.
        """
        # some dummy groups
        sample_names = ['test1', 'test2', 'test3']
        sample_return_value = 'test'

        # mock function (define output)
        mock_add_group.return_value = sample_return_value

        # create groups
        grp1 = self.storage.add_group(sample_names[0])
        grp2 = self.storage.add_group(sample_names[1])
        grp3 = self.storage.add_group(sample_names[2])

        # check if the created groups match the input names
        self.assertEqual(grp1, sample_return_value, 'Strings shoudl be the same')
        self.assertEqual(grp2, sample_return_value, 'Strings shoudl be the same')
        self.assertEqual(grp3, sample_return_value, 'Strings shoudl be the same')



#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
