import collections as cl
from .column import ContinuousColumn
from .split import Split
import numpy as np
from scipy import stats
from .invalid_split_reason import InvalidSplitReason
from numpy import nan as NaN

def chisquare(n_ij, weighted):
    """
    Calculates the chisquare for a matrix of ind_v x dep_v
    for the unweighted and SPSS weighted case
    """
    if weighted:
        m_ij = n_ij / n_ij

        nan_mask = np.isnan(m_ij)
        m_ij[nan_mask] = 0.000001  # otherwise it breaks the chi-squared test

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


class Stats(object):
    """
    Stats class that determines the correct statistical method to apply
    """
    def __init__(self, alpha_merge, min_child_node_size, split_threshold, dep_population, is_exhaustive=False):
        self.split_threshold = 1 - split_threshold
        self.alpha_merge = alpha_merge
        self.min_child_node_size = min_child_node_size
        self.dep_population = dep_population
        self.is_exhaustive = is_exhaustive

    def best_split(self, ind, dep):
        """ determine which splitting function to apply """
        if isinstance(dep, ContinuousColumn):
            return self.best_con_split(ind, dep)
        else:
            return self.best_cat_heuristic_split(ind, dep)

    def best_cat_heuristic_split(self, ind, dep):
        """ determine best categorical variable split using heuristic methods """
        split = Split(None, None, None, None, 0)
        min_child_node_size = self.min_child_node_size

        all_dep = np.unique(dep.arr)
        if len(all_dep) == 1:
            split.invalid_reason = InvalidSplitReason.PURE_NODE
            return split
        elif len(dep.arr) < min_child_node_size and dep.weights is None:
            # if not weights and too small, skip
            split.invalid_reason = InvalidSplitReason.MIN_CHILD_NODE_SIZE
            return split
        elif dep.weights is not None and len(dep.weights) < min_child_node_size:
            # if weighted count is too small, skip
            split.invalid_reason = InvalidSplitReason.PURE_NODE
            return split

        for i, ind_var in enumerate(ind):
            split.invalid_reason = None # must reset because using invalid reason to break
            ind_var = ind_var.deep_copy()
            unique = np.unique(ind_var.arr)

            freq = {}
            if dep.weights is None:
                for col in unique:
                    counts = np.unique(np.compress(ind_var.arr == col, dep.arr), return_counts=True)
                    freq[col] = cl.defaultdict(int)
                    freq[col].update(np.transpose(counts))
            else:
                for col in unique:
                    counts = np.unique(np.compress(ind_var.arr == col, dep.arr), return_counts=True)
                    freq[col] = cl.defaultdict(int)
                    for dep_v in all_dep:
                        freq[col][dep_v] = dep.weights[(ind_var.arr == col) * (dep.arr == dep_v)].sum()


            if dep.weights is not None:
                row_count = dep.weights.sum()
            else:
                row_count = len(dep.arr)

            if len(list(ind_var.possible_groupings())) == 0:
                split.invalid_reason = InvalidSplitReason.PURE_NODE
            while next(ind_var.possible_groupings(), None) is not None:
                choice, highest_p_join, split_chi = None, None, None

                for comb in ind_var.possible_groupings():
                    col1_freq = freq[comb[0]]
                    col2_freq = freq[comb[1]]

                    keys = set(col1_freq.keys()).union(col2_freq.keys())
                    n_ij = np.array([
                        [col1_freq.get(k, 0) for k in keys],
                        [col2_freq.get(k, 0) for k in keys]
                    ])

                    # check to see if min_child_node_size permits this direction
                    # 31 can't merge with 10 if it only leaves 27 for the other node(s)
                    # but if these are the only two, can't skip, because the level can be defined
                    # as these two nodes
                    other_splits = row_count - n_ij.sum()
                    if other_splits < min_child_node_size and other_splits != 0:
                        p_split, dof, chi = 1, NaN, NaN
                        continue

                    if n_ij.shape[1] == 1:
                        p_split, dof, chi = 1, NaN, NaN
                        # could be the only valid combination, as we skip
                        # ones that result in other nodes that give min child node sizes
                        # this solves [[20], [10, 11]] even though 10 & 11 are exact,
                        # this must be the choice of this iteration
                        choice = comb
                        break
                    else:
                        chi, p_split, dof = chisquare(n_ij, dep.weights is not None)

                    if choice is None or p_split > highest_p_join or (p_split == highest_p_join and chi > split_chi):
                        choice, highest_p_join, split_chi = comb, p_split, chi

                sufficient_split = not highest_p_join or highest_p_join < self.alpha_merge
                if not sufficient_split:
                  split.invalid_reason = InvalidSplitReason.ALPHA_MERGE
                elif (n_ij.sum(axis=1) < min_child_node_size).any():
                  split.invalid_reason = InvalidSplitReason.MIN_CHILD_NODE_SIZE
                elif self.is_exhaustive and len(freq.values()) > 2:
                  split.invalid_reason = InvalidSplitReason.NODE_NOT_EXHAUSTIVE
                else:
                    n_ij = np.array([
                        [f[dep_val] for dep_val in all_dep] for f in freq.values()
                    ])

                    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
                    chi, p_split, dof = chisquare(n_ij, dep.weights is not None)

                    temp_split = Split(i, ind_var.groups(), chi, p_split, dof, split_name=ind_var.name)
                    better_split = not split.valid() or p_split < split.p or (p_split == split.p and chi > split.score)

                    if better_split:
                        split, temp_split = temp_split, split

                    chi_threshold = self.split_threshold * split.score

                    if temp_split.valid() and temp_split.score >= chi_threshold:
                        for sur in temp_split.surrogates:
                            if sur.column_id != i and sur.score >= chi_threshold:
                                split.surrogates.append(sur)

                        temp_split.surrogates = []
                        split.surrogates.append(temp_split)

                    break

                # all combinations created don't suffice. i.e. what's left is below min_child_node_size
                if choice is None:
                    break
                else:
                    ind_var.group(choice[0], choice[1])
                    for val, count in freq[choice[1]].items():
                        freq[choice[0]][val] += count
                    del freq[choice[1]]
        if split.valid():
            split.sub_split_values(ind[split.column_id].metadata)
        return split

    def best_con_split(self, ind, dep):
        """ determine best continuous variable split """
        split = Split(None, None, None, None, 0)
        is_normal = stats.normaltest(self.dep_population)[1] > 0.05
        sig_test = stats.bartlett if is_normal else stats.levene
        response_set = dep.arr
        if dep.weights is not None:
            response_set = dep.arr * dep.weights

        for i, ind_var in enumerate(ind):
            ind_var = ind_var.deep_copy()
            unique = np.unique(ind_var.arr)
            keyed_set = {}

            for col in unique:
                matched_elements = np.compress(ind_var.arr == col, response_set)
                keyed_set[col] = matched_elements

            while next(ind_var.possible_groupings(), None) is not None:
                choice, highest_p_join, split_score = None, None, None
                for comb in ind_var.possible_groupings():
                    col1_keyed_set = keyed_set[comb[0]]
                    col2_keyed_set = keyed_set[comb[1]]
                    dof = len(np.concatenate((col1_keyed_set, col2_keyed_set))) - 2
                    score, p_split = sig_test(col1_keyed_set, col2_keyed_set)

                    if choice is None or p_split > highest_p_join or (p_split == highest_p_join and score > split_score):
                        choice, highest_p_join, split_score = comb, p_split, score

                sufficient_split = highest_p_join < self.alpha_merge and all(
                    len(node_v) >= self.min_child_node_size for node_v in keyed_set.values()
                )

                invalid_reason = None
                sufficient_split = highest_p_join < self.alpha_merge
                if not sufficient_split: invalid_reason = InvalidSplitReason.ALPHA_MERGE

                sufficient_split = sufficient_split and all(
                    len(node_v) >= self.min_child_node_size for node_v in keyed_set.values()
                )
                
                if not sufficient_split: 
                    split.invalid_reason = InvalidSplitReason.MIN_CHILD_NODE_SIZE
                elif self.is_exhaustive and len(list(ind_var.possible_groupings())) != 1: 
                    invalid_reason = InvalidSplitReason.NODE_NOT_EXHAUSTIVE
                elif sufficient_split and len(keyed_set.values()) > 1:
                    dof = len(np.concatenate(list(keyed_set.values()))) - 2
                    score, p_split = sig_test(*keyed_set.values())

                    temp_split = Split(i, ind_var.groups(), score, p_split, dof, split_name=ind_var.name)

                    better_split = not split.valid() or p_split < split.p or (p_split == split.p and score > split.score)

                    if better_split:
                        split, temp_split = temp_split, split

                    score_threshold = self.split_threshold * split.score

                    if temp_split.valid() and temp_split.score >= score_threshold:
                        for sur in temp_split.surrogates:
                            if sur.column_id != i and sur.score >= score_threshold:
                                split.surrogates.append(sur)

                        temp_split.surrogates = []
                        split.surrogates.append(temp_split)

                    break
                else:
                    split.invalid_reason = invalid_reason

                ind_var.group(choice[0], choice[1])

                keyed_set[choice[0]] = np.concatenate((keyed_set[choice[1]], keyed_set[choice[0]]))
                del keyed_set[choice[1]]

        if split.valid():
            split.sub_split_values(ind[split.column_id].metadata)
        return split
