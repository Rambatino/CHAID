"""
This package provides a python implementation of the Chi-Squared Automatic
Inference Detection (CHAID) decision tree.
"""
import itertools as it
import collections as cl
import numpy as np
from scipy import stats
from treelib import Tree
import operator


class CHAIDVector(object):
    """
    A numpy array with metadata

    Parameters
    ----------
    arr : array-like
        The numpy array
    metadata : dict
        The substitutions of the vector
    missing_id : string
        An identifier for the missing value to be associated
    """
    def __init__(self, arr=None, metadata=None, missing_id='<missing>'):
        self._metadata = metadata or {}
        self._arr = None
        self._missing_id = missing_id
        self.sub_non_floats(arr)

    def sub_non_floats(self, vect):
        """
        Substitute floats into the vector if it does not have a dtype of float

        Parameters
        ----------
        vect : nd.array
            the vector in whcih to substitute the float

        Returns
        ----------
        tuple : prcoessed vector, hash or substitutions
        """
        self._arr = np.array(vect)
        if vect.dtype != float and vect.dtype != int:
            unique_v = np.unique(self._arr)
            float_map = [(x, float(i)) for i, x in enumerate(unique_v)]
            for value, new_id in float_map:
                self._arr[self._arr == value] = new_id
            self._arr = self._arr.astype(float, subok=False, copy=False)
            nans = np.isnan(self._arr)
            self._arr[nans] = -1.0
            self._metadata = {v: k for k, v in float_map}
        else:
            nans = np.isnan(self._arr)
            self._arr[nans] = -1.0
        self._metadata[-1.0] = self._missing_id

    def __iter__(self):
        return iter(self._arr)

    def __getitem__(self, key):
        return CHAIDVector(self._arr[key], metadata=self.metadata)

    def __setitem__(self, key, value):
        self._arr[key] = value
        return CHAIDVector(np.array(self._arr), metadata=self.metadata)

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return CHAIDVector(np.array(self._arr), metadata=self.metadata)

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


class CHAIDNode(object):
    """
    A node in the CHAID tree

    Parameters
    ----------
    choices : array-like
        Contains a list of the splits that gave rise to that node
    split_variable : number or string
        A value indicating what independent variable the node derived from
    chi : float
        The chi-squared score for the split
    p : float
        The p-value for the split
    indices : array-like or None
        The row index that ended up in the node (only occurs in terminal nodes)
    node_id : float
        A float representing the id of the node
    parent : float or None
        The node_id of the parent of that node
    dep_v : array-like
        The dependent variable set
    is_terminal : boolean
        Whether the node is terminal
    """
    def __init__(self, choices=None, split=None, indices=None, node_id=0, parent=None, dep_v=None, is_terminal=False):
        indices = [] if indices is None else indices
        self.choices = list(choices or [])
        self.split = split or CHAIDSplit(None, None, None, None)
        self.indices = indices
        self.node_id = node_id
        self.parent = parent
        self.dep_v = dep_v
        self._members = None
        self.is_terminal = is_terminal

    def __hash__(self):
        return hash(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        format_str = '({0.choices}, {0.members}, {0.split})'
        return format_str.format(self)

    def __lt__(self, other):
        return self.node_id < other.node_id

    @property
    def chi(self):
        return self.split.chi

    @property
    def p(self):
        return self.split.p

    @property
    def split_variable(self):
        return self.split.column

    @property
    def members(self):
        if self._members is None:
            dep_v = self.dep_v
            counts = np.transpose(np.unique(dep_v.arr, return_counts=True))
            self._members = {dep_v.metadata.get(k, k): v for k, v in counts}
        return self._members


class CHAIDSplit(object):
    """
    A potential split for a node in to produce children

    Parameters
    ----------
    column : float
        The key of where the split is occuring relative to the input data
    splits : array-like
        The grouped variables
    split_map : array-like
        The name of the grouped variables
    chi : float
        The chi-square value of that split
    p : float
        The p value of that split
    """
    def __init__(self, column, splits, chi, p):
        splits = splits or []
        self.surrogates = []
        self.column_id = column
        self.split_name = None
        self.splits = list(splits)
        self.split_map = [None] * len(self.splits)
        self.chi = chi
        self.p = p

    def sub_split_values(self, sub):
        """ Substiutes the splits with other values into the split_map """
        for i, arr in enumerate(self.splits):
            self.split_map[i] = [sub.get(x, x) for x in arr]
        for split in self.surrogates:
            split.sub_split_values(sub)

    def name_columns(self, sub):
        """ Substiutes the split column index with a human readable string """
        if self.column_id is not None and len(sub) > self.column_id:
            self.split_name = sub[self.column_id]
        for split in self.surrogates:
            split.name_columns(sub)

    def __repr__(self):
        format_str = '({0.column}, p={0.p}, chi={0.chi}, groups={0.groupings})'
        if not self.valid():
            return '<Invalid Chaid Split>'
        return format_str.format(self)

    @property
    def column(self):
        if not self.valid():
            return None
        return self.split_name or str(self.column_id)

    @property
    def groupings(self):
        if not self.valid():
            return "[]"
        if all(x is None for x in self.split_map):
            return str(self.splits)
        return str(self.split_map)

    def valid(self):
        return self.column_id is not None


class MappingDict(dict):
    """ a dict with a default value when no key present """
    def __missing__(self, key):
        value = self[key] = [key]
        return value


class CHAID(object):
    """
    Create a CHAID object which contains all the information of the tree

    Parameters
    ----------
    ndarr : numpy.ndarray
        non-aggregated 2-dimensional array containing
        independent variables on the veritcal axis and (usually)
        respondent level data on the horizontal axis
    arr : numpy.ndarray
        1-dimensional array of the dependent variable associated with
        ndarr
    alpha_merge : float
        the threshold value in which to create a split (default 0.05)
    max_depth : float
        the threshold value for the maximum number of levels after the root
        node in the tree (default 2)
    min_sample : float
        the threshold value of the number of respondents that the node must
        contain (default 30)
    split_titles : array-like
        array of names for the independent variables in the data
    """
    def __init__(self, ndarr, arr, alpha_merge=0.05, max_depth=2, min_sample=30, split_titles=None, split_threshold=0):
        self.alpha_merge = alpha_merge
        self.max_depth = max_depth
        self.min_sample = min_sample
        self.split_titles = split_titles or []
        self.vectorised_array = []
        for ind in range(0, ndarr.shape[1]):
            self.vectorised_array.append(CHAIDVector(ndarr[:, ind]))
        self.data_size = ndarr.shape[0]
        self.node_count = 0
        self.tree_store = None
        self.observed = CHAIDVector(arr)
        self.split_threshold = split_threshold

    def build_tree(self):
        """ Build chaid tree """
        self.tree_store = []
        self.node(np.arange(0, self.data_size, dtype=np.int), self.vectorised_array, self.observed)

    @staticmethod
    def from_pandas_df(df, i_variables, d_variable, alpha_merge=0.05, max_depth=2, min_sample=30, split_threshold=0):
        """
        Helper method to pre-process a pandas data frame in order to run CHAID
        analysis

        Parameters
        ----------
        df :  pandas.DataFrame
            the dataframe with the dependent and independent variables in which
            to slice from
        i_variables :  array-like
            list of the column names for the independent variables
        d_variable : string
            the name of the dependent variable in the dataframe
        alpha_merge : float
            the threshold value in which to create a split (default 0.05)
        max_depth : float
            the threshold value for the maximum number of levels after the root
            node in the tree (default 2)
        min_sample : float
            the threshold value of the number of respondents that the node must
            contain (default 30)
        """
        ind_df = df[i_variables]
        ind_values = ind_df.values
        dep_values = df[d_variable].values
        return CHAID(ind_values, dep_values, alpha_merge, max_depth, min_sample, split_titles=list(ind_df.columns.values), split_threshold=split_threshold)

    def node(self, rows, ind, dep, depth=0, parent=None, parent_decisions=None):
        """ internal method to create a node in the tree """
        depth = depth + 1

        if self.max_depth < depth:
            terminal_node = CHAIDNode(choices=parent_decisions, node_id=self.node_count,
                                      parent=parent, indices=rows, dep_v=dep, is_terminal=True)
            self.tree_store.append(terminal_node)
            self.node_count += 1
            return self.tree_store

        split = self.generate_best_split(ind, dep)

        split.name_columns(self.split_titles)

        node = CHAIDNode(choices=parent_decisions, node_id=self.node_count, indices=rows, dep_v=dep,
                         parent=parent, split=split)

        self.tree_store.append(node)
        parent = self.node_count
        self.node_count += 1

        if not split.valid():
            node.is_terminal = True
            return self.tree_store

        for index, choices in enumerate(split.splits):
            correct_rows = np.in1d(ind[split.column_id].arr, choices)
            dep_slice = dep[correct_rows]
            ind_slice = [vect[correct_rows] for vect in ind]
            row_slice = rows[correct_rows]
            if self.min_sample < len(dep_slice.arr):
                self.node(row_slice, ind_slice, dep_slice, depth=depth, parent=parent, parent_decisions=split.split_map[index])
            else:
                terminal_node = CHAIDNode(choices=split.split_map[index], node_id=self.node_count,
                                          parent=parent, indices=row_slice, dep_v=dep_slice, is_terminal=True)
                self.tree_store.append(terminal_node)
                self.node_count += 1
        return self.tree_store

    def generate_best_split(self, ind, dep):
        """ internal method to generate the best split """
        split = CHAIDSplit(None, None, None, 1)
        relative_split_threshold = 1 - self.split_threshold
        for i, index in enumerate(ind):
            index = index.deep_copy()
            unique = set(index.arr)

            mappings = MappingDict()
            frequencies = {}
            for col in unique:
                counts = np.unique(dep.arr[index.arr == col], return_counts=True)
                frequencies[col] = cl.defaultdict(int)
                frequencies[col].update(np.transpose(counts))

            while len(unique) > 1:
                size = int((len(unique) * (len(unique) - 1)) / 2)
                sub_data_columns = [('combinations', object), ('chi', float), ('p', float)]
                sub_data = np.array([(None, 0, 1)]*size, dtype=sub_data_columns, order='F')
                for j, comb in enumerate(it.combinations(unique, 2)):
                    col1_freq = frequencies[comb[0]]
                    col2_freq = frequencies[comb[1]]

                    keys = set(col1_freq.keys()).union(col2_freq.keys())

                    cr_table = [
                        [col1_freq.get(k, 0) for k in keys],
                        [col2_freq.get(k, 0) for k in keys]
                    ]

                    chi = stats.chi2_contingency(np.array(cr_table), correction=False)
                    sub_data[j] = (comb, chi[0], chi[1])

                choice, chi, highest_p_split = max(sub_data, key=lambda x: (x[2], x[1]))

                if size == 1 or highest_p_split < self.alpha_merge:
                    responses = [mappings[x] for x in unique]
                    temp_split = CHAIDSplit(i, responses, chi, highest_p_split)

                    better_split = highest_p_split < split.p or (highest_p_split == split.p and chi > split.chi)
                    
                    if not split.valid() or better_split:
                        split, temp_split = temp_split, split

                    chi_threshold = relative_split_threshold * split.chi

                    if temp_split.valid() and temp_split.chi >= chi_threshold:
                        for sur in temp_split.surrogates:
                            if sur.column_id != i and sur.chi >= chi_threshold:
                                split.surrogates.append(sur)

                        temp_split.surrogates = []
                        split.surrogates.append(temp_split)

                    break

                if choice[1] in mappings:
                    mappings[choice[0]] += mappings[choice[1]]
                    del mappings[choice[1]]
                else:
                    mappings[choice[0]] += [choice[1]]

                index[index.arr == choice[1]] = choice[0]
                unique.remove(choice[1])

                for val, count in frequencies[choice[1]].items():
                    frequencies[choice[0]][val] += count
                del frequencies[choice[1]]

        if split.valid():
            split.sub_split_values(ind[split.column_id].metadata)
        return split

    def to_tree(self):
        """ returns a TreeLib tree """
        tree = Tree()
        for node in self:
            tree.create_node(node, node.node_id, parent=node.parent)
        return tree

    def __iter__(self):
        """ Function to allow nodes to be iterated over """
        if not self.tree_store:
            self.build_tree()
        return iter(self.tree_store)

    def __repr__(self):
        if not self.tree_store:
            self.build_tree()
        return str(self.tree_store)

    def get_node(self, node_id):
        """
        Returns the node with the given id
        Parameters
        ----------
        node_id : integer
            Find the node with this ID
        """
        if not self.tree_store:
            self.build_tree()
        return self.tree_store[node_id]

    def print_tree(self):
        """ prints the tree out """
        self.to_tree().show()

    def node_predictions(self):
        """ Determines which rows fall into which node """
        pred = np.zeros(self.data_size)
        for node in self:
            if node.is_terminal:
                pred[node.indices] = node.node_id
        return pred

    def model_predictions(self):
        """
        Determines the highest frequency of
        categorical dependent variable in the
        terminal node where that row fell
        """
        pred = np.zeros(self.data_size)
        for node in self:
            if node.is_terminal:
                pred[node.indices] = max(node.members, key=node.members.get)
        return pred

    def risk(self):
        """
        Calculates the fraction of risk associated
        with the model predictions
        """
        model_predictions = self.model_predictions()
        observed = self.observed.arr
        return 1 - float((model_predictions == observed).sum()) / self.data_size
