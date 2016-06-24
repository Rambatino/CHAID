"""
Testing module for the class CHAIDTree
"""
import numpy as np
import collections
import CHAID

def list_unordered_equal(a, b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        a = sorted(a)
        b = sorted(b)
        return all(list_unordered_equal(i_a, i_b) for i_a, i_b in zip(a, b))
    else:
        return a == b

def list_ordered_equal(a, b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        return all(list_ordered_equal(i_a, i_b) for i_a, i_b in zip(a, b))
    else:
        return a == b

def test_best_split():
    """
    Test passing in a perfect split data, with no catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 5))
    orig_arr = np.array(([1] * 5) + ([2] * 5))
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
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

