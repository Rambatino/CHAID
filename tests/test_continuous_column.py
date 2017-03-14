"""
Testing module for the class Continuous
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal, CHAID
import pytest

NAN = float('nan')


def test_chaid_vector_converts_strings():
    """
    Check that error raised when string column supplied
    """
    with pytest.raises(ValueError) as excinfo:
        vector = CHAID.ContinuousColumn(np.array(['2', '4']))
        assert excinfo.value.message == 'Must only pass numerical values to create continuous column'


def test_chaid_vector_with_dtype_object():
    """
    Check that error raised when object column supplied
    """
    with pytest.raises(ValueError) as excinfo:
        vector = CHAID.ContinuousColumn(np.array(['2', '4'], dtype="object"))
        assert excinfo.value.message == 'Must only pass numerical values to create continuous column'
