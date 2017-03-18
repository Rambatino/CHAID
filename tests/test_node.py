"""
Testing module for the class Split
"""

from setup_tests import CHAID
import numpy as np

def test_dependent_variable_properties_as_members_for_continous_node():
    continuous_dp = CHAID.ContinuousColumn(np.array([1.3, 23.0, 3.0, 3.0, 12.4]))
    node = CHAID.Node(dep_v=continuous_dp)
    assert node.members.keys() == ['s.t.d', 'mean']
    assert [round(val, 4) for val in node.members.values()] == [8.2194, 8.54]

