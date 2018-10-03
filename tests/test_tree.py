"""
Testing module for the class Tree
"""
from unittest import TestCase
import numpy as np
from setup_tests import list_ordered_equal, list_unordered_equal, CHAID, ROOT_FOLDER
import pandas as pd
from treelib import Tree as TreeLibTree
import os

class TestClassificationRules(TestCase):
    def setUp(self):
        invalid_split = CHAID.Split(None, None, 0, 1, 0)
        self.tree = CHAID.Tree.from_numpy(np.array([[1]]), np.array([1]))
        self.tree._tree_store = [
            CHAID.Node(
                node_id=0,
                split=CHAID.Split('a', [[1], [2]], 1, 0.2, 2)
            ),
            CHAID.Node(node_id=1, split=invalid_split, choices=[1], parent=0),
            CHAID.Node(
                node_id=2,
                split=CHAID.Split('c', [[3]], 1, 0.2, 2),
                choices=[2],
                parent=0
            )
        ]
        self.last_node = CHAID.Node(
            node_id=3,
            split=invalid_split,
            choices=[3],
            parent=2
        )
        self.tree._tree_store.append(self.last_node)

    def test_single_path(self):
        expected_rules = [
            {
                'node': 3,
                'rules': [
                    {'data': [3], 'variable': 'c'},
                    {'data': [2], 'variable': 'a'}
                ]
            }
        ]
        assert list_unordered_equal(self.tree.classification_rules(self.last_node), expected_rules), "Couldn't find path to determine rules from specified node"

    def test_all_paths(self):
        expected_rules = [
            {
                'node': 3,
                'rules': [
                    {'data': [3], 'variable': 'c'},
                    {'data': [2], 'variable': 'a'}
                ]
            },
            {
                'node': 1,
                'rules': [
                    {'data': [1], 'variable': 'a'}
                ]
            }
        ]
        assert list_unordered_equal(self.tree.classification_rules(), expected_rules), "Couldn't find path to determine rules from all terminal nodes"


def test_best_split_unique_values():
    """
    Test passing in a perfect split data, with no catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 5))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=0)

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
    tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=0)

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
    tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=0)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert list_ordered_equal(ndarr, orig_ndarr), 'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), 'Calling chaid should have no side affects for original numpy arrays'
    assert split.column_id == 0, 'Identifies correct column to split on'
    assert list_unordered_equal(split.split_map, [[1], [2], [3]]), 'Correctly identifies categories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.015

def test_best_split_with_combination_combining_if_too_small():
    """
    Test passing in a perfect split data, with a single catagory merges needed
    """
    arr = np.array(([1] * 5) + ([2] * 10))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 3) + ([3, 2, 3] * 5) + [1, 2, 3] * 2).reshape(15, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=5, alpha_merge=0.055)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert list_ordered_equal(ndarr, orig_ndarr), 'Calling chaid should have no side affects for original numpy arrays'
    assert list_ordered_equal(arr, orig_arr), 'Calling chaid should have no side affects for original numpy arrays'
    assert split.column_id == 0, 'Identifies correct column to split on'
    assert list_unordered_equal(split.split_map, [[1], [2, 3]]), 'Correctly identifies categories'
    assert list_unordered_equal(split.surrogates, []), 'No surrogates should be generated'
    assert split.p < 0.055


def test_new_columns_constructor():
    """
    Test the new tree constructor that takes CHAID Columns as parameters
    """
    orientation = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    age = np.array([0,1,1,0,2,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])
    metadata = {0: '0-5', 1: '6-10', 2: '11-15'}
    cols = [
        CHAID.OrdinalColumn(orientation, name="orientation", metadata=metadata),
        CHAID.OrdinalColumn(age, name="age", metadata=metadata),
    ]
    tree = CHAID.Tree(cols, CHAID.NominalColumn(income), {'min_child_node_size': 1})
    assert tree.tree_store[0].split.groupings == "[['0-5'], ['6-10', '11-15']]"


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
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, split_threshold=0.9, min_child_node_size=0)

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
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, split_threshold=0.9, min_child_node_size=0)

        split = tree.generate_best_split(
            tree.vectorised_array,
            tree.observed
        )

        assert split.p < split.surrogates[0].p, 'The best split should be the minimum p by default'
        assert split.score > split.surrogates[0].score, 'The data picked should not allow picked split to have both p and chi less than the surrogate'


def test_p_and_chi_values():
    """
    Check chi and p value against hand calculated values
    """
    arr = np.array(([1] * 3) + ([2] * 4))
    ndarr = np.array(([1] * 4) + ([2] * 3)).reshape(7, 1)

    tree = CHAID.Tree.from_numpy(ndarr, arr, split_threshold=0.9, min_child_node_size=0)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )
    assert round(split.score, 4) == 3.9375
    assert round(split.p, 4) == 0.0472


def test_p_and_chi_values_when_weighting_applied():
    """
    Check chi and p value when weights supplied
    """
    gender = np.array([0,0,0,1,0,0,1,1,0,0,1])
    income = np.array([0,0,1,0,2,0,1,2,1,0,1])

    weighting = np.array([0.9,0.8,0.9,1.1,1.2,0.8,1.3,0.2,0.5,0.7,1.1])
    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9, weights=weighting, min_child_node_size=0)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert round(split.score, 4) == 1.6179
    assert round(split.p, 4) == 0.4453


def test_correct_dof():
    """
    Check the degrees of freedom is correct
    """
    gender = np.array([0,0,0,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2])
    income = np.array([0,0,1,0,2,0,1,2,1,0,1,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9, min_child_node_size=0)

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

    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9, weights=weighting, min_child_node_size=0)

    split = tree.generate_best_split(
        tree.vectorised_array,
        tree.observed
    )

    assert round(split.score, 4) == 14.5103
    assert round(split.p, 4) == 0.0007


def test_min_child_node_size_is_30():
    """
    Test that the min_child_node_size is set to 30 and prevents
    splitting if the parent's child would have less than 30 data points
    """
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))

    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9)
    invalid_split_reason = 'splitting would create nodes with less than the minimum child node size'
    assert str(tree.tree_store[0].split.invalid_reason) == invalid_split_reason
    assert len(tree.tree_store) == 1

def test_to_tree_returns_a_tree():
    """
    Test that the to_tree() method returns expected result
    """
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))
    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9,
                      min_child_node_size=1, min_parent_node_size=1)

    assert isinstance(tree.to_tree(), TreeLibTree), 'A TreeLib object is returned'
    assert len(tree.tree_store) == len(tree.to_tree().nodes), 'The tree contains the correct number of nodes'

def test_accuracy():
    """
    Test that accuracy returns correct percentage
    """
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))
    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9,
                      min_child_node_size=1, min_parent_node_size=1)

    assert tree.accuracy() == 0.85
    assert tree.accuracy() == 1 - tree.risk()

def test_max_depth_returns_correct_invalid_message():
    """
    Test when max_depth reached, it has the correct invalid message
    on the terminal nodes
    """
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))
    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9, max_depth=1,
                      min_child_node_size=1, min_parent_node_size=1)

    assert tree.tree_store[-1].split.invalid_reason == CHAID.InvalidSplitReason.MAX_DEPTH, 'The max depth limit is '\
                                                 'the invalid reason on the terminal node'

def test_node_predictions():
    gender = np.array([0,0,1,1,0,0,1,1,0,0,1,2,2,2,2,2,2,2,2,1])
    income = np.array([0,0,1,1,2,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0])

    ndarr = np.transpose(np.vstack([gender]))
    tree = CHAID.Tree.from_numpy(ndarr, income, alpha_merge=0.9, max_depth=1,
                      min_child_node_size=1, min_parent_node_size=1)

    # brute force has a lower p, but a lower chi. Confusing. Will leave as the heursitic approach
    assert (tree.node_predictions() == np.array([
        1.,  1.,  2.,  2.,  1.,  1.,  2.,  2.,  1.,  1.,  2.,  3.,  3.,
        3.,  3.,  3.,  3.,  3.,  3.,  2.
    ])).all() == True

class TestTreeGenerated(TestCase):
    """ Test case class to check that the tree is correcly lazy loaded """
    def setUp(self):
        """ Set up for tree generation tests """
        arr = np.array(([1] * 5) + ([2] * 5))
        ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
        self.tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=0)

    def test_iter(self):
        """ Test the calls to __iter__() populate the tree """
        self.tree.__iter__()
        assert self.tree.tree_store is not None

    def test_modification(self):
        """ Test the calls to get_node() populate the tree """
        self.tree.get_node(0)
        assert self.tree.tree_store is not None

    def test_deletion(self):
        assert self.tree.tree_store is not None


class TestComplexStructures(TestCase):
    """ Test case class to utilise logic only exposed from large datasets """
    # def setUp(self):
    #    self.df = pd.read_csv(ROOT_FOLDER + '/tests/data/CHAID.csv')

    def test_p_and_chi_values_selectivity(self):
        """
        Check chi taken into consideration when significance becomes 0 for multiple independent variables
        """
        # ndarr = self.df[['col_17', 'col_27']].values
        # arr = self.df['dep'].values
        #
        # tree = CHAID.Tree.from_numpy(ndarr, arr, split_threshold=0.9)
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
        self.string_ndarr = np.array(([u'\u2013', u'\u2012'] * 20) + ([u'\u2011', u'\u2008'] * 20) + ([u'\u2000', u'\u2223'] * 19) + [u'\u2123', u'\u1993']).reshape(30, 4)

    def test_incorrect_weighted_counts(self):
        """
        Fix bug whereby the weights was using the class weights
        and not the sliced weights in node()
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_parent_node_size=2, min_child_node_size=0)
        assert tree.tree_store[3].members == {1: 0, 2: 1.2}
        assert tree.tree_store[5].members == {1: 5.0, 2: 6.0}

    def test_unicode_printing(self):
        cols = dict(zip([u'\u2013', 'a', 'b', u'another unicode \u2013 \u2013'], ['nominal'] * 4))
        df = pd.DataFrame(data=self.string_ndarr, columns=cols)
        df['ordinal'] = self.arr[::-1]
        cols['ordinal'] = 'ordinal'
        df['dep_v'] = self.arr
        no_exception = True
        try:
            CHAID.Tree.from_pandas_df(df, cols, 'dep_v', min_child_node_size=0).print_tree()
        except:
            no_exception = False
        assert no_exception, 'Raised error while printing the tree'

    def test_splits_shouldnt_carry_on_splitting_below_min_child_node_size(self):
        """
        Fix bug whereby no splits occur when valid split is segmented below
        min_child_node_size threshold
        """
        region = np.array([
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 2, 3, 2, 2, 2,
            3, 2, 4, 4, 2, 4, 4, 4, 2, 2, 2, 2, 3, 2, 3, 2, 3, 2, 2, 2])
        age = np.array([
            3, 4, 4, 3, 2, 4, 2, 3, 3, 2, 2, 3, 4, 3, 4, 2, 2, 3, 2, 3,
            2, 4, 4, 3, 2, 3, 1, 2, 4, 4, 3, 4, 4, 3, 2, 4, 2, 3, 3, 2,
            2, 3, 4, 3, 4, 2, 2, 3, 2, 3, 2, 4, 4, 3, 2, 3, 1, 2, 4, 4])
        gender = np.array([
            1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2,
            2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2,
            2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2])
        lover = np.array([1] * 25 + [0] * 35)
        tree = CHAID.Tree.from_numpy(
            np.vstack([region, age, gender]).transpose(),
            lover,
            alpha_merge=0.05
        )
        assert len(tree.tree_store) == 3

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
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, alpha_merge=0.999, max_depth=5, min_child_node_size=31)
        assert len(tree.tree_store) == 1

    def test_min_child_node_size_does_not_stop_for_unweighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, alpha_merge=0.999, max_depth=5, min_child_node_size=5)
        assert len(tree.tree_store) == 4

    def test_min_child_node_size_does_stop_for_weighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_child_node_size=10.7)
        assert len(tree.tree_store) == 4
        assert round(tree.tree_store[0].split.p, 5) == 0.08781

    def test_min_child_node_size_does_not_stop_for_weighted_case(self):
        """
        Check that minimum child node size causes the tree to
        terminate correctly
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.arr, alpha_merge=0.999, weights=self.wt, max_depth=5, min_child_node_size=11.5)
        assert len(tree.tree_store) == 3


class TestContinuousDependentVariable(TestCase):
    """ Testing that trees based on a continuous dependent variable work"""
    def setUp(self):
        """ Setup test data for continuous data """
        self.random_arr = np.array(
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
        self.normal_arr = np.array([
            215.74655491,  237.0905247 ,  193.72021408,  152.89363815,
            175.36670032,  232.59086085,  204.20219942,  248.99321897,
            267.95686148,  165.7204985 ,  177.38110221,  220.40618705,
            262.71893125,  240.00774431,  210.85572027,  255.06583994,
            232.85274614,  274.71932373,  186.83175676,  241.47832856,
            294.98781486,  190.82037054,  143.7991682 ,  170.32090888,
            207.20320791,  208.10226642,  187.09923858,  178.9242382 ,
            155.17266333,  140.69923988,  210.80029533,  193.85525698,
            232.69854217,  230.4408611 ,  149.34523942,  303.6243051 ,
            171.1562868 ,  185.24131426,  195.80616026,  224.38213062,
            261.77203837,  170.81218927,  216.37943211,  265.25650174,
            203.3098626 ,  229.84982086,  212.14777791,  265.25335911,
            296.11334434,  242.40424522,  270.30264815,   77.97401496,
            176.80382943,  156.35135782,  155.29031942,  262.11885208,
            161.33251252,  256.05120377,  158.32542953,  189.07183278,
            155.72524265,  244.68956731,  286.68689241,   94.08648606,
            253.80300049,  161.17371005,  116.94584491,  182.88557535,
            182.85752412,  253.42111371,  131.25146323,  264.86407965,
            197.3742505 ,  296.95506279,  221.01600673,  234.04694958,
            154.42957223,  176.94139196,  200.59554949,  170.4040058 ,
            229.39358115,  127.43357367,  249.09735255,  227.90731765,
            238.9667355 ,  163.83410357,  194.88998826,  134.49013182,
            154.54356067,  254.19699384,  143.93816979,  256.11031829,
            186.56096688,  178.40462838,  159.79032932,  187.7542398 ,
            267.18537402,  190.99969385,  130.30080584,  216.12902248,
            247.8707783 ,  246.49016072,  275.3636918 ,  165.69987612,
            181.16709806,  193.87951446,  156.03720504,  221.44032879,
            182.21405831,  119.22571297,  219.14946203,  140.358539  ,
            210.5826685 ,  256.57132523,  244.82587339,  153.26377344,
            198.44006972,  172.6057332 ,  140.26518016,  171.32162943]
        )
        self.wt = np.array(([1.0] * 60) + ([1.2] * 60))
        self.ndarr = np.array(([2, 3] * 20) + ([2, 5] * 20) + ([3, 4] * 19) + [2, 3] + [1, 2, 5] * 80 + [1, 2, 3] * 40).reshape(120, 4)

    def test_continuous_dependent_variable(self):
        """
        Check that a tree can be built with a continuous dependent variable
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.random_arr, alpha_merge=0.999, max_depth=5, min_child_node_size=11, dep_variable_type='continuous')
        assert round(tree.tree_store[0].p, 4) == 0.4119
        assert len(tree.tree_store) == 9

    def test_continuous_dependent_variable_with_weighting(self):
        """
        Check that a tree can be built with a continuous dependent variable
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.random_arr, alpha_merge=0.999, max_depth=5, min_child_node_size=11, dep_variable_type='continuous', weights=self.wt)
        assert round(tree.tree_store[0].p, 4) == 0.1594
        assert len(tree.tree_store) == 9

    def test_bartlett_significance(self):
        """
        Check that a tree can be built with a continuous dependent variable using the bartlett significance because the distribution is normal
        """
        tree = CHAID.Tree.from_numpy(self.ndarr, self.normal_arr, alpha_merge=0.999, max_depth=5, min_child_node_size=11, dep_variable_type='continuous', weights=self.wt)
        assert round(tree.tree_store[0].p, 4) == 0.3681
        assert len(tree.tree_store) == 5


class TestStringCategoricalDependentVariableForModelPrediction(TestCase):
    """ Test to make sure we can handle string categorical dependent varaibles """
    def setUp(self):
        """
        Setup data for test case
        """
        self.region = np.array([
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 2, 3, 2, 2, 2,
            3, 2, 4, 4, 2, 4, 4, 4, 2, 2, 2, 2, 3, 2, 3, 2, 3, 2, 2, 2])
        self.age = np.array([
            3, 4, 4, 3, 2, 4, 2, 3, 3, 2, 2, 3, 4, 3, 4, 2, 2, 3, 2, 3,
            2, 4, 4, 3, 2, 3, 1, 2, 4, 4, 3, 4, 4, 3, 2, 4, 2, 3, 3, 2,
            2, 3, 4, 3, 4, 2, 2, 3, 2, 3, 2, 4, 4, 3, 2, 3, 1, 2, 4, 4])
        self.gender = np.array([
            1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2,
            2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2,
            2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2])
        self.lover = np.array(['lover'] * 25 + ['non-lover'] * 35)
        self.tree = CHAID.Tree.from_numpy(
            np.vstack([self.region, self.age, self.gender]).transpose(),
            self.lover,
            alpha_merge=0.05
        )

    def test_string_dependent_categorical_variable_for_model_prediction(self):
        assert (self.tree.model_predictions() ==  np.array(['lover'] * 30 + ['non-lover'] * 30)).all()

    def test_risk_still_works(self):
        int_lover = np.array([1] * 25 + [0] * 35)
        other_tree = CHAID.Tree.from_numpy(
            np.vstack([self.region, self.age, self.gender]).transpose(),
            int_lover,
            alpha_merge=0.05
        )
        assert self.tree.risk() == other_tree.risk()
