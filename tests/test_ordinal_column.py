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
        arr = np.array([1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0, 10.0])
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure possible groups are only adjacent numbers  """
        groupings = list(self.col.possible_groupings())
        possible_groupings = [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0)]
        assert list_unordered_equal(possible_groupings, groupings), 'Without NaNs, with groups are identified, possible grouping are incorrectly identified.'

        groups = list(self.col.groups())
        actual_groups = [[1.0], [2.0], [3.0], [4.0], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'Without NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_grouping(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = list(self.col.possible_groupings())
        possible_groupings = [(1.0, 3.0), (3.0, 5.0)]
        assert list_unordered_equal(possible_groupings, groupings), 'Without NaNs, with groups are identified, possible grouping are incorrectly identified.'

        groups = list(self.col.groups())
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'Without NaNs, before any groups are identified, actual groupings are incorrectly reported'

class TestOrdinalGroupingWithNAN(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for grouping tests """
        arr = np.array([1.0, 2.0, NAN, 3.0, 3.0, NAN, 3.0, 3.0, NAN, 4.0, 5.0, 10.0])
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure possible groups are only adjacent numbers  """
        groupings = [ (self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0), (1.0, '<missing>'), (2.0, '<missing>'), (3.0, '<missing>'),
            (4.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, before any groups are identified, possible grouping are incorrectly calculated.'

        groups = list(self.col.groups())
        groups = [ [self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0], [3.0], [4.0], [5.0], ['<missing>'], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_grouping(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = [ (self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0), (1.0, '<missing>'), (3.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups are identified, possible grouping incorrectly identified.'

        groups = [ [self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0], ['<missing>']]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, before any groups are identified, actual groupings are incorrectly reported'
