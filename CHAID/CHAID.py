import itertools as it
import pandas as pd
from scipy import stats
import numpy as np
import collections as cl
from treelib import Tree


class CHAIDNode(object):
    def __init__(self, choices=None, members=None, split_variable=None, chi=0,
                 p=0, terminal_indices=None, node_id=0, parent=None):
        members = {} if members is None else members
        terminal_indices = [] if terminal_indices is None else terminal_indices
        self.choices = choices
        self.members = members
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


class Split(object):
    def __init__(self, index, splits, chi, p):
        self.index = index
        self.splits = splits
        self.chi = chi
        self.p = p


class MappingDict(dict):
    def __missing__(self, key):
        value = self[key] = [key]
        return value


class CHAID(object):

    def __init__(self, alpha_merge=0.05, max_depth=2, min_sample=30):
        self.alpha_merge = alpha_merge
        self.max_depth = max_depth
        self.min_sample = min_sample
        self.tree_store = []
        self.data_size = None
        self.independent_variable_names = []
        self.node_count = 0

    @staticmethod
    def fill_data_frame(data_frame):
        if data_frame.dtype == object:
            data_frame.fillna('-1.0', inplace=True)
        else:
            data_frame.fillna(-1.0, inplace=True)

    @staticmethod
    def from_pandas_df(ind_df, dep_series, alpha_merge=0.05, max_depth=2, min_sample=30):
        tree = CHAID(alpha_merge, max_depth, min_sample)
        tree.independent_variable_names = ind_df.columns
        ind_df.apply(tree.fill_data_frame)
        ind_values = ind_df.values
        dep_values = dep_series.values
        tree.data_size = dep_values.shape[0]
        tree.node(np.arange(0, tree.data_size + 1, dtype=np.int), ind_values, dep_values)
        return tree

    def node(self, rows, ind, dep, depth=0, parent=None, parent_decisions=None):
        depth = depth + 1

        members = dict(np.transpose(np.unique(dep, return_counts=True)))

        if self.max_depth < depth:
            terminal_node = CHAIDNode(choices=parent_decisions, members=members, node_id=self.node_count, parent=parent, terminal_indices=rows)
            self.tree_store.append(terminal_node)
            self.node_count += 1
            return self.tree_store

        split = self.generate_best_split(ind, dep)

        node = CHAIDNode(choices=parent_decisions, members=members, node_id=self.node_count, parent=parent, split_variable=split.index, chi=split.chi, p=split.p)
        self.tree_store.append(node)
        parent = self.node_count
        self.node_count += 1

        if split.index is None:
            return self.tree_store

        for choices in split.splits:
            correct_rows = np.in1d(ind[:, split.index], choices)
            dep_slice = dep[correct_rows]
            ind_slice = ind[correct_rows, :]
            row_slice = rows[correct_rows]
            if self.min_sample < len(dep_slice):
                self.node(row_slice, ind_slice, dep_slice, depth=depth, parent=parent, parent_decisions=choices)
            else:
                memebers = dict(np.transpose(np.unique(dep_slice, return_counts=True)))
                terminal_node = CHAIDNode(choices=choices, members=memebers, node_id=self.node_count, parent=parent, terminal_indices=row_slice)
                self.tree_store.append(terminal_node)
                self.node_count += 1
        return self.tree_store

    def generate_best_split(self, ind, dep):
        split = Split(None, None, None, 1)
        for i in range(0, ind.shape[1]):
            index = np.array(ind[:, i])
            unique = set(index)

            mappings = MappingDict()
            frequincies = {}
            for col in unique:
                counts = np.unique(dep[index == col][0], return_counts=True)
                frequincies[col] = cl.defaultdict(int)
                frequincies[col].update(np.transpose(counts))

            while len(unique) > 1:
                size = (len(unique) * (len(unique) - 1)) / 2
                sub_data = np.ndarray(shape=(size, 3), dtype=object, order='F')
                for j, comb in enumerate(it.combinations(unique, 2)):
                    y = frequincies[comb[0]]
                    g = frequincies[comb[1]]

                    keys = set(y.keys() + g.keys())

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
                        responces = [mappings[x] for x in unique]
                        chi = sub_data[correct_row][1]
                        split = Split(i, responces, chi, highest_p_split)
                    break

                choice = list(sub_data[correct_row, 0])

                if choice[1] in mappings:
                    mappings[choice[0]] += mappings[choice[1]]
                    del mappings[choice[1]]
                else:
                    mappings[choice[0]] += [choice[1]]

                index[index == choice[1]] = choice[0]
                unique.remove(choice[1])

                for val, count in frequincies[choice[1]].items():
                    frequincies[choice[0]][val] += count
                del frequincies[choice[1]]

        return split

    def to_tree(self):
        tree = Tree()
        for node in self.tree_store:
            tree.create_node(node, node.node_id, parent=node.parent)
        return tree

    def print_tree(self):
        self.to_tree().show()

    def predict(self):
        pred = np.zeros(self.data_size)
        for node in self.tree_store:
            pred[node.terminal_indices] = node.node_id
        return pred

    def __repr__(self):
        return str(self.tree_store)
