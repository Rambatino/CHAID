"""
Testing module for the class NominalColumn
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal,list_unordered_equal, CHAID

NAN = float('nan')

class TestOrdinalDeepCopy(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for copy tests"""
        # Use string so numpy array dtype is object and may store references
        arr = np.array([1, 2, 3, 3, 3, 3])
        self.orig = CHAID.OrdinalColumn(arr)
        self.copy = self.orig.deep_copy()

    def test_deep_copy_does_copy(self):
        """ Ensure a copy actually happens when deep_copy is called """
        assert id(self.orig) != id(self.copy), 'The vector objects must be different'
        assert list_ordered_equal(self.copy, self.orig), 'Vector contents must be the same'

    def test_changing_copy(self):
        """ Test that altering the copy doesn't alter the original """
        self.copy.arr[0] = 55.0
        assert not list_ordered_equal(self.copy, self.orig), 'Altering one vector should not affect the other'

    def test_metadata(self):
        """ Ensure metadata is copied correctly or deep_copy """
        assert self.copy.metadata == self.orig.metadata, 'Copied metadata should be equivilent'

class TestOrdinalGrouping(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for grouping tests """
        arr = np.array([1, 2, 3, 3, 3, 3, 4, 5, 10])
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure a groupings are only adjacent numbers  """
        groupings = list(self.col.possible_groupings())
        expected_groupings = [(1, 2), (2, 3), (3, 4), (4, 5)]
        assert list_unordered_equal(expected_groupings, groupings)

    def test_groups_after_grouping(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3, 4)
        self.col.group(3, 2)
        groupings = list(self.col.possible_groupings())
        expected_groupings = [(1, 3), (3, 5)]
        assert list_unordered_equal(expected_groupings, groupings)

class TestOrdinalGroupingWithNAN(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for grouping tests """
        arr = np.array([1, 2, NAN, 3, 3, NAN, 3, 3, NAN, 4, 5, 10])
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure a groupings are only adjacent numbers  """
        groupings = list(self.col.possible_groupings())
        expected_groupings = [
            (1, 2), (2, 3), (3, 4), (4, 5), (1, NAN), (2, NAN), (3, NAN),
            (4, NAN), (5, NAN), (10, NAN)
        ]
        assert list_unordered_equal(expected_groupings, groupings)

    def test_groups_after_grouping(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3, 4)
        self.col.group(3, 2)
        groupings = list(self.col.possible_groupings())
        expected_groupings = [
            (1, 3), (3, 5), (1, NAN), (3, NAN), (5, NAN), (10, NAN)
        ]
        assert list_unordered_equal(expected_groupings, groupings)