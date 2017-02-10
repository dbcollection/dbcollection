#!/usr/bin/env python3

"""
string_ascii.py unit testing.
"""


import os
import sys
import numpy as np

import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..', '..', 'dbcollection', 'utils'))
sys.path.append(lib_path)
from string_ascii import *


#-----------------------
# Unit Test definitions
#-----------------------

class Str2AsciiTest(unittest.TestCase):
    """
    Test class.
    """

    def test_str_to_ascii(self):
        """
        Test converting a string to an ascii numpy array
        """
        # sample data
        sample_string = 'test'
        sample_res = np.array([116, 101, 115, 116], dtype=np.uint8)

        # convert str to ascii
        res = str_to_ascii(sample_string)

        # check if the arrays are the same
        self.assertEqual(res.tolist(), sample_res.tolist(), 'Arrays should be equal')


    def test_ascii_to_str(self):
        """
        Test converting a a ascii numpy array to a string of characters.
        """
        # sample data
        sample_array = np.array([116, 101, 115, 116], dtype=np.uint8)
        sample_string = 'test'

        # convert ascii to str
        res = ascii_to_str(sample_array)

        # check if the strings are the same
        self.assertEqual(res, sample_string, 'Strings should be equal')


    def test_convert_str_to_ascii__single_string(self):
        """
        Test converting a single string into a numpy array.
        """
        # sample data
        sample_string = 'test'
        sample_res = np.array([116, 101, 115, 116, 0], dtype=np.uint8)

        # convert str to ascii
        res = convert_str_to_ascii(sample_string)

        # check if the arrays are the same
        self.assertEqual(res.tolist(), sample_res.tolist(), 'Arrays should be equal')


    def test_convert_str_to_ascii__list_of_strings(self):
        """
        Test converting a list of strings string into a numpy array (matrix).
        """
        # sample data
        sample_string_list = ['test1', 'test2', 'test3']
        sample_res = np.array([[116, 101, 115, 116, 49, 0], \
                               [116, 101, 115, 116, 50, 0], \
                               [116, 101, 115, 116, 51, 0]],\
                               dtype=np.uint8)

        # convert str to ascii
        res = convert_str_to_ascii(sample_string_list)

        # check if the arrays are the same
        self.assertEqual(res.tolist(), sample_res.tolist(), 'Arrays should be equal')


    def test_convert_ascii_to_str__single_array(self):
        """
        Test converting a numpy array into a single string of characters.
        """
        # sample data
        sample_array = np.array([116, 101, 115, 116, 0], dtype=np.uint8)
        sample_string = 'test'

        # convert ascii to str
        res = convert_ascii_to_str(sample_array)

        # check if the strings are the same
        self.assertEqual(res, sample_string, 'Strings should be equal')


    def test_convert_ascii_to_str__matrix_array(self):
        """
        Test converting a numpy matrix into a list of string of characters.
        """
         # sample data
        sample_matrix = np.array([[116, 101, 115, 116, 49, 0], \
                               [116, 101, 115, 116, 50, 0], \
                               [116, 101, 115, 116, 51, 0]],\
                               dtype=np.uint8)
        sample_string_list = ['test1', 'test2', 'test3']

        # convert ascii to str
        res = convert_ascii_to_str(sample_matrix)

        # check if the strings are the same
        self.assertEqual(res, sample_string_list, 'Lists should be equal')


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
