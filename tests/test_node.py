"""
Testing module for the class Node
"""

from setup_tests import CHAID
import numpy as np

def test_dependent_variable_properties_as_members_for_continous_node():
    """
    Tests that node prints the std and mean when contonuous column supplied
    """
    data = np.array([1.3, 23.0, 3.0, 3.0, 12.4])
    continuous_dp = CHAID.ContinuousColumn(data)
    node = CHAID.Node(dep_v=continuous_dp)
    assert node.members == {'mean': data.mean(), 's.t.d': data.std()}

def test_node_should_have_a_score():
    """
    Tests that node uses the split score and is called 'score'
    """
    data = np.array([1.3, 23.0, 3.0, 3.0, 12.4])
    continuous_dp = CHAID.ContinuousColumn(data)
    split = CHAID.Split("a", [], 2, 3, 4)
    node = CHAID.Node(dep_v=continuous_dp, split=split)
    assert node.score == 2
