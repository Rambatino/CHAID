"""
Testing module for the class CHAIDTree
"""
import collections
from unittest import TestCase
import numpy as np
import CHAID


class TestVectorGenerated(TestCase):
    def test_chaid_vector_converts_strings_with_correct_metadata(self):
        """ Checking that the metadata is correct when CHAIDVectors are created """
        arr = np.array(['1', '2'])
        vector = CHAID.CHAIDVector(arr)

        assert np.array_equal(vector.arr, np.array([0.0, 1.0])), 'The indices are correctly substituted'
        assert vector._metadata == {0.0: '1', 1.0: '2', -1.0: '<missing>'}, 'The metadata is formed correctly'
