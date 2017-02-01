#!/usr/bin/env python3

"""
file.py unit testing.
"""


import unittest
from unittest import mock
from unittest.mock import patch, mock_open


#-----------------------
# Unit Test definitions
#-----------------------

class UtilsTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        self.widget = Widget('widget')

    def test_one(self):
        """
        Test one.
        """
        self.assertEqual(self.widget.size(), 1,
             'incorrect default size')

    def test_two(self):
        """
        Test two.
        """
        self.assertEqual(self.widget.size(), 2,
             'incorrect default size')


#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
