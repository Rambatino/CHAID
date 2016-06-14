import itertools as it
import pandas as pd
from scipy import stats
import numpy as np
import collections as cl
from treelib import Node, Tree

DEFAULT_CONDITIONS =  {
	'alpha_merge': .05,
	'max_depth': 2,
	'min_sample': 30
}	

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


def conditions_merged(conditions):
	new_conditions = DEFAULT_CONDITIONS.copy()
	new_conditions.update(conditions)
	return new_conditions

def chaid(ind_df, dep_series, conditions):
	new_conditions = conditions_merged(conditions)
	params = {
		'independent_variable_names': ind_df.columns
	}
	ind_df.apply(lambda x: x.fillna('-1.0', inplace=True) if (x.dtype == object) else x.fillna(-1.0, inplace=True))
	ind_values = ind_df.values
	dep_values = dep_series.values
	tree, node_id =  chaid_node(params, np.arange(0, dep_values.shape[0] + 1, dtype=np.int), ind_values, dep_values, new_conditions)
	return tree

def chaid_node(params, rows, ind, dep, conditions, depth=0, tree_store=[], parent=None, node_id=0, parent_decisions=None):
	depth = depth + 1

	uni = dict(np.transpose(np.unique(dep, return_counts=True)))

	if conditions['max_depth'] < depth:
		terminal_node = Node(choices=parent_decisions, members=uni, id=node_id, parent=parent, terminal_indices=rows)
		tree_store.append(terminal_node)
		return tree_store, node_id + 1

	split_variable, split_keys, chi, p = generate_best_split(ind, dep, conditions)

	node = Node(choices=parent_decisions, members=uni, id=node_id, parent=parent, split_variable=split_variable, chi=chi, p=p)
	tree_store.append(node)
	parent = node_id
	node_id = node_id + 1

	if split_variable is None:
		return tree_store, node_id

	for choices in split_keys:
		correct_rows = np.in1d(ind[:, split_variable], choices)
		dep_slice = dep[correct_rows]
		ind_slice = ind[correct_rows, :]
		row_slice = rows[correct_rows]
		if conditions['min_sample'] < len(dep_slice):
			tree_store, node_id = chaid_node(params, row_slice, ind_slice, dep_slice, conditions, depth, node_id=node_id, parent=parent, tree_store=tree_store, parent_decisions=choices)
		else:
			uni = dict(np.transpose(np.unique(dep_slice, return_counts=True)))
			terminal_node = Node(choices=choices, members=uni, id=node_id, parent=parent, terminal_indices=row_slice)
			tree_store.append(terminal_node)
			node_id = node_id + 1

	return tree_store, node_id

def generate_best_split(ind, dep, conditions):
	most_sig_ind = (None, None, None, 1)
	for i in range(0, ind.shape[1]):
		index = np.array(ind[:,i])
		unique = set(index)

		mappings = {}

		while len(unique) > 1:
			size  = (len(unique) * (len(unique) - 1)) / 2
			sub_data = np.ndarray(shape=(size, 3), dtype=object, order='F')
			for j, comb in enumerate(it.combinations(unique, 2)):
				y = np.where(np.in1d(index, comb[0]))[0]
				g = np.where(np.in1d(index, comb[1]))[0]

				uni_y = dict(np.transpose(np.unique(dep[y], return_counts=True)))
				uni_g = dict(np.transpose(np.unique(dep[g], return_counts=True)))

				keys = set(uni_y.keys() + uni_g.keys())

				cr_table = [
					[ uni_y.get(k, 0) for k in keys],
					[ uni_g.get(k, 0) for k in keys]
				]

				chi = stats.chi2_contingency(np.array(cr_table))
				sub_data[j] = (comb, chi[0], chi[1])

			highest_p_split = np.sort(sub_data[:, 2])[-1]
			correct_row = np.where(np.in1d(sub_data[:, 2], highest_p_split))[0][0]

			if size == 1 or highest_p_split < conditions['alpha_merge']:
				if highest_p_split < most_sig_ind[3]:
					most_sig_ind = (i, [ mappings.get(x, [x]) for x in unique ], sub_data[correct_row][1], highest_p_split)
				break

			split = list(sub_data[correct_row, 0])

			if split[1] in mappings:
				mappings[split[0]] =  mappings.get(split[0], [split[0]]) + mappings[split[1]]
				del mappings[split[1]]
			else:
				mappings[split[0]] = mappings.get(split[0], [split[0]]) + [split[1]]

			index[ index == split[1] ] = split[0]
			unique.remove(split[1])

	return most_sig_ind

def to_tree(tree_data):
	tree = Tree()
	for node in tree_data:
		tree.create_node(node, node.id, parent=node.parent)
	return tree

def model_prediction(tree_data, length):
	pred = np.zeros(length)
	for node in tree_data:
		pred[node.terminal_indices] = node.id
	return pred

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
	to_tree(chaid(ind_df, dep_series, config)).show()
