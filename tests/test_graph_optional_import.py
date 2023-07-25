"""
Testing module for the class Graph
"""
import numpy as np
import pytest
import builtins, sys
from importlib import reload
from unittest.mock import patch
import os


class PackageDiscarder:
    def __init__(self):
        self.pkgnames = []
    def find_spec(self, fullname, path, target=None):
        if fullname in self.pkgnames:
            raise ImportError()


@pytest.fixture
def no_graph_packages():
    modules_to_remove = []
    for name in sys.modules:
        if name.startswith('plotly') or name.startswith('graphviz') or name.startswith('CHAID') or name.startswith('setup_tests') or name in ['colorlover', 'graphviz', 'Digraph']:
            modules_to_remove.append(name)
    _ = [sys.modules.pop(x) for x in modules_to_remove]

    d = PackageDiscarder()
    d.pkgnames.extend([
        'plotly.graph_objs',
        'plotly.io',
        'colorlover',
        'graphviz',
        'Digraph',
    ])
    sys.meta_path.insert(0, d)
    yield
    sys.meta_path.remove(d)


def test_graph_warns_without_optional_imports(no_graph_packages):
    """
    Test that the graph produces an error without the optional imports (mocked)
    """
    with pytest.warns(UserWarning, match='Imports of optional packages needed to generate graphs failed. Please install with the "graph" option.'):
        from setup_tests import CHAID
