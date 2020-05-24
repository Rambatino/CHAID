"""
Testing module for the class Graph
"""
import numpy as np
from setup_tests import CHAID, ROOT_FOLDER
import os

def test_graph_is_created_properly():
    """
    Test that the graph is created correctly
    """
    arr = np.array(([1] * 5) + ([2] * 5))
    orig_arr = arr.copy()
    ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
    orig_ndarr = ndarr.copy()
    tree = CHAID.Tree.from_numpy(ndarr, arr, min_child_node_size=0)

    expected_path = os.path.join(ROOT_FOLDER, "tests", "expected_graph", "test")
    output_path = os.path.join(ROOT_FOLDER, "tests", "graph", "test")

    tree.render(path=output_path, view=False)

    # assert the pngs match
    with open(output_path + ".png", 'rb') as f:
          contents = f.read()
          with open(expected_path + ".png", 'rb') as g:
              expected_contents = g.read()
              assert contents == expected_contents

    # assert that a digraph is created
    assert os.path.exists(output_path)
