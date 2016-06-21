import itertools as it
import pandas as pd
from scipy import stats
import numpy as np
import collections as cl
from treelib import Tree
from enum import Enum

class CHAIDNode(object):
    """
    A node in the CHAID tree

    Parameters
    ----------
    choices : array-like
        Contains a list of the splits that gave rise to that node
    members : dict
        Frequency of the members at that node
    split_variable : number or string
        A value indicating what independent variable the node derived from
    chi : float
        The chi-squared score for the split
    p : float
        The p-value for the split
    terminal_indices : array-like or None
        The row index that ended up in the node (only occurs in terminal nodes)
    node_id : float 
        A float representing the id of the node
    parent : float or None
        The node_id of the parent of that node
    """
    def __init__(self, choices=None, members=None, split_variable=None, chi=0,
                 p=0, terminal_indices=None, node_id=0, parent=None):
        terminal_indices = [] if terminal_indices is None else terminal_indices
        self.choices = list(choices or [])
        self.members = members or {}
        self.split_variable = split_variable
        self.chi = chi
        self.p = p
        self.terminal_indices = terminal_indices
        self.node_id = node_id
        self.parent = parent

    def __hash__(self):
        return hash(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        format_str = '({choices}, {members}, {split_variable}, {chi}, {p})'
        return format_str.format(**self.__dict__)

    def __lt__(self, other):
        return self.node_id < other.node_id


class CHAIDSplit(object):
    """
    A potential split for a node in to produce children

    Parameters
    ----------
    index : float
        The key of where the split is occuring relative to the input data
    splits : array-like
        The grouped variables
    split_map : array-like
        The name of the grouped variables
    score : float
        The statistical score value of that split
    p : float
        The p value of that split
    """
    def __init__(self, index, splits, score, p):
        splits = splits or []
        self.index = index
        self.splits = list(splits)
        self.split_map = [None] * len(self.splits)
        self.score = score
        self.p = p

    def sub_split_values(self, sub):
        """ substiutes the splits with other values into the split_map """
        for i, arr in enumerate(self.splits):
            self.split_map[i] = [sub.get(x, x) for x in arr]


class MappingDict(dict):
    """ a dict with a default value when no key present """
    def __missing__(self, key):
        value = self[key] = [key]
        return value


class CHAIDVariableTypes(Enum):
    nominal = 0
    ordinal = 1
    continuous = 3

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
        the threshold value for the maximum number of levels after the root node in the tree (default 2)
    min_sample : float
        the threshold value of the number of respondents that the node must contain (default 30)
    missing_id : string 
        the name of the nan values in the data
    split_titles : array-like 
        array of names for the independent variables in the data
    """
    def __init__(self, ndarr, arr, alpha_merge=0.05, max_depth=2, min_sample=30, missing_id='<missing>', 
                 split_titles=None, independent_variable_types=None, dependent_variable_type=None):
        self.alpha_merge = alpha_merge
        self.max_depth = max_depth
        self.min_sample = min_sample
        self.missing_id = missing_id
        self.i_v_types = independent_variable_types or [CHAIDVariableTypes(0)] * ndarr.shape[1]
        self.d_v_type = dependent_variable_type or CHAIDVariableTypes(0)
        self.split_titles = split_titles or []
        self.ind_metadata = {}
        self.dep_metadata = {}
        for ind in range(0, ndarr.shape[1]):
            ndarr[:, ind], self.ind_metadata[ind] = self.sub_non_floats(ndarr[:, ind])
        ndarr = ndarr.astype(float, subok=False, order='K', copy=False)
        arr, self.dep_metadata = self.sub_non_floats(arr)
        self.data_size = ndarr.shape[0]
        self.node_count = 0
        self.tree_store = []
        self.node(np.arange(0, self.data_size, dtype=np.int), ndarr, arr)

    @staticmethod
    def from_pandas_df(df, i_variables, d_variable, alpha_merge=0.05, max_depth=2, min_sample=30,
                        independent_variable_types=None, dependent_variable_type=None):
        """
        Helper method to pre-process a pandas data frame in order to run CHAID analysis
        
        Parameters
        ----------
        df :  pandas.DataFrame
            the dataframe with the dependent and independent variables in which to slice from
        i_variables :  array-like
            list of the column names for the independent variables
        d_variable : string
            the name of the dependent variable in the dataframe 
        alpha_merge : float
            the threshold value in which to create a split (default 0.05)
        max_depth : float
            the threshold value for the maximum number of levels after the root node in the tree (default 2)
        min_sample : float
            the threshold value of the number of respondents that the node must contain (default 30)
        """
        ind_df = df[i_variables]
        ind_values = ind_df.values
        dep_values = df[d_variable].values
        if independent_variable_types is not None:
            independent_variable_types = [CHAIDVariableTypes[x] for x in independent_variable_types]
        if dependent_variable_type is not None:
            dependent_variable_type = CHAIDVariableTypes[dependent_variable_type]
        return CHAID(ind_values, dep_values, alpha_merge, max_depth, min_sample, 
                     split_titles=list(ind_df.columns.values), independent_variable_types=independent_variable_types,
                     dependent_variable_type=dependent_variable_type)

    def sub_non_floats(self, vect):
        """
        substitute floats into the vector if it does not have a dtype of float

        Parameters
        ----------     
        vect : nd.array
            the vector in whcih to substitute the float

        Returns
        ----------
        tuple : prcoessed vector, hash or substitutions
        """
        vector = vect
        meta = {}
        if vect.dtype != float:
            unique_v = np.unique(vector.astype(str))
            float_map = [(x, float(i)) for i, x in enumerate(unique_v)]
            for value, new_id in float_map:
                vector[vector == value] = new_id
            vector = vector.astype(float, subok=False, order='K', copy=False)
            nans = np.isnan(vector)
            vector[nans] = -1.0
            meta = {v: k for k, v in float_map}
        else:
            nans = np.isnan(vector)
            vector[nans] = -1.0
        meta[-1.0] = self.missing_id
        return vector, meta

    def node(self, rows, ind, dep, depth=0, parent=None, parent_decisions=None):
        """ inteneral method to create a node in the tree """
        depth = depth + 1

        members = np.transpose(np.unique(dep, return_counts=True))
        members = dict((self.dep_metadata.get(k, k), v) for k, v in members)

        if self.max_depth < depth:
            terminal_node = CHAIDNode(choices=parent_decisions, members=members, node_id=self.node_count,
                                      parent=parent, terminal_indices=rows)
            self.tree_store.append(terminal_node)
            self.node_count += 1
            return self.tree_store

        split = self.generate_best_split(ind, dep)

        if split.index is not None and len(self.split_titles) > split.index:
            split_name = self.split_titles[split.index]
        else:
            split_name = split.index

        node = CHAIDNode(choices=parent_decisions, members=members, node_id=self.node_count,
                         parent=parent, chi=split.score, p=split.p, split_variable=split_name)
        self.tree_store.append(node)
        parent = self.node_count
        self.node_count += 1

        if split.index is None:
            return self.tree_store

        for index, choices in enumerate(split.splits):
            correct_rows = np.in1d(ind[:, split.index], choices)
            dep_slice = dep[correct_rows]
            ind_slice = ind[correct_rows, :]
            row_slice = rows[correct_rows]
            if self.min_sample < len(dep_slice):
                self.node(row_slice, ind_slice, dep_slice, depth=depth, parent=parent, parent_decisions=split.split_map[index])
            else:
                members = np.transpose(np.unique(dep_slice, return_counts=True))
                members = dict((self.dep_metadata.get(k, k), v) for k, v in members)

                terminal_node = CHAIDNode(choices=split.split_map[index], members=members, node_id=self.node_count,
                                          parent=parent, terminal_indices=row_slice)
                self.tree_store.append(terminal_node)
                self.node_count += 1
        return self.tree_store

    def generate_best_split(self, ind, dep):
        """ inteneral method to generate the best split """
        split = CHAIDSplit(None, None, None, 1)
        for i in range(0, ind.shape[1]):
            index = np.array(ind[:, i])
            unique = set(index)

            mappings = MappingDict()
            frequencies = {}
            for col in unique:
                if self.d_v_type == CHAIDVariableTypes(3):
                    frequencies[col] = dep[index == col]
                else:
                    counts = np.unique(dep[index == col][0], return_counts=True)
                    frequencies[col] = cl.defaultdict(int)
                    frequencies[col].update(np.transpose(counts))

            while len(unique) > 1:
                size = int((len(unique) * (len(unique) - 1)) / 2)
                sub_data = np.ndarray(shape=(size, 3), dtype=object, order='F')
                for j, comb in enumerate(it.combinations(unique, 2)):
                    y = frequencies[comb[0]]
                    g = frequencies[comb[1]]
                    if self.d_v_type == CHAIDVariableTypes(3):
                        levene = stats.levene(y, g)
                        sub_data[j] = (comb, levene[0], levene[1])
                    else:
                        keys = set(y.keys()).union(g.keys())

                        cr_table = [
                            [y.get(k, 0) for k in keys],
                            [g.get(k, 0) for k in keys]
                        ]

                        chi = stats.chi2_contingency(np.array(cr_table))
                        sub_data[j] = (comb, chi[0], chi[1])

                highest_p_split = np.sort(sub_data[:, 2])[-1]
                correct_row = np.where(np.in1d(sub_data[:, 2], highest_p_split))[0][0]

                if size == 1 or highest_p_split < self.alpha_merge:
                    if highest_p_split < split.p:
                        score = sub_data[correct_row][1]
                        # if self.d_v_type == CHAIDVariableTypes(3):
                        #     responses = []
                        # else:
                        responses = [mappings[x] for x in unique]
                        split = CHAIDSplit(i, responses, score, highest_p_split)
                    break

                choice = list(sub_data[correct_row, 0])

                if choice[1] in mappings:
                    mappings[choice[0]] += mappings[choice[1]]
                    del mappings[choice[1]]
                else:
                    mappings[choice[0]] += [choice[1]]

                index[index == choice[1]] = choice[0]
                unique.remove(choice[1])

                if self.d_v_type == CHAIDVariableTypes(3):
                    frequencies[choice[0]] = np.concatenate((frequencies[choice[0]], frequencies[choice[1]]), axis=0)        
                else:
                    for val, count in frequencies[choice[1]].items():
                        frequencies[choice[0]][val] += count
                del frequencies[choice[1]]

        split.sub_split_values(self.ind_metadata.get(split.index, {}))
        return split

    def to_tree(self):
        """ returns a TreeLib tree """
        tree = Tree()
        for node in self.tree_store:
            tree.create_node(node, node.node_id, parent=node.parent)
        return tree

    def print_tree(self):
        """ prints the tree out """
        self.to_tree().show()

    def predict(self):
        """ determines which rows fall into which node """
        pred = np.zeros(self.data_size)
        for node in self.tree_store:
            pred[node.terminal_indices] = node.node_id
        return pred

    def __repr__(self):
        return str(self.tree_store)
