"""
Testing module for the class CHAID
"""
from unittest import TestCase
import numpy as np
from setup_tests import list_ordered_equal, list_unordered_equal, CHAID, ROOT_FOLDER, CHAIDNode
import pandas as pd

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
    assert list_unordered_equal(split.split_map, [[1], [2]]), 'Correctly identifies catagories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.015


def test_spliting_identical_values():
    """
    Test that passing in identical data cannot be split
    """
    arr = np.array(([1] * 5) + ([1] * 5))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.CHAID(ndarr, arr)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert list_ordered_equal(ndarr, orig_ndarr), \
        'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), \
        'Identifies correct column to split on'
    assert not split.valid(), \
        'Should not be able to split data with no skew'


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
    assert list_unordered_equal(split.split_map, [[1], [2, 3]]), 'Correctly identifies catagories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.015

class TestSurrogate(TestCase):
    """ Test case class to test surrogate detection """
    def setUp(self):
        """ Setup test data that contains a surrogate """
        self.arr = np.array(([1] * 20) + ([2] * 20) + ([3] * 20))
        self.ndarr = np.array(([2, 3] * 20) + ([2, 4] * 20) + ([3, 4] * 19)+ [2, 3]).reshape(60, 2)

    def test_surrgate_detection(self):
        """
        Test passing in data, in which a surrogate split exists
        """
        tree = CHAID.CHAID(self.ndarr, self.arr, split_threshold=0.9)

        split = tree.generate_best_split(
            tree.vectorised_array,
            tree.observed
        )

        assert split.column_id == 1, 'The best split should be on column 1'
        assert len(split.surrogates) == 1, 'There should be a single surrogate in given data'
        assert split.surrogates[0].column_id == 0, 'The surrogate should be on column 0'

    def test_surrogate_default_min_p(self):
        """
        Test that chaid selects min p split
        """
        tree = CHAID.CHAID(self.ndarr, self.arr, split_threshold=0.9)

        split = tree.generate_best_split(
            tree.vectorised_array,
            tree.observed
        )

        assert split.p < split.surrogates[0].p, 'The best split should be the minimum p by default'
        assert split.chi > split.surrogates[0].chi, 'The data picked should not allow picked split to have both p and chi less than the surrogate'

def test_p_and_chi_values():
    """
    Check chi and p value against hand calculated values
    """
    arr = np.array(([1] * 3) + ([2] * 4))
    ndarr = np.array(([1] * 4) + ([2] * 3)).reshape(7, 1)

    tree = CHAID.CHAID(ndarr, arr, split_threshold=0.9)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert round(split.chi, 4) == 3.9375
    assert round(split.p, 4) == 0.0472


def test_rules_when_single_numerical_independent_variable():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1], [2], [1], [3], [1], [2], [1], [2], [3], [4],
        [1], [2], [3], [4], [1], [2], [3], [1], [2], [3]
    ])

    tree = CHAID.CHAID(ndarr=independent_set, arr=np.array([]))

    indices_1 = np.array([0,  2,  4,  6, 10, 14, 17, 1,  5,  7, 11, 15, 18])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)

    indices_2   = np.array([ 3,  8, 12, 16, 19, 9, 13])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    tree.tree_store = [terminal_node_1, terminal_node_2]

    assert (tree.rules() == pd.Series([2, 2, 3, 3], index=[1, 2, 3, 4])).all()
    assert tree.rules().name == 'node'


def test_rules_when_single_object_independent_variable():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        ['a'], ['b'], ['c'], ['a'], ['b'], ['c'], ['d'], ['e'], ['f']
    ])

    tree = CHAID.CHAID(ndarr=independent_set, arr=np.array([]))
    indices_1 = np.array([0, 3])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)

    indices_2   = np.array([1, 2, 4, 5, 6])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    indices_3   = np.array([7, 8])
    terminal_node_3 = CHAID.CHAIDNode(node_id=4, is_terminal=True, indices=indices_3)

    tree.tree_store = [terminal_node_1, terminal_node_2, terminal_node_3]

    expected = pd.Series([2, 3, 3, 3, 4, 4], index=['a', 'b', 'c', 'd', 'e', 'f'])

    assert (tree.rules() == expected).all()
    assert tree.rules().name == 'node'


def test_rules_when_multiple_numerical_independent_variables():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1, 0], [2, 1], [1, 0], [3, 1], [1, 0], [2, 1], [1, 0], [2, 1], [3, 1], [4, 0]
    ])

    tree = CHAID.CHAID(ndarr=independent_set, arr=np.array([]))
    indices_1 = np.array([0, 2, 4, 6, 9])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)
    indices_2 = np.array([1, 3, 5, 7, 8])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    tree.tree_store = [terminal_node_1, terminal_node_2]

    index = pd.MultiIndex.from_arrays(np.array([[1, 4, 3, 2], [0, 0, 1, 1]]))
    expected = pd.Series([2, 2, 3, 3], index=index)

    assert (tree.rules() == expected).all()
    assert tree.rules().name == 'node'


def test_rules_when_multiple_mixed_object_independent_variables():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1, 0, 'a'], [2, 1, 'b'], [1, 0, 'a'], [3, 1, 'c'], [1, 0, 'a'],
        [2, 1, 'b'], [1, 0, 'a'], [2, 1, 'b'], [3, 1, 'c'], [4, 0, 'a']
    ])

    tree = CHAID.CHAID(ndarr=independent_set, arr=np.array([]))
    indices_1 = np.array([0, 2, 4, 6, 9])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)


    indices_2 = np.array([1, 5, 7])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)


    indices_3 = np.array([3, 8])
    terminal_node_3 = CHAID.CHAIDNode(node_id=4, is_terminal=True, indices=indices_3)

    tree.tree_store = [terminal_node_1, terminal_node_2, terminal_node_3]

    index = pd.MultiIndex.from_arrays(np.array([[1, 4, 2, 3], [0, 0, 1, 1], ['a', 'a', 'b', 'c']]))
    expected = pd.Series([2, 2, 3, 4], index=index)

    assert (tree.rules() == expected).all()
    assert tree.rules().name == 'node'


class TestTreeGenerated(TestCase):
    """ Test case class to check that the tree is correcly lazy loaded """
    def setUp(self):
        """ Set up for tree generation tests """
        arr = np.array(([1] * 5) + ([2] * 5))
        ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
        self.tree = CHAID.CHAID(ndarr, arr)

    def test_iter(self):
        """ Test the calls to __iter__() populate the tree """
        self.tree.__iter__()
        assert self.tree.tree_store is not None

    def test_modification(self):
        """ Test the calls to get_node() populate the tree """
        self.tree.get_node(0)
        assert self.tree.tree_store is not None

    def test_deletion(self):
        """ Test the calls to build_tree() populate the tree """
        self.tree.build_tree()
        assert self.tree.tree_store is not None

class TestComplexStructures(TestCase):
    """ Test case class to utilise logic only exposed from large datasets """
    # def setUp(self):
        # self.df = pd.read_csv(ROOT_FOLDER + '/tests/data/CHAID.csv')

    def test_p_and_chi_values_selectivity(self):
        """
        Check chi taken into consideration when significance becomes 0 for multiple independent variables
        """
        # ndarr = self.df[['col_17', 'col_27']].values
        # arr = self.df['dep'].values
        #
        # tree = CHAID.CHAID(ndarr, arr, split_threshold=0.9)
        #
        # split = tree.generate_best_split(
        #     tree.vectorised_array,
        #     tree.observed
        # )
        assert True
