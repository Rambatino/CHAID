"""
Testing module for the class Split
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

