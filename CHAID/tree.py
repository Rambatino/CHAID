import collections as cl
import numpy as np
from scipy import stats
from treelib import Tree as TreeLibTree
from .node import Node
from .split import Split
from .column import NominalColumn


def chisquare(n_ij, weighted):
    """
    Calculates the chisquare for a matrix of ind_v x dep_v
    for the unweighted and SPSS weighted case
    """
    if weighted:
        m_ij = n_ij / n_ij

        nan_mask = np.isnan(m_ij)
        m_ij[nan_mask] = 0.000001 # otherwise it breaks the chi-squared test

        w_ij = m_ij
        n_ij_col_sum = n_ij.sum(axis=1)
        n_ij_row_sum = n_ij.sum(axis=0)
        alpha, beta, eps = (1, 1, 1)
        while eps > 10e-6:
            alpha = alpha * np.vstack(n_ij_col_sum / m_ij.sum(axis=1))
            beta = n_ij_row_sum / (alpha * w_ij).sum(axis=0)
            eps = np.max(np.absolute(w_ij * alpha * beta - m_ij))
            m_ij = w_ij * alpha * beta

    else:
        m_ij = (np.vstack(n_ij.sum(axis=1)) * n_ij.sum(axis=0)) / n_ij.sum().astype(float)

    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
    chi, p_val = stats.chisquare(n_ij, f_exp=m_ij, ddof=n_ij.size - 1 - dof, axis=None)

    return (chi, p_val, dof)

class Tree(object):
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
    min_parent_node_size : float
        the threshold value of the number of respondents that the node must
        contain (default 30)
    split_titles : array-like
        array of names for the independent variables in the data
    """
    def __init__(self, ndarr, arr, alpha_merge=0.05, max_depth=2, min_parent_node_size=30,
                 min_child_node_size=None, split_titles=None, split_threshold=0, weights=None):
        self.alpha_merge = alpha_merge
        self.max_depth = max_depth
        self.min_parent_node_size = min_parent_node_size
        self.min_child_node_size = min_child_node_size
        self.split_titles = split_titles or []
        self.vectorised_array = []
        for ind in range(0, ndarr.shape[1]):
            self.vectorised_array.append(NominalColumn(ndarr[:, ind]))
        self.data_size = ndarr.shape[0]
        self.node_count = 0
        self.tree_store = None
        self.observed = NominalColumn(arr)
        self.weights = weights
        self.split_threshold = split_threshold

    def build_tree(self):
        """ Build chaid tree """
        self.tree_store = []
        self.node(np.arange(0, self.data_size, dtype=np.int), self.vectorised_array, self.observed,
                  wt=self.weights)

    @staticmethod
    def from_pandas_df(df, i_variables, d_variable, alpha_merge=0.05, max_depth=2,
                       min_parent_node_size=30, min_child_node_size=0, split_threshold=0,
                       weight=None):
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
        min_parent_node_size : float
            the threshold value of the number of respondents that the node must
            contain (default 30)
        """
        ind_df = df[i_variables]
        ind_df = ind_df
        ind_values = ind_df.values
        dep_values = df[d_variable].values
        weights = df[weight] if weight is not None else None
        return Tree(ind_values, dep_values, alpha_merge, max_depth, min_parent_node_size,
                    min_child_node_size, list(ind_df.columns.values), split_threshold, weights)

    def node(self, rows, ind, dep, wt=None, depth=0, parent=None, parent_decisions=None):
        """ internal method to create a node in the tree """
        depth += 1

        if self.max_depth < depth:
            terminal_node = Node(choices=parent_decisions, node_id=self.node_count,
                                 parent=parent, indices=rows, dep_v=dep, is_terminal=True,
                                 weights=wt)
            self.tree_store.append(terminal_node)
            self.node_count += 1
            return self.tree_store

        split = self.generate_best_split(ind, dep, wt)

        split.name_columns(self.split_titles)

        node = Node(choices=parent_decisions, node_id=self.node_count, indices=rows, dep_v=dep,
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
            weight_slice = wt[correct_rows] if wt is not None else None
            if self.min_parent_node_size < len(dep_slice.arr):
                self.node(row_slice, ind_slice, dep_slice, depth=depth, parent=parent,
                          parent_decisions=split.split_map[index], wt=weight_slice)
            else:
                terminal_node = Node(choices=split.split_map[index], node_id=self.node_count,
                                     parent=parent, indices=row_slice, dep_v=dep_slice,
                                     is_terminal=True, weights=weight_slice)
                self.tree_store.append(terminal_node)
                self.node_count += 1
        return self.tree_store

    def generate_best_split(self, ind, dep, wt=None):
        """ internal method to generate the best split """
        split = Split(None, None, None, None, 0)
        relative_split_threshold = 1 - self.split_threshold
        all_dep = set(dep.arr)
        for i, index in enumerate(ind):
            index = index.deep_copy()
            unique = set(index.arr)

            freq = {}
            for col in unique:
                counts = np.unique(dep.arr[index.arr == col], return_counts=True)
                if wt is None:
                    freq[col] = cl.defaultdict(int)
                    freq[col].update(np.transpose(counts))
                else:
                    freq[col] = cl.defaultdict(int)
                    for dep_v in set(dep.arr):
                        freq[col][dep_v] = wt[(index.arr == col) * (dep.arr == dep_v)].sum()

            while next(index.possible_groupings(), None) is not None:
                groupings = list(index.possible_groupings())
                size = len(groupings)

                sub_data_columns = [('combinations', object), ('p', float), ('chi', float)]
                sub_data = np.array([(None, 0, 1)]*size, dtype=sub_data_columns, order='F')
                for j, comb in groupings:
                    col1_freq = freq[comb[0]]
                    col2_freq = freq[comb[1]]

                    keys = set(col1_freq.keys()).union(col2_freq.keys())

                    n_ij = np.array([
                        [col1_freq.get(k, 0) for k in keys],
                        [col2_freq.get(k, 0) for k in keys]
                    ])

                    chi, p_split, dof = chisquare(n_ij, wt is not None)

                    sub_data[j] = (comb, p_split, chi)

                choice, highest_p_join, chi_join = max(sub_data, key=lambda x: (x[1], x[2]))

                sufficient_split = highest_p_join < self.alpha_merge and all(
                    sum(node_v.values()) >= self.min_child_node_size for node_v in freq.values()
                )

                if sufficient_split and len(freq.values()) > 1:
                    n_ij = np.array([
                        [f[dep_val] for dep_val in all_dep] for f in freq.values()
                    ])

                    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
                    chi, p_split, dof = chisquare(n_ij, wt is not None)

                    temp_split = Split(i, index.groups(), chi, p_split, dof)

                    better_split = not split.valid() or p_split < split.p or (p_split == split.p and chi > split.chi)

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

                index.group(choice[0], choice[1])

                for val, count in freq[choice[1]].items():
                    freq[choice[0]][val] += count
                del freq[choice[1]]

        if split.valid():
            split.sub_split_values(ind[split.column_id].metadata)
        return split


    def to_tree(self):
        """ returns a TreeLib tree """
        tree = TreeLibTree()
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
