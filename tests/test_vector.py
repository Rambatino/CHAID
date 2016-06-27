"""
Testing module for the class CHAIDVector
"""
from setup_tests import list_ordered_equal, CHAID
from unittest import TestCase
import numpy as np

def test_chaid_vector_converts_strings_with_correct_metadata():
    """ Checking that the metadata is correct when CHAIDVectors are created from strings """
    arr = np.array(['1', '2'])
    vector = CHAID.CHAIDVector(arr)

    assert np.array_equal(vector.arr, np.array([0.0, 1.0])), 'The indices are correctly substituted'
    assert vector.metadata == {0.0: '1', 1.0: '2', -1.0: '<missing>'}, 'The metadata is formed correctly'

def test_chaid_vector_does_not_convert_ints():
    """ Checking that the metadata is correct when CHAIDVectors are created from ints """
    arr = np.array([1, 2])
    vector = CHAID.CHAIDVector(arr)

    assert np.array_equal(vector.arr, np.array([1, 2])), 'The indices are correctly substituted'
    assert vector.metadata == {-1.0: '<missing>'}, 'The metadata is formed correctly'

def test_chaid_vector_does_not_convert_floats():
    """ Checking that the metadata is correct when CHAIDVectors are created from floats """
    arr = np.array([1.0, 2.0])
    vector = CHAID.CHAIDVector(arr)

    assert np.array_equal(vector.arr, np.array([1.0, 2.0])), 'The indices are correctly substituted'
    assert vector.metadata == {-1.0: '<missing>'}, 'The metadata is formed correctly'

def test_chaid_vector_converts_ints_when_dtype_is_object():
    """ Checking that the metadata is correct when CHAIDVectors are created from objects """
    arr = np.array([1, 2], dtype="object")
    vector = CHAID.CHAIDVector(arr)

    assert np.array_equal(vector.arr, np.array([0.0, 1.0])), 'The indices are correctly substituted'
    assert vector.metadata == {0.0: 1, 1.0: 2, -1.0: '<missing>'}, 'The metadata is formed correctly'

class TestDeepCopy(TestCase):
    """ Test fixture class for deep copy method """
    def setUp(self):
        """ Setup for copy tests"""
        # Use string so numpy array dtype is object and may store references
        arr = np.array(['5.0', '10.0'])
        self.orig = CHAID.CHAIDVector(arr)
        self.copy = self.orig.deep_copy()

    def test_deep_copy_does_copy(self):
        """ Ensure a copy actually happens when deep_copy is called"""
        assert id(self.orig) != id(self.copy), 'The vector objects must be different'
        assert list_ordered_equal(self.copy, self.orig), 'Vector contents must be the same'

    def test_alteration_doesnt_affect_original(self):
        """ Test that altering the copy doesn't alter the original """
        self.copy.arr[0] = 55.0
        assert not list_ordered_equal(self.copy, self.orig), 'Altering one vector should not affected the other'

    def test_metadata(self):
        """ Ensure metadata is copied correctly or deep_copy """
        assert self.copy.metadata == self.orig.metadata, 'Copied metadata should be equivilent'
