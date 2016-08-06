"""
This module provides helper functions for the rest of the testing module
"""

from collections import Iterable
import os
import sys

ROOT_FOLDER = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path.append(ROOT_FOLDER)

import CHAID
import CHAID.chaid_vector as CHAIDVector
import CHAID.chaid_node as CHAIDNode
import CHAID.chaid_split as CHAIDSplit
import CHAID.mapping_dict as MappingDict

def list_unordered_equal(list_a, list_b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(list_a, Iterable) and isinstance(list_b, Iterable):
        list_a = sorted(list_a)
        list_b = sorted(list_b)
        return all(list_unordered_equal(*item) for item in zip(list_a, list_b))
    else:
        return list_a == list_b


def list_ordered_equal(list_a, list_b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(list_a, Iterable) and isinstance(list_b, Iterable):
        return all(list_ordered_equal(*item) for item in zip(list_a, list_b))
    else:
        return list_a == list_b
