"""
Testing module for the class ContinuousColumn
"""
from unittest import TestCase
import numpy as np
from numpy import nan
from setup_tests import list_ordered_equal, CHAID
import pytest

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

def test_nans_filled_with_zero():
    """
    Check that nans are filled with zero
    """
    arr = np.array([np.nan, 1., 2., 3.])
    assert (CHAID.ContinuousColumn(arr).arr == np.array([0., 1., 2., 3.])).all()

