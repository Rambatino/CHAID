import itertools as it
import pandas as pd
from scipy import stats
import numpy as np
import collections as cl
from treelib import Node, Tree

class Node(object):
	def __init__(self, choices=None, members={}, split_variable=None, chi=0, p=0, terminal_indices=[], id=0, parent=None):
		self.choices = choices
		self.members = members
		self.split_variable = split_variable
		self.chi = chi
		self.p = p			
		self.terminal_indices = terminal_indices
		self.id = id
		self.parent = parent

	def __hash__(self):
		return self.__dict__

	def __eq__(self, other):
		if isinstance(other, self.__class__):
		    return self.__dict__ == other.__dict__
		else:
		    return False

	def __repr__(self):
		return str((self.choices, self.members, self.split_variable, self.chi, self.p))


class Split(object):
	def __init__(self, index, splits, chi, p):
		self.index = index
		self.splits = splits
		self.chi = chi
		self.p = p


class CHAID(object):
	DEFAULT_CONDITIONS =  { 'alpha_merge': .05, 'max_depth': 2, 'min_sample': 30 }	

	def from_pandas_df(self, ind_df, dep_series, conditions):
		new_conditions = self.DEFAULT_CONDITIONS.copy()
		new_conditions.update(conditions)
		params = {
			'independent_variable_names': ind_df.columns
		}
		ind_df.apply(lambda x: x.fillna('-1.0', inplace=True) if (x.dtype == object) else x.fillna(-1.0, inplace=True))
		ind_values = ind_df.values
		dep_values = dep_series.values
		self.data_size = dep_values.shape[0]
		self.tree_data, node_id =  self.node(params, np.arange(0, dep_values.shape[0] + 1, dtype=np.int), ind_values, dep_values, new_conditions)
		return self

	def node(self, params, rows, ind, dep, conditions, depth=0, tree_store=[], parent=None, node_id=0, parent_decisions=None):
		depth = depth + 1

		members = dict(np.transpose(np.unique(dep, return_counts=True)))

		if conditions['max_depth'] < depth:
			terminal_node = Node(choices=parent_decisions, members=members, id=node_id, parent=parent, terminal_indices=rows)
			tree_store.append(terminal_node)
			return tree_store, node_id + 1

		split = self.generate_best_split(ind, dep, conditions)

		node = Node(choices=parent_decisions, members=members, id=node_id, parent=parent, split_variable=split.index, chi=split.chi, p=split.p)
		tree_store.append(node)
		parent = node_id
		node_id = node_id + 1

		if split.index is None:
			return tree_store, node_id

		for choices in split.splits:
			correct_rows = np.in1d(ind[:, split.index], choices)
			dep_slice = dep[correct_rows]
			ind_slice = ind[correct_rows, :]
			row_slice = rows[correct_rows]
			if conditions['min_sample'] < len(dep_slice):
				tree_store, node_id = self.node(params, row_slice, ind_slice, dep_slice, conditions, depth, node_id=node_id, parent=parent, tree_store=tree_store, parent_decisions=choices)
			else:
				memebers = dict(np.transpose(np.unique(dep_slice, return_counts=True)))
				terminal_node = Node(choices=choices, members=memebers, id=node_id, parent=parent, terminal_indices=row_slice)
				tree_store.append(terminal_node)
				node_id = node_id + 1

		return tree_store, node_id

	def generate_best_split(self, ind, dep, conditions):
		split = Split(None, None, None, 1)
		for i in range(0, ind.shape[1]):
			index = np.array(ind[:,i])
			unique = set(index)

			mappings = {}
			frequincies = dict([ (col, dict(np.transpose(np.unique(dep[np.where(np.in1d(index, col))[0]], return_counts=True)))) for col in unique])

			while len(unique) > 1:
				size  = (len(unique) * (len(unique) - 1)) / 2
				sub_data = np.ndarray(shape=(size, 3), dtype=object, order='F')
				for j, comb in enumerate(it.combinations(unique, 2)):
					y = frequincies[comb[0]]
					g = frequincies[comb[1]]

					keys = set(y.keys() + g.keys())

					cr_table = [
						[ y.get(k, 0) for k in keys],
						[ g.get(k, 0) for k in keys]
					]

					chi = stats.chi2_contingency(np.array(cr_table))
					sub_data[j] = (comb, chi[0], chi[1])

				highest_p_split = np.sort(sub_data[:, 2])[-1]
				correct_row = np.where(np.in1d(sub_data[:, 2], highest_p_split))[0][0]

				if size == 1 or highest_p_split < conditions['alpha_merge']:
					if highest_p_split < split.p:
						split = Split(i, [ mappings.get(x, [x]) for x in unique ], sub_data[correct_row][1], highest_p_split)
					break

				choice = list(sub_data[correct_row, 0])

				if choice[1] in mappings:
					mappings[choice[0]] =  mappings.get(choice[0], [choice[0]]) + mappings[choice[1]]
					del mappings[choice[1]]
				else:
					mappings[choice[0]] = mappings.get(choice[0], [choice[0]]) + [choice[1]]

				index[ index == choice[1] ] = choice[0]
				unique.remove(choice[1])

				for val, count in frequincies[choice[1]].items():
					frequincies[choice[0]][val] = frequincies[choice[0]].get(val, 0) + count
				del frequincies[choice[1]]

		return split

	def to_tree(self):
		tree = Tree()
		for node in self.tree_data:
			tree.create_node(node, node.id, parent=node.parent)
		return tree

	def print_tree(self):
		self.to_tree().show()

	def predict(self):
		pred = np.zeros(self.data_size)
		for node in self.tree_data:
			pred[node.terminal_indices] = node.id
		return pred

	def __repr__(self):
		 return str(self.tree_data)


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='Run the chaid algorithm on a csv file.')
	parser.add_argument('file')
	parser.add_argument('dependent_variable', nargs=1)
	parser.add_argument('independent_variables', nargs='+')

	parser.add_argument('--max-depth', type=int, help='Max depth of generated tree')
	parser.add_argument('--min-samples', type=int, help='Minimum number of samples required to split node')
	parser.add_argument('--alpha-merge', type=float, help='Alpha Merge')
	nspace = parser.parse_args()

	df = pd.read_csv(nspace.file)
	dep_series = df[nspace.dependent_variable]
	ind_df = df[nspace.independent_variables]

	config = {}
	if nspace.max_depth:
		config['max_depth'] = nspace.max_depth
	if nspace.alpha_merge:
		config['alpha_merge'] = nspace.alpha_merge
	if nspace.min_samples:
		config['min_sample'] = nspace.min_samples
	CHAID().from_pandas_df(ind_df, dep_series, config).print_tree()
