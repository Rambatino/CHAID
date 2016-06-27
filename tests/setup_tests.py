import collections
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../CHAID')
import CHAID

def list_unordered_equal(a, b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        a = sorted(a)
        b = sorted(b)
        return all(list_unordered_equal(i_a, i_b) for i_a, i_b in zip(a, b))
    else:
        return a == b


def list_ordered_equal(a, b):
    """ Compares the unordered contents of two nd lists"""
    if isinstance(a, collections.Iterable) and isinstance(b, collections.Iterable):
        return all(list_ordered_equal(i_a, i_b) for i_a, i_b in zip(a, b))
    else:
        return a == b
