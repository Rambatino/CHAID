"""
Testing module for the class NominalColumn
"""
from unittest import TestCase
import numpy as np
import pytest
from numpy import nan
from setup_tests import list_ordered_equal, CHAID


@pytest.mark.parametrize('arr', [
    np.array([-1, 0, 1, -1]),
    np.array([-0.5, 0.0, 1.0, -0.5]),
    np.arange(-128, 128, dtype=np.int8),
    np.array(list('abcdefghijkl')),
    np.array(list('abcdefghijkl'), dtype='S1'),
    np.array(['0', '1', '2', '10']),
    np.array([False, True, False]),
    np.array([-1, 0, 1, 'a', '0', -1], dtype=object),
])
def test_category_encoding_preserves_original_values(arr):
    original = arr.copy()
    column = CHAID.NominalColumn(arr)

    assert [column.metadata[code] for code in column.arr] == arr.tolist()
    assert len(np.unique(column.arr)) == len(set(arr.tolist()))
    assert column.arr.dtype == np.float64
    np.testing.assert_array_equal(arr, original)


@pytest.mark.parametrize('arr, expected', [
    (np.array([np.nan, -1, 0, np.nan]), ['<missing>', -1, 0, '<missing>']),
    (np.array([np.nan, np.nan]), ['<missing>', '<missing>']),
    (np.array([np.nan, 0, -1, np.nan], dtype=object), ['<missing>', 0, -1, '<missing>']),
    (np.array([np.float32('nan'), 'a', 0, np.nan], dtype=object), ['<missing>', 'a', 0, '<missing>']),
    (np.array([], dtype=float), []),
])
def test_category_encoding_preserves_missing_values(arr, expected):
    column = CHAID.NominalColumn(arr)

    assert [column.metadata[code] for code in column.arr] == expected
    assert (column.arr == -1).tolist() == [value == '<missing>' for value in expected]
    assert all(value == value for value in column.metadata.values())


def test_category_encoding_keeps_sorted_category_ids():
    column = CHAID.NominalColumn(np.array(['z', 'a', 'm', 'a']))

    assert column.metadata == {0: 'a', 1: 'm', 2: 'z'}
    np.testing.assert_array_equal(column.arr, [2, 0, 1, 0])


def test_chaid_vector_converts_strings():
    """
    Check that the metadata is correct when NominalColumns are created from
    strings
    """
    arr = np.array(['2', '4'])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: '2', 1: '4'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_ints():
    """
    Check that the metadata is correct when NominalColumns are created from ints
    """
    arr = np.array([1, 2])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_ints_and_nan():
    """
    Check that the metadata is correct when NominalColumns are created from ints
    """
    arr = np.array([1, 2, np.nan])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2, -1: '<missing>'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_floats():
    """
    Check that the metadata is correct when NominalColumns are created from
    floats
    """
    arr = np.array([1.0, 2.0])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1.0, 1: 2.0}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_floats_and_nan():
    """
    Check that the metadata is correct when NominalColumns are created from
    floats
    """
    arr = np.array([1.0, 2.0, np.nan])
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1.0, 1: 2.0, -1: '<missing>'}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_dtype_object():
    """
    Check that the metadata is correct when NominalColumns are created from
    objects
    """
    arr = np.array([1, 2], dtype="object")
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2}, \
        'The metadata is formed correctly'


def test_chaid_vector_with_dtype_object_and_nans():
    """
    Check that the metadata is correct when NominalColumns are created from
    objects
    """
    arr = np.array([1, 2, np.nan], dtype="object")
    vector = CHAID.NominalColumn(arr)

    assert np.array_equal(vector.arr, np.array([0, 1, -1])), \
        'The indices are correctly substituted'
    assert vector.metadata == {0: 1, 1: 2, -1: '<missing>'}, \
        'The metadata is formed correctly'

def test_column_stores_weights():
    """
    Tests that the columns store the weights when they are passed
    """
    arr = np.array([1.0, 2.0, 3.0])
    wt = np.array([2.0, 1.0, 0.25])
    nominal = CHAID.NominalColumn(arr, weights=wt)
    ordinal = CHAID.OrdinalColumn(arr, weights=wt)
    continuous = CHAID.ContinuousColumn(arr, weights=wt)
    assert (nominal.weights == wt).all()
    assert (ordinal.weights == wt).all()
    assert (continuous.weights == wt).all()

def test_fix_metadata_if_passed_in():
    arr = np.array([1.0, 2.0, 3.0])
    nominal = CHAID.NominalColumn(arr, metadata={1.0: 'Cat', 2.0: 'Haz', 3.0: 'Cheezburger'})
    assert [nominal.metadata[x] for x in nominal.arr] == ['Cat', 'Haz', 'Cheezburger']

def test_all_combinations():
    arr = np.array([1.0, 2.0, 3.0, 4.0])
    nominal = CHAID.NominalColumn(arr)
    assert [ i for i in nominal.all_combinations()] == [[[0.0], [1.0, 2.0, 3.0]],
                                          [[0.0, 1.0], [2.0, 3.0]],
                                          [[1.0], [0.0, 2.0, 3.0]],
                                          [[0.0], [1.0], [2.0, 3.0]],
                                          [[0.0, 1.0, 2.0], [3.0]],
                                          [[1.0, 2.0], [0.0, 3.0]],
                                          [[0.0], [1.0, 2.0], [3.0]],
                                          [[0.0, 2.0], [1.0, 3.0]],
                                          [[2.0], [0.0, 1.0, 3.0]],
                                          [[0.0], [2.0], [1.0, 3.0]],
                                          [[0.0, 1.0], [2.0], [3.0]],
                                          [[1.0], [0.0, 2.0], [3.0]],
                                          [[1.0], [2.0], [0.0, 3.0]],
                                          [[0.0], [1.0], [2.0], [3.0]]]


class TestDeepCopy(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for copy tests"""
        # Use string so numpy array dtype is object and may store references
        arr = np.array(['5.0', '10.0'])
        self.orig = CHAID.NominalColumn(arr)
        self.copy = self.orig.deep_copy()

    def test_deep_copy_does_copy(self):
        """ Ensure a copy actually happens when deep_copy is called """
        assert id(self.orig) != id(self.copy), 'The vector objects must be different'
        assert list_ordered_equal(self.copy, self.orig), 'Vector contents must be the same'

    def test_changing_copy(self):
        """ Test that altering the copy doesn't alter the original """
        self.copy.arr[0] = 55.0
        assert not list_ordered_equal(self.copy, self.orig), 'Altering one vector should not affected the other'

    def test_metadata(self):
        """ Ensure metadata is copied correctly or deep_copy """
        assert self.copy.metadata == self.orig.metadata, 'Copied metadata should be equivalent'


class TestBugFixes(TestCase):
    """ Specific tests for bug fixes """
    def test_comparison_of_different_object_types(self):
        """
        Fix bug whereby floats were being passed into NominalColumn
        from `self.observed = NominalColumn(arr)` but as `dtype=object`
        resulting in `TypeError: unorderable types: int() > str()` in
        python 3.x only
        """
        input_list = [100, 'c', 13, 15, np.nan, np.nan]
        object_arr = np.array(input_list, dtype=object)
        vector = CHAID.NominalColumn(object_arr)

        assert [vector.metadata[x] for x in vector.arr] == ['<missing>' if x != x else x for x in input_list]


def test_negative_values_stay_distinct_categories():
    """ Substituted ids must not collide with values that are still to be substituted """
    col = CHAID.NominalColumn(np.array([-5, 0, 1, 1, 0, -5]))
    assert list(col.arr) == [0, 1, 2, 2, 1, 0]
    assert col.metadata == {0: -5, 1: 0, 2: 1}
