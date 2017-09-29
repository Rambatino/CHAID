import numpy as np
from math import isnan
from itertools import combinations
from .mapping_dict import MappingDict

def is_sorted(ndarr, nan_val=None):
    store = []
    for arr in ndarr:
        if arr == [] or len(arr) == 1: continue
        if nan_val is not None and nan_val in arr:
            arr.remove(nan_val)
        store.append(arr[-1] - arr[0] == len(arr) - 1)
    return all(store)

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
    def __init__(self, arr=None, metadata=None, missing_id='<missing>',
                 substitute=True, weights=None, name=None):
        self.metadata = dict(metadata or {})
        self.arr = np.array(arr)
        self._missing_id = missing_id
        self.weights = weights
        self.name = name

    def __iter__(self):
        return iter(self.arr)

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def possible_groupings(self):
        raise NotImplementedError

    @property
    def type(self):
        """
        Returns a string representing the type
        """
        raise NotImplementedError

    def deep_copy(self):
        """
        Returns a deep copy
        """
        raise NotImplementedError

    def bell_set(self, collection, ordinal=False):
        """
        Calculates the Bell set
        """
        if len(collection) == 1:
            yield [ collection ]
            return

        first = collection[0]
        for smaller in self.bell_set(collection[1:]):
            for n, subset in enumerate(smaller):
                if not ordinal or (ordinal and is_sorted(smaller[:n] + [[ first ] + subset] + smaller[n+1:], self._nan)):
                    yield smaller[:n] + [[ first ] + subset] + smaller[n+1:]

            if not ordinal or (ordinal and is_sorted([ [ first ] ] + smaller, self._nan)):
                yield [ [ first ] ] + smaller


class NominalColumn(Column):
    """
    A column containing numerical values that are unrelated to
    one another (i.e. do not follow a progression)
    """
    def __init__(self, arr=None, metadata=None, missing_id='<missing>',
                 substitute=True, weights=None, name=None):
        super(self.__class__, self).__init__(arr, metadata=metadata, missing_id=missing_id, weights=weights, name=name)
        if substitute and metadata is None:
            self.substitute_values(arr)

        self._groupings = MappingDict()
        for x in np.unique(self.arr):
            self._groupings[x] = [x]

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return NominalColumn(self.arr, metadata=self.metadata, name=self.name,
                             missing_id=self._missing_id, substitute=False, weights=self.weights)

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

        try:
            unique = np.unique(vect)
        except:
            unique = set(vect)

        unique = [
            x for x in unique if not isinstance(x, float) or not isnan(x)
        ]

        arr = np.copy(vect)
        for new_id, value in enumerate(unique):
            np.place(arr, arr==value, new_id)
            self.metadata[new_id] = value
        arr = arr.astype(np.float)
        np.place(arr, np.isnan(arr), -1)
        self.arr = arr

        if -1 in arr:
            self.metadata[-1] = self._missing_id

    def __getitem__(self, key):
        new_weights = None if self.weights is None else self.weights[key]
        return NominalColumn(self.arr[key], metadata=self.metadata, substitute=False, weights=new_weights, name=self.name)

    def __setitem__(self, key, value):
        self.arr[key] = value
        return self

    def groups(self):
        return list(self._groupings.values())

    def possible_groupings(self):
        return combinations(self._groupings.keys(), 2)

    def all_combinations(self):
        bell_set = self.bell_set(sorted(list(self._groupings.keys())))
        next(bell_set)
        return bell_set

    def group(self, x, y):
        self._groupings[x] += self._groupings[y]
        del self._groupings[y]
        self.arr[self.arr == y] = x

    @property
    def type(self):
        """
        Returns a string representing the type
        """
        return 'nominal'


class OrdinalColumn(Column):
    """
    A column containing integer values that have an order
    """
    def __init__(self, arr=None, metadata=None, missing_id='<missing>',
                 groupings=None, substitute=True, weights=None, name=None):
        super(self.__class__, self).__init__(arr, metadata, missing_id=missing_id, weights=weights, name=name)
        self._nan = np.array([np.nan]).astype(int)[0]

        if substitute and metadata is None:
            self.arr, self.orig_type = self.substitute_values(self.arr)
        elif substitute and metadata and not np.issubdtype(self.arr.dtype, np.integer):
            # custom metadata has been passed in from external source, and must be converted to int
            self.arr = self.arr.astype(int)
            self.metadata = { int(k):v for k, v in metadata.items() }
            self.metadata[self._nan] = missing_id

        self._groupings = {}
        if groupings is None:
            for x in np.unique(self.arr):
                self._groupings[x] = [x, x + 1, False]
        else:
            for x in np.unique(self.arr):
                self._groupings[x] = list(groupings[x])
        self._possible_groups = None

    def substitute_values(self, vect):
        if not np.issubdtype(vect.dtype, np.integer):
            uniq = set(vect)
            uniq_floats = np.array(list(uniq), dtype=float)
            uniq_ints = uniq_floats.astype(int)
            nan = self._missing_id
            self.metadata = {
                new: nan if isnan(as_float) else old
                for old, as_float, new in zip(uniq, uniq_floats, uniq_ints)
            }
            self.arr = self.arr.astype(float)
        return self.arr.astype(int), self.arr.dtype.type

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return OrdinalColumn(self.arr, metadata=self.metadata, name=self.name,
                             missing_id=self._missing_id, substitute=True,
                             groupings=self._groupings, weights=self.weights)

    def __getitem__(self, key):
        new_weights = None if self.weights is None else self.weights[key]
        return OrdinalColumn(self.arr[key], metadata=self.metadata, name=self.name,
                             missing_id=self._missing_id, substitute=True,
                             groupings=self._groupings, weights=new_weights)

    def __setitem__(self, key, value):
        self.arr[key] = value
        return self

    def groups(self):
        vals = self._groupings.values()
        return [
            [x for x in range(minmax[0], minmax[1])] + ([self._nan] if minmax[2] else [])
            for minmax in vals
        ]

    def possible_groupings(self):
        if self._possible_groups is None:
            ranges = sorted(self._groupings.items())
            candidates = zip(ranges[0:], ranges[1:])
            self._possible_groups = [
                (k1, k2) for (k1, minmax1), (k2, minmax2) in candidates
                if minmax1[1] == minmax2[0]
            ]
            if self._nan in self.arr:
                self._possible_groups += [
                    (key, self._nan) for key in self._groupings.keys() if key != self._nan
                ]
        return self._possible_groups.__iter__()

    def all_combinations(self):
        bell_set = self.bell_set(sorted(list(self._groupings.keys())), True)
        next(bell_set)
        return bell_set


    def group(self, x, y):
        self._possible_groups = None
        if y != self._nan:
            x = int(x)
            y = int(y)
            x_max = self._groupings[x][1]
            y_min = self._groupings[y][0]
            if y_min >= x_max:
                self._groupings[x][1] = self._groupings[y][1]
            else:
                self._groupings[x][0] = y_min
            self._groupings[x][2] = self._groupings[x][2] or self._groupings[y][2]
        else:
            self._groupings[x][2] = True

        del self._groupings[y]
        self.arr[self.arr == y] = x

    @property
    def type(self):
        """
        Returns a string representing the type
        """
        return 'ordinal'

class ContinuousColumn(Column):
    """
    A column containing numerical values on a continuous scale
    """
    def __init__(self, arr=None, metadata=None, missing_id='<missing>',
                 weights=None):
        if not np.issubdtype(arr.dtype, np.number):
            raise ValueError('Must only pass numerical values to create continuous column')

        super(self.__class__, self).__init__(np.nan_to_num(arr), metadata, missing_id=missing_id, weights=weights)

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return ContinuousColumn(self.arr, metadata=self.metadata, missing_id=self._missing_id, weights=self.weights)

    def __getitem__(self, key):
        new_weights = None if self.weights is None else self.weights[key]
        return ContinuousColumn(self.arr[key], metadata=self.metadata, weights=new_weights)

    def __setitem__(self, key, value):
        self.arr[key] = value
        return self

    @property
    def type(self):
        """
        Returns a string representing the type
        """
        return 'continuous'
