import numpy as np
import math
from itertools import combinations
from .mapping_dict import MappingDict

class Column(object):
    """
    A numpy array with metadata

    Parameters
    ----------
    arr : iterable object
        The numpy array
    metadata : dict
        The substitutions of the vector
    missing_id : string
        An identifier for the missing value to be associated
    substitute : bool
        Whether the objects in the given array need to be substitued for
        integers
    """
    def __init__(self, arr=None, metadata=None,
                 missing_id='<missing>', substitute=True):
        self._metadata = dict(metadata or {})
        self._arr = np.array(arr)
        self._missing_id = missing_id
        self._groupings = MappingDict()

    def __iter__(self):
        return iter(self._arr)

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def possible_groupings(self):
        raise NotImplementedError

    def combine(self, x, y):
        raise NotImplementedError

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        raise NotImplementedError

    @property
    def arr(self):
        """
        Provides access to the internal numpy array
        """
        return self._arr

    @arr.setter
    def arr(self, value):
        """
        Allows writing to the internal numpy array
        """
        self._arr = value

    @property
    def metadata(self):
        """
        Provides access to the internal metadata e.g. when a string has been
        replaced with a float, this will provide a mapping back to the original
        string
        """
        return self._metadata

class NominalColumn(Column):
    """
    A column containing numerical values that are unrelated to
    one another (i.e. do not follow a progression)
    """
    def __init__(self, arr=None, metadata=None,
                 missing_id='<missing>', substitute=True):
        super(self.__class__, self).__init__(arr, metadata, missing_id)
        if substitute:
            self.substitute_values(arr)
        for x in np.unique(self._arr):
            self._groupings[x] = [x]

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return NominalColumn(self._arr, metadata=self.metadata,
                             missing_id=self._missing_id, substitute=False)

    def substitute_values(self, vect):
        """
        Internal method to substitute integers into the vector, and construct
        metadata to convert back to the original vector.

        np.nan is always given -1, all other objects are given integers in
        order of apperence.

        Parameters
        ----------
        vect : np.array
            the vector in which to substitute values in

        """
        unique = np.unique(vect)
        unique = [
            x for x in unique if not isinstance(x, float) or not math.isnan(x)
        ]

        arr = np.zeros(len(vect), dtype=int) - 1
        for new_id, value in enumerate(unique):
            arr[vect == value] = new_id
            self._metadata[new_id] = value
        self._arr = arr

        if -1 in arr:
            self._metadata[-1] = self._missing_id

    def __getitem__(self, key):
        return NominalColumn(self._arr[key], metadata=self.metadata, substitute=False)

    def __setitem__(self, key, value):
        self._arr[key] = value
        return NominalColumn(np.array(self._arr), metadata=self.metadata, substitute=False)

    def groups(self):
        return list(self._groupings.values())

    def possible_groupings(self):
        return enumerate(combinations(self._groupings.keys(), 2))

    def group(self, x, y):
        self._groupings[x] += self._groupings[y]
        del self._groupings[y]
        self._arr[self._arr == y] = x
