"""
Testing module for the class CHAID
"""
from setup_tests import list_ordered_equal, list_unordered_equal, CHAID
from unittest import TestCase
import numpy as np

def test_best_split_unique_values():
    """
    Test passing in a perfect split data, with no catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 5))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.CHAID(ndarr, arr)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert list_ordered_equal(ndarr, orig_ndarr), 'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), 'Calling chaid should have no side affects for original numpy arrays'
    assert split.column_id == 0, 'Identifies correct column to split on'
    assert list_unordered_equal(split.splits, [[1.0], [2.0]]), 'Correctly identifies catagories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.015

def test_best_split_with_combination():
    """
    Test passing in a perfect split data, with a single catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 10))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5) + ([3, 2, 3] * 5)).reshape(15, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.CHAID(ndarr, arr)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert list_ordered_equal(ndarr, orig_ndarr), 'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), 'Calling chaid should have no side affects for original numpy arrays'
    assert split.column_id == 0, 'Identifies correct column to split on'
    assert list_unordered_equal(split.splits, [[1.0], [2.0, 3.0]]), 'Correctly identifies catagories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.015

def test_surrogate_correctly_identified():
    """
    Test passing in data, in which a surrogate split exists
    """
    arr = np.array(([1] * 20) + ([2] * 20))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 20) + ([2, 3, 3] * 19) + [2, 2, 3]).reshape(40, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.CHAID(ndarr, arr, split_threshold=0.9)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert len(split.surrogates) == 1
    assert split.surrogates[0].column_id == 1

def test_p_and_chi_values():
    """
    Check chi and p value against hand calculated values
    """
    arr = np.array(([1] * 3) + ([2] * 4))
    orig_arr = arr.copy()
    ndarr = np.array(([1] * 4) + ([2] * 3)).reshape(7, 1)
    orig_ndarr = ndarr.copy()

    tree = CHAID.CHAID(ndarr, arr, split_threshold=0.9)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert round(split.chi, 4) == 1.4705 #chi2_contingency([[3, 1], [0, 3]])
    assert round(split.p, 4) == 0.2253


class TestTreeGenerated(TestCase):
    """ Test case class to check that the tree is correcly lazy loaded """
    def setUp(self):
        """ Set up for tree generation tests """
        arr = np.array(([1] * 5) + ([2] * 5))
        orig_arr = np.array(([1] * 5) + ([2] * 5))
        ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
        orig_ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
        self.tree = CHAID.CHAID(ndarr, arr)

    def test_iter(self):
        """ Test the calls to __iter__() populate the tree """
        self.tree.__iter__()
        assert(self.tree.tree_store is not None)

    def test_modification(self):
        """ Test the calls to get_node() populate the tree """
        self.tree.get_node(0)
        assert(self.tree.tree_store is not None)

    def test_deletion(self):
        """ Test the calls to build_tree() populate the tree """
        self.tree.build_tree()
        assert(self.tree.tree_store is not None)
