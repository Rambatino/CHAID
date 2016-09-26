"""
This package provides a python implementation of the Chi-Squared Automatic
Inference Detection (CHAID) decision tree.
"""
import itertools as it
import collections as cl
import numpy as np
import math
from scipy import stats
from treelib import Tree


class CHAIDVector(object):
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
        if substitute:
            self.substitute_values(arr)

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

    def __iter__(self):
        return iter(self._arr)

    def __getitem__(self, key):
        return CHAIDVector(self._arr[key], metadata=self.metadata, substitute=False)

    def __setitem__(self, key, value):
        self._arr[key] = value
        return CHAIDVector(np.array(self._arr), metadata=self.metadata, substitute=False)

    def deep_copy(self):
        """
        Returns a deep copy.
        """
        return CHAIDVector(self._arr, metadata=self.metadata,
                           missing_id=self._missing_id, substitute=False)

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
    def __init__(self, choices=None, split=None, indices=None, node_id=0, parent=None, dep_v=None, is_terminal=False, weights=None):
        indices = [] if indices is None else indices
        self.choices = list(choices or [])
        self.split = split or CHAIDSplit(None, None, None, None, 0)
        self.indices = indices
        self.node_id = node_id
        self.parent = parent
        self.dep_v = dep_v
        self._members = None
        self.is_terminal = is_terminal
        self.weights = weights

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
            metadata = dep_v.metadata
            self._members = {}
            for member in metadata.values():
                self._members[member] = 0

            if self.weights is None:
                counts = np.transpose(np.unique(dep_v.arr, return_counts=True))
            else:
                counts = np.array([
                    [i, self.weights[dep_v.arr == i].sum()] for i in set(dep_v.arr)
                ])

            self._members.update((metadata[k], v) for k, v in counts)

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
    dof : int
        The degrees of freedom as a result of this split
    """
    def __init__(self, column, splits, chi, p, dof):
        splits = splits or []
        self.surrogates = []
        self.column_id = column
        self.split_name = None
        self.splits = list(splits)
        self.split_map = [None] * len(self.splits)
        self.chi = chi
        self.p = p
        self._dof = dof

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
        format_str = '({0.column}, p={0.p}, chi={0.chi}, groups={0.groupings})'\
                     ', dof={0.dof})'
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

    @property
    def dof(self):
        return self._dof

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
    def __init__(self, ndarr, arr, alpha_merge=0.05, max_depth=2, min_sample=30, split_titles=None, split_threshold=0, weights=None):
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
        self.weights = weights
        self.split_threshold = split_threshold

    def build_tree(self):
        """ Build chaid tree """
        self.tree_store = []
        self.node(np.arange(0, self.data_size, dtype=np.int), self.vectorised_array, self.observed,
                  wt=self.weights)

    @staticmethod
    def from_pandas_df(df, i_variables, d_variable, alpha_merge=0.05, max_depth=2, min_sample=30, split_threshold=0, weight=None):
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
        ind_df = ind_df
        ind_values = ind_df.values
        dep_values = df[d_variable].values
        weights = df[weight] if weight is not None else None
        return CHAID(ind_values, dep_values, alpha_merge, max_depth, min_sample, split_titles=list(ind_df.columns.values), split_threshold=split_threshold, weights=weights)

    def node(self, rows, ind, dep, wt=None, depth=0, parent=None, parent_decisions=None):
        """ internal method to create a node in the tree """
        depth += 1

        if self.max_depth < depth:
            terminal_node = CHAIDNode(choices=parent_decisions, node_id=self.node_count,
                                      parent=parent, indices=rows, dep_v=dep, is_terminal=True, weights=wt)
            self.tree_store.append(terminal_node)
            self.node_count += 1
            return self.tree_store

        split = self.generate_best_split(ind, dep, wt)

        split.name_columns(self.split_titles)

        node = CHAIDNode(choices=parent_decisions, node_id=self.node_count, indices=rows, dep_v=dep,
                         parent=parent, split=split, weights=wt)

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
            weight_slice = (wt[correct_rows] if wt is not None else None)
            if self.min_sample < len(dep_slice.arr):
                self.node(row_slice, ind_slice, dep_slice, depth=depth, parent=parent, parent_decisions=split.split_map[index], wt=weight_slice)
            else:
                terminal_node = CHAIDNode(choices=split.split_map[index], node_id=self.node_count,
                                          parent=parent, indices=row_slice, dep_v=dep_slice, is_terminal=True, weights=weight_slice)
                self.tree_store.append(terminal_node)
                self.node_count += 1
        return self.tree_store

    def generate_best_split(self, ind, dep, wt=None):
        """ internal method to generate the best split """
        split = CHAIDSplit(None, None, None, None, 0)
        relative_split_threshold = 1 - self.split_threshold
        st_chi = stats.chisquare
        all_dep = set(dep.arr)
        for i, index in enumerate(ind):
            index = index.deep_copy()
            unique = set(index.arr)

            mappings = MappingDict()
            freq = {}
            wt_freq = {}
            for col in unique:
                counts = np.unique(dep.arr[index.arr == col], return_counts=True)
                freq[col] = cl.defaultdict(int)
                freq[col].update(np.transpose(counts))
                if wt is not None:
                    wt_freq[col] = cl.defaultdict(int)
                    for dep_v in set(dep.arr):
                        wt_freq[col][dep_v] = wt[(index.arr == col) * (dep.arr == dep_v)].sum()

            while len(unique) > 1:
                size = int((len(unique) * (len(unique) - 1)) / 2)
                sub_data_columns = [('combinations', object), ('p', float), ('chi', float)]
                sub_data = np.array([(None, 0, 1)]*size, dtype=sub_data_columns, order='F')
                for j, comb in enumerate(it.combinations(unique, 2)):
                    if wt is None:
                        col1_freq = freq[comb[0]]
                        col2_freq = freq[comb[1]]

                        keys = set(col1_freq.keys()).union(col2_freq.keys())

                        n_ij = np.array([
                            [col1_freq.get(k, 0) for k in keys],
                            [col2_freq.get(k, 0) for k in keys]
                        ])

                        m_ij = (np.vstack(n_ij.sum(axis=1)) * n_ij.sum(axis=0)) / n_ij.sum().astype(float)
                    else:
                        col1_wt_freq = wt_freq[comb[0]]
                        col2_wt_freq = wt_freq[comb[1]]

                        keys = set(col1_wt_freq.keys()).union(col2_wt_freq.keys())

                        n_ij = np.array([
                            [col1_wt_freq.get(k, 0) for k in keys],
                            [col2_wt_freq.get(k, 0) for k in keys]
                        ])

                        m_ij = n_ij / n_ij

                        nan_mask = np.isnan(m_ij)
                        m_ij[nan_mask] = 0.000001 # otherwise it breaks the chi-squared test

                        m_ij = self.weighted_case(n_ij, m_ij)

                    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
                    ret = st_chi(n_ij, f_exp=m_ij, ddof=n_ij.size - 1 - dof, axis=None)

                    sub_data[j] = (comb, ret[1], ret[0])

                choice, highest_p_join, chi_join = max(sub_data, key=lambda x: (x[1], x[2]))


                if highest_p_join < self.alpha_merge:
                    if wt is None:
                        n_ij = np.array([
                            [f[dep_val] for dep_val in all_dep] for f in freq.values()
                        ])
                        m_ij = (np.vstack(n_ij.sum(axis=1)) * n_ij.sum(axis=0)) / n_ij.sum().astype(float)
                    else:
                        n_ij = np.array([
                            [f[dep_val] for dep_val in all_dep] for f in wt_freq.values()
                        ])
                        m_ij = n_ij / n_ij

                        nan_mask = np.isnan(m_ij)
                        m_ij[nan_mask] = 0.000001

                        m_ij = self.weighted_case(n_ij, m_ij)

                    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
                    chi, p_split = st_chi(n_ij, f_exp=m_ij, ddof=n_ij.size - 1 - dof, axis=None)

                    responses = [mappings[x] for x in unique]
                    temp_split = CHAIDSplit(i, responses, chi, p_split, dof)

                    better_split = p_split < split.p or (p_split == split.p and chi > split.chi)

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

                for val, count in freq[choice[1]].items():
                    freq[choice[0]][val] += count
                del freq[choice[1]]

                if wt is not None:
                    for val, total in wt_freq[choice[1]].items():
                        wt_freq[choice[0]][val] += total
                    del wt_freq[choice[1]]

        if split.valid():
            split.sub_split_values(ind[split.column_id].metadata)
        return split

    def weighted_case(self, n_ij, m_ij):
        w_ij = m_ij
        n_ij_col_sum = n_ij.sum(axis=1)
        n_ij_row_sum = n_ij.sum(axis=0)
        alpha, beta, eps = (1, 1, 1)
        while eps > 10e-6:
            alpha = alpha * np.vstack(n_ij_col_sum / m_ij.sum(axis=1))
            beta = n_ij_row_sum / (alpha * w_ij).sum(axis=0)
            eps = np.max(np.absolute(w_ij * alpha * beta - m_ij))
            m_ij = w_ij * alpha * beta
        return m_ij

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
