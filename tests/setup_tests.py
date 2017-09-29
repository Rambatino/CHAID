"""
This module provides helper functions for the rest of the testing module
"""

from collections import Iterable
import os
import sys
from math import isnan

ROOT_FOLDER = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../')

sys.path = [ROOT_FOLDER] + sys.path

import CHAID

def islist(a):
    return isinstance(a, Iterable) and not isinstance(a, str)


def str_ndlist(a):
    return [str_ndlist(i) for i in a]  if islist(a) else str(a)


def list_unordered_equal(list_a, list_b):
    """ Compares the unordered contents of two nd lists"""
    if islist(list_a) and islist(list_b):
        list_a = [str_ndlist(item_a) for item_a in list_a]
        list_b = [str_ndlist(item_b) for item_b in list_b]
        list_a.sort()
        list_b.sort()
        return len(list_a) == len(list_b) and all(list_unordered_equal(*item) for item in zip(list_a, list_b))
    else:
        return list_a == list_b or (isinstance(float, str) and isnan(list_a) and isnan(list_b))


def list_ordered_equal(list_a, list_b):
    """ Compares the unordered contents of two nd lists"""
    if islist(list_a) and islist(list_b):
        list_a = [item_a for item_a in list_a]
        list_b = [item_b for item_b in list_b]
        return len(list_a) == len(list_b) and all(list_ordered_equal(*item) for item in zip(list_a, list_b))
    else:
        return list_a == list_b or (isnan(list_a) and isnan(list_b))
