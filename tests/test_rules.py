"""
Testing module for the class CHAIDVector
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal, CHAID, CHAIDRules



def test_rules_when_single_numerical_independent_variable():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1], [2], [1], [3], [1], [2], [1], [2], [3], [4],
        [1], [2], [3], [4], [1], [2], [3], [1], [2], [3]
    ])

    dependent_set = np.array([
        1, 2, 2, 1, 2, 1, 2, 1, 2, 1,
        2, 2, 1, 1, 2, 1, 2, 1, 1, 2
    ])

    tree = CHAID.CHAID(ndarr=independent_set, arr=dependent_set)

    indices_1 = np.array([0,  2,  4,  6, 10, 14, 17, 1,  5,  7, 11, 15, 18])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)

    indices_2   = np.array([ 3,  8, 12, 16, 19, 9, 13])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    tree.tree_store = [terminal_node_1, terminal_node_2]

    assert (CHAIDRules(tree).rules() == pd.Series([2, 2, 3, 3], index=[1, 2, 3, 4])).all()
    assert CHAIDRules(tree).rules().name == 'node'


def test_rules_when_single_object_independent_variable():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        ['a'], ['b'], ['c'], ['a'], ['b'], ['c'], ['d'], ['e'], ['f']
    ])

    dependent_set = np.array([1, 2, 2, 1, 2, 1, 2, 1, 2])


    tree = CHAID.CHAID(ndarr=independent_set, arr=dependent_set)
    indices_1 = np.array([0, 3])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)

    indices_2   = np.array([1, 2, 4, 5, 6])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    indices_3   = np.array([7, 8])
    terminal_node_3 = CHAID.CHAIDNode(node_id=4, is_terminal=True, indices=indices_3)

    tree.tree_store = [terminal_node_1, terminal_node_2, terminal_node_3]

    expected = pd.Series([2, 3, 3, 3, 4, 4], index=['a', 'b', 'c', 'd', 'e', 'f'])

    assert (CHAIDRules(tree).rules() == expected).all()
    assert CHAIDRules(tree).rules().name == 'node'


def test_rules_when_multiple_numerical_independent_variables():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1, 0], [2, 1], [1, 0], [3, 1], [1, 0], [2, 1], [1, 0], [2, 1], [3, 1], [4, 0]
    ])

    dependent_set = np.array([1, 2, 2, 1, 2, 1, 2, 1, 2, 1])

    tree = CHAID.CHAID(ndarr=independent_set, arr=dependent_set)
    indices_1 = np.array([0, 2, 4, 6, 9])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)
    indices_2 = np.array([1, 3, 5, 7, 8])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)

    tree.tree_store = [terminal_node_1, terminal_node_2]

    index = pd.MultiIndex.from_arrays(np.array([[1, 4, 3, 2], [0, 0, 1, 1]]))
    expected = pd.Series([2, 2, 3, 3], index=index)

    assert (CHAIDRules(tree).rules() == expected).all()
    assert CHAIDRules(tree).rules().name == 'node'


def test_rules_when_multiple_mixed_object_independent_variables():
    """
    Check whether it correctly determines the unique independent
    variables for each node
    """

    independent_set = np.array([
        [1, 0, 'a'], [2, 1, 'b'], [1, 0, 'a'], [3, 1, 'c'], [1, 0, 'a'],
        [2, 1, 'b'], [1, 0, 'a'], [2, 1, 'b'], [3, 1, 'c'], [4, 0, 'a']
    ])

    dependent_set = np.array([1, 2, 2, 1, 2, 1, 2, 1, 2, 1])

    tree = CHAID.CHAID(ndarr=independent_set, arr=dependent_set)
    indices_1 = np.array([0, 2, 4, 6, 9])
    terminal_node_1 = CHAID.CHAIDNode(node_id=2, is_terminal=True, indices=indices_1)


    indices_2 = np.array([1, 5, 7])
    terminal_node_2 = CHAID.CHAIDNode(node_id=3, is_terminal=True, indices=indices_2)


    indices_3 = np.array([3, 8])
    terminal_node_3 = CHAID.CHAIDNode(node_id=4, is_terminal=True, indices=indices_3)

    tree.tree_store = [terminal_node_1, terminal_node_2, terminal_node_3]

    index = pd.MultiIndex.from_arrays(np.array([[1, 4, 2, 3], [0, 0, 1, 1], ['a', 'a', 'b', 'c']]))
    expected = pd.Series([2, 2, 3, 4], index=index)

    assert (CHAIDRules(tree).rules() == expected).all()
    assert CHAIDRules(tree).rules().name == 'node'
