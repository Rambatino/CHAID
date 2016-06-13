import itertools as it
import pandas as pd
from scipy import stats
import numpy as np
import collections as cl
from treelib import Node, Tree
# df = pd.read_csv("/Users/Mark/CHAID.csv")
# ind_df = df[['Umsatz', 'V5001', 'V5002_1', 'V5002_2', 'V5002_3', 'V5002_4', 'V6001', 'V6002']]
# dep_series = df['titypv']
# from CHAID import CHAID
# CHAID.df_to_tree(ind_df, dep_series, {})

DEFAULT_CONDITIONS =  {
	'alpha_merge': 0.05,
	'max_depth': 3,
	'min_sample': 30
}	

def conditions_merged(conditions):
	new_conditions = DEFAULT_CONDITIONS.copy()
	new_conditions.update(conditions)
	return new_conditions

def df_to_tree(ind_df, dep_series, conditions):
	new_conditions = conditions_merged(conditions)
	params = {
		'independent_variable_names': ind_df.columns
	}
	ind_df = ind_df.fillna(-1.0)
	ind_values = ind_df.values
	dep_values = dep_series.values
	tree(params, ind_values, dep_values, new_conditions)
	return 1

def tree(params, ind, dep, conditions):
	split = generate_best_split(ind, dep, conditions)



	return 1


def generate_best_split(ind, dep, conditions):
	for i in range(0, ind.shape[1]):
		data = {}
		index = ind[:,i]
		unique = np.unique(index)
		unique_list = list(it.combinations(unique, 2))
		combs = np.array(list(it.combinations(unique, 2)))
		import ipdb; ipdb.set_trace()
		while True:
			sub_data = np.ndarray(shape=(len(combs), 3), dtype=object, order='F')
			for j, comb in enumerate(combs):
				y = np.where(np.in1d(index, comb[0]))[0]
				g = np.where(np.in1d(index, comb[1]))[0]
				uni_y = dict(np.transpose(np.unique(dep[y], return_counts=True)))
				uni_g = dict(np.transpose(np.unique(dep[g], return_counts=True)))
				diff_1 = set(uni_y.keys()) - set(uni_g.keys())
				uni_g.update(dict(map(lambda x: [x, 0], diff_1)))
				diff_2 = set(uni_g.keys()) - set(uni_y.keys())
				uni_y.update(dict(map(lambda x: [x, 0], diff_2)))
				chi = stats.chi2_contingency(np.array([uni_y.values(), uni_g.values()]))
				sub_data[j] = [comb, chi[0], chi[1]]
			highest_p_split = np.sort(sub_data[:,2])[-1]
			correct_row = np.where(np.in1d(sub_data[:,2], highest_p_split))[0][0]
			split = list(sub_data[correct_row, 0])
			if len(combs) == 1 or highest_p_split < conditions['alpha_merge']:
				data[str(i)] = sub_data
				break
			combs = combs.astype(object)
			drop = []
			for tt, aa in enumerate(combs): 
				substitute(aa, split)
				ff = np.where(np.in1d(aa, split))
				if len(ff[0]) == 1:
					combs[tt, ff[0][0]] = split
					if is_equal(combs[tt - 1], combs[tt]):
						drop.append(tt)
				elif len(ff[0]) == 2:
					drop.append(tt)
			combs = np.delete(combs, drop, 0)


	return 5


def flatten_list(ndarr):
	new_list = []
	# for sublist in ndarr:
	# 	if isinstance(sublist, list): 

	return 'lol'


def substitute(element_row, current_split):
	import ipdb; ipdb.set_trace()
	new_array = []
	for sublist in current_split:
		if isinstance(sublist, list):
			for item in sublist:
				new_array.append(item)
	# flattened_array = [item for sublist in current_split (for item in sublist if isinstance(item, list) else item)]
	for item in element_row:
		if isinstance(item, np.ndarray): 
			substitute(item, current_split)
		elif np.in1d(flattened_array, [item]).sum() == 1:
			element_row[np.where(np.in1d(flattened_array, [item]))[0][0]] = current_split
	return 50


	

# def find_index(arr_maj, arr_min):
# 	# if is_equal(arr_maj, arr_min): return []
# 	data = []
# 	import ipdb; ipdb.set_trace()
# 	for i, v in enumerate(arr_maj):
# 		if not isinstance(v, float): 
# 			data.append(i)
# 			index = find_index(v, arr_min)
# 			if index is not None:
# 				data.append(index)
# 		elif any(x == v for x in np.ndarray.flatten(np.array(arr_min))): return i ## need to not find both
# 	import ipdb; ipdb.set_trace()
# 	return data

def is_equal(arg1, arg2):
	truthy = True
	np_set = (np.ndarray)
	if isinstance(arg1, np_set) and isinstance(arg2, np_set):
		for i, v in enumerate(arg1):
			truthy = is_equal(v, arg2[i])
			if not truthy: return truthy 
	elif isinstance(arg1, float) and isinstance(arg2, float):
		if arg1 != arg2:
			return False
	else:
		return False
	return truthy