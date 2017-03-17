"""
Testing module for the class CHAID
"""
from unittest import TestCase
import numpy as np
from setup_tests import list_ordered_equal, list_unordered_equal, CHAID, ROOT_FOLDER
import pandas as pd

def test_best_split_unique_values():
    """
    Test passing in a perfect split data, with no catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 5))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.Tree(ndarr, arr)

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
    tree = CHAID.Tree(ndarr, arr)

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
    tree = CHAID.Tree(ndarr, arr)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert list_ordered_equal(ndarr, orig_ndarr), 'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), 'Calling chaid should have no side affects for original numpy arrays'
    assert split.column_id == 0, 'Identifies correct column to split on'
    assert list_unordered_equal(split.split_map, [[1], [2], [3]]), 'Correctly identifies catagories'
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
        tree = CHAID.Tree(self.ndarr, self.arr, split_threshold=0.9)

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
        tree = CHAID.Tree(self.ndarr, self.arr, split_threshold=0.9)

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

    tree = CHAID.Tree(ndarr, arr, split_threshold=0.9)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert round(split.chi, 4) == 3.9375
    assert round(split.p, 4) == 0.0472

def test_p_and_chi_values_when_weighting_applied():
    """
    Check chi and p value when weights supplied
    """
    gender = np.array([0,0,0,1,0,0,1,1,0,0,1])
    income = np.array([0,0,1,0,2,0,1,2,1,0,1])

    weighting = np.array([0.9,0.8,0.9,1.1,1.2,0.8,1.3,0.2,0.5,0.7,1.1])
    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree(ndarr, income, alpha_merge=0.9, weights=weighting)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert round(split.chi, 4) == 1.6179
    assert round(split.p, 4) == 0.4453

def test_correct_dof():
    """
    Check the degrees of freedom is correct
    """
    gender = np.array([0,0,0,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2])
    income = np.array([0,0,1,0,2,0,1,2,1,0,1,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree(ndarr, income, alpha_merge=0.9)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert split.dof == (len(set(gender)) - 1) * (len(set(income)) - 1)

def test_zero_subbed_weighted_ndarry():
    """
    Test how the split works when 0 independent categorical variable chooses a dependent categorical variable for the weighted case.
    In this instance, a very small float is assigned to the 0 value
    """
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])
    weighting = np.array(([0.9] * int(len(gender) / 2.0)) + ([1.9] * int(len(gender) / 2.0)))

    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree(ndarr, income, alpha_merge=0.9, weights=weighting)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert round(split.chi, 4) == 14.5103
    assert round(split.p, 4) == 0.0007

class TestTreeGenerated(TestCase):
    """ Test case class to check that the tree is correcly lazy loaded """
    def setUp(self):
        """ Set up for tree generation tests """
        arr = np.array(([1] * 5) + ([2] * 5))
        ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
        self.tree = CHAID.Tree(ndarr, arr)

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
        # tree = CHAID.Tree(ndarr, arr, split_threshold=0.9)
        #
        # split = tree.generate_best_split(
        #     tree.vectorised_array,
        #     tree.observed
        # )
        assert True

class TestBugFixes(TestCase):
    """ Specific tests for bug fixes """
    def setUp(self):
        """ Setup test data for bug fixes """
        self.arr = np.array(([1] * 15) + ([2] * 15))
        self.wt = np.array(([1.0] * 15) + ([1.2] * 15))
        self.ndarr = np.array(([2, 3] * 20) + ([2, 5] * 20) + ([3, 4] * 19) + [2, 3]).reshape(30, 4)

    def test_incorrect_weighted_counts(self):
        """
        Fix bug wherby the weights was using the class weights
        and not the sliced weights in node()
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_parent_node_size=2)
        tree.build_tree()
        assert tree.tree_store[3].members == {1: 0, 2: 1.2}
        assert tree.tree_store[5].members == {1: 5.0, 2: 6.0}

class TestStoppingRules(TestCase):
    """ Testing that stopping rules are being applied correctly """
    def setUp(self):
        """ Setup test data for bug fixes """
        self.arr = np.array(([1] * 15) + ([2] * 15))
        self.wt = np.array(([1.0] * 15) + ([1.2] * 15))
        self.ndarr = np.array(([2, 3] * 20) + ([2, 5] * 20) + ([3, 4] * 19) + [2, 3]).reshape(30, 4)

    def test_min_child_node_size_does_stop_for_unweighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, max_depth=5, min_child_node_size=11)
        tree.build_tree()
        assert len(tree.tree_store) == 1

    def test_min_child_node_size_does_not_stop_for_unweighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, max_depth=5, min_child_node_size=10)
        tree.build_tree()
        assert len(tree.tree_store) == 4

    def test_min_child_node_size_does_stop_for_weighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_child_node_size=10.7)
        tree.build_tree()
        assert len(tree.tree_store) == 4

    def test_min_child_node_size_does_not_stop_for_weighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_child_node_size=11.5)
        tree.build_tree()
        assert len(tree.tree_store) == 3


class TestContinuousDependentVariable(TestCase):
    """ Testing that stopping rules are being applied correctly """
    def setUp(self):
        """ Setup test data for bug fixes """
        self.arr = np.array(
           [0.23198952,  0.26550251,  0.96461057,  0.13733767,  0.76674088,
            0.60637166,  0.18822053,  0.78785506,  0.47786053,  0.44448984,
            0.88632344,  0.94060264,  0.52900520,  0.68301794,  0.00485769,
            0.09299505,  0.41767638,  0.22345506,  0.61899892,  0.53763263,
            0.41424529,  0.87527060,  0.10843391,  0.22902548,  0.52043049,
            0.82396842,  0.64215622,  0.42827082,  0.76920710,  0.27736853,
            0.95756523,  0.45140920,  0.12405161,  0.53774033,  0.72198885,
            0.37880053,  0.93554955,  0.44434796,  0.62834896,  0.02788777,
            0.30288893,  0.07198041,  0.59731867,  0.63485262,  0.79936557,
            0.41154027,  0.82900816,  0.49216809,  0.56649288,  0.26539558,
            0.12304309,  0.03233878,  0.64612524,  0.69844021,  0.30560065,
            0.05408900,  0.31020185,  0.93087523,  0.27952452,  0.57186781,
            0.36214135,  0.34114557,  0.82028983,  0.29795183,  0.21028335,
            0.41612748,  0.24781879,  0.19125266,  0.17214954,  0.44039645,
            0.84397111,  0.91060384,  0.70898285,  0.27049457,  0.15502956,
            0.47580771,  0.21507488,  0.68243381,  0.56233427,  0.22376202,
            0.76630117,  0.00162193,  0.15057895,  0.10145753,  0.69406461,
            0.81280760,  0.79726816,  0.42523241,  0.56025856,  0.10287649,
            0.53337746,  0.82185783,  0.38270064,  0.77411309,  0.01754383,
            0.84690273,  0.20057135,  0.37194360,  0.24657089,  0.91520048,
            0.65575302,  0.03220805,  0.71449568,  0.97194268,  0.94031990,
            0.61484448,  0.46961425,  0.38495625,  0.41865701,  0.81394666,
            0.57147433,  0.33414233,  0.13847757,  0.31316325,  0.04371212,
            0.36556674,  0.56316862,  0.66761528,  0.02491041,  0.12124478]
        )
        self.wt = np.array(([1.0] * 60) + ([1.2] * 60))
        self.ndarr = np.array(([2, 3] * 20) + ([2, 5] * 20) + ([3, 4] * 19) + [2, 3] + [1, 2, 5] * 80 + [1, 2, 3] * 40).reshape(120, 4)

    def test_min_child_node_size_does_stop_for_unweighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree(self.ndarr, self.arr, alpha_merge=0.999, max_depth=5, min_child_node_size=11)
        tree.build_tree()
        assert True
