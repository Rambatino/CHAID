"""
Testing module for the class OrdinalColumn
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal, list_unordered_equal, CHAID

def test_all_ordinal_combinations():
    arr = np.array([1.0, 2.0, 3.0, 4.0])
    ordinal = CHAID.OrdinalColumn(arr)
    assert [
        i for i in ordinal.all_combinations()
    ] == [[[1], [2, 3, 4]],
         [[1, 2], [3, 4]],
         [[1], [2], [3, 4]],
         [[1, 2, 3], [4]],
         [[1], [2, 3], [4]],
         [[1, 2], [3], [4]],
         [[1], [2], [3], [4]]]

def test_all_ordinal_combinations_with_nan():
    arr = np.array([1.0, 2.0, 3.0, np.nan])
    ordinal = CHAID.OrdinalColumn(arr)
    nan_val = np.array([np.nan]).astype(int)[0]
    assert [
        i for i in ordinal.all_combinations()
    ] == [[[nan_val], [1, 2, 3]],
          [[nan_val, 1], [2, 3]],
          [[1], [nan_val, 2, 3]],
          [[nan_val], [1], [2, 3]],
          [[nan_val, 1, 2], [3]],
          [[1, 2], [nan_val, 3]],
          [[nan_val], [1, 2], [3]],
          [[nan_val, 1], [2], [3]],
          [[1], [nan_val, 2], [3]],
          [[1], [2], [nan_val, 3]],
          [[nan_val], [1], [2], [3]]]

class TestOrdinalDeepCopy(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for copy tests"""
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
        possible_groupings = [(1, 2), (2, 3), (3, 4), (4, 5)]
        assert list_unordered_equal(possible_groupings, groupings), 'Without NaNs, with groups are identified, possible grouping are incorrectly identified.'

        groups = list(self.col.groups())
        actual_groups = [[1], [2], [3], [4], [5], [10]]
        assert list_unordered_equal(actual_groups, groups), 'Without NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_grouping(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3, 4)
        self.col.group(3, 2)

        groupings = list(self.col.possible_groupings())
        possible_groupings = [(1, 3), (3, 5)]
        assert list_unordered_equal(possible_groupings, groupings), 'Without NaNs, with groups are identified, possible grouping are incorrectly identified.'

        groups = list(self.col.groups())
        actual_groups = [[1], [2, 3, 4], [5], [10]]
        assert list_unordered_equal(actual_groups, groups), 'Without NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_copy(self):
        """ Ensure a copy actually happens when deep_copy is called """
        self.col.group(3, 4)
        self.col.group(3, 2)
        col = self.col.deep_copy()

        groupings = list(col.possible_groupings())
        possible_groupings = [(1, 3), (3, 5)]
        assert list_unordered_equal(possible_groupings, groupings), 'Without NaNs, with groups are identified, possible grouping are incorrectly identified.'

        groups = list(col.groups())
        actual_groups = [[1], [2, 3, 4], [5], [10]]
        assert list_unordered_equal(actual_groups, groups), 'Without NaNs, before any groups are identified, actual groupings are incorrectly reported'


class TestOrdinalWithObjects(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for grouping tests """
        arr = np.array(
            [1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0, 10.0, None],
            dtype=object
        )
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure possible groups are only adjacent numbers  """
        metadata = self.col.metadata
        groupings = [(metadata[x], metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0), (1.0, '<missing>'), (2.0, '<missing>'), (3.0, '<missing>'),
            (4.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, before any groups are identified, possible grouping are incorrectly calculated.'

        groups = list(self.col.groups())
        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0], [3.0], [4.0], [5.0], ['<missing>'], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_grouping(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = [(self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0), (1.0, '<missing>'), (3.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups are identified, possible grouping incorrectly identified.'

        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0], ['<missing>']]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups identified, actual groupings are incorrectly reported'

    def test_groups_grouping_with_nan(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups containing nans"""
        self.col.group(4.0, self.col._nan)
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = [(self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0)
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups containing nan identified, possible grouping incorrectly identified.'

        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0, '<missing>'], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups containing nan identified, actual groupings are incorrectly reported'

    def test_groups_after_copy(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)
        col = self.col.deep_copy()

        groupings = [(col.metadata[x], col.metadata[y]) for x, y in col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0), (1.0, '<missing>'), (3.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups are identified, possible grouping incorrectly identified.'

        groups = [[col.metadata[i] for i in group] for group in col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0], ['<missing>']]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups identified, actual groupings are incorrectly reported'

    def test_groups_after_copy_with_nan(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups containing nans"""
        self.col.group(3.0, 4.0)
        self.col.group(3.0, self.col._nan)
        self.col.group(3.0, 2.0)
        col = self.col.deep_copy()

        groupings = [(col.metadata[x], col.metadata[y]) for x, y in col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0)
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups containing nan identified, possible grouping incorrectly identified.'

        groups = [[col.metadata[i] for i in group] for group in col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0, '<missing>'], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups containing nan identified, actual groupings are incorrectly reported'


class TestOrdinalGroupingWithnan(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for grouping tests """
        arr = np.array([1.0, 2.0, nan, 3.0, 3.0, nan, 3.0, 3.0, nan, 4.0, 5.0, 10.0])
        self.col = CHAID.OrdinalColumn(arr)

    def test_possible_groups(self):
        """ Ensure possible groups are only adjacent numbers  """
        metadata = self.col.metadata
        groupings = [(metadata[x], metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0), (1.0, '<missing>'), (2.0, '<missing>'), (3.0, '<missing>'),
            (4.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, before any groups are identified, possible grouping are incorrectly calculated.'

        groups = list(self.col.groups())
        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0], [3.0], [4.0], [5.0], ['<missing>'], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, before any groups are identified, actual groupings are incorrectly reported'

    def test_groups_after_grouping(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = [(self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0), (1.0, '<missing>'), (3.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups are identified, possible grouping incorrectly identified.'

        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0], ['<missing>']]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups identified, actual groupings are incorrectly reported'

    def test_groups_grouping_with_nan(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups containing nans"""
        self.col.group(4.0, self.col._nan)
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)

        groupings = [(self.col.metadata[x], self.col.metadata[y]) for x, y in self.col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0)
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups containing nan identified, possible grouping incorrectly identified.'

        groups = [[self.col.metadata[i] for i in group] for group in self.col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0, '<missing>'], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups containing nan identified, actual groupings are incorrectly reported'

    def test_groups_after_copy(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups """
        self.col.group(3.0, 4.0)
        self.col.group(3.0, 2.0)
        col = self.col.deep_copy()

        groupings = [(col.metadata[x], col.metadata[y]) for x, y in col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0), (1.0, '<missing>'), (3.0, '<missing>'), (5.0, '<missing>'), (10.0, '<missing>')
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups are identified, possible grouping incorrectly identified.'

        groups = [[col.metadata[i] for i in group] for group in col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0], [5.0], [10.0], ['<missing>']]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups identified, actual groupings are incorrectly reported'

    def test_groups_after_copy_with_nan(self):
        """ Ensure possible groups are only adjacent numbers after identifing some groups containing nans"""
        self.col.group(3.0, 4.0)
        self.col.group(3.0, self.col._nan)
        self.col.group(3.0, 2.0)
        col = self.col.deep_copy()

        groupings = [(col.metadata[x], col.metadata[y]) for x, y in col.possible_groupings()]
        possible_groupings = [
            (1.0, 3.0), (3.0, 5.0)
        ]
        assert list_unordered_equal(possible_groupings, groupings), 'With NaNs, with groups containing nan identified, possible grouping incorrectly identified.'

        groups = [[col.metadata[i] for i in group] for group in col.groups()]
        actual_groups = [[1.0], [2.0, 3.0, 4.0, '<missing>'], [5.0], [10.0]]
        assert list_unordered_equal(actual_groups, groups), 'With NaNs, with groups containing nan identified, actual groupings are incorrectly reported'

class TestOrdinalConstructor(TestCase):
    """ Test fixture class for testing external Ordinal contruction """
    def setUp(self):
        """ Setup for tests """
        arr_with_nan = np.array([1.0, 2.0, nan, 3.0, 3.0, nan, 3.0])
        self.col_with_nan = CHAID.OrdinalColumn(arr_with_nan, {1.0: 'first', 2.0: 'second', 3.0: 'third'})

    def test_correctly_subs_nan_values(self):
        assert self.col_with_nan.arr[2] == self.col_with_nan._nan

    def test_correctly_subs_floats_for_ints(self):
        assert np.issubdtype(self.col_with_nan.arr.dtype, np.integer)

    def test_correctly_subs_floated_metadata(self):
        assert self.col_with_nan.metadata == {self.col_with_nan._nan: '<missing>', 1: 'first', 2: 'second', 3: 'third'}
