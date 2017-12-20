def best_cat_brute_force_split(self, ind, dep):
    """ determine best categorical variable split using brute force """
    split = Split(None, None, None, None, 0)
    all_dep = np.unique(dep.arr)
    for i, ind_var in enumerate(ind):
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

        if len(list(ind_var.possible_groupings())) == 0:
            split.invalid_reason = InvalidSplitReason.PURE_NODE

        choice, highest_p_join, split_chi, dof = None, None, None, None
        for comb in ind_var.all_combinations():
            freqs = [ sum( [ cl.Counter(freq[key]) for key in c ], cl.Counter()) for c in comb ]

            if sum([ (sum(x.values()) < self.min_child_node_size) for x in freqs ] ) > 0:
                continue
            keys = set(sum([ list(f.keys()) for f in freqs ], []))

            n_ij = np.array(
                [ [ col.get(k, 0) for k in keys ] for col in freqs ]
            )

            chi, p_split, dof = chisquare(n_ij, dep.weights is not None)

            if (choice is None or p_split < highest_p_join or (p_split == highest_p_join and chi > split_chi)) and p_split < self.alpha_merge:
                choice, highest_p_join, split_chi = comb, p_split, chi

        temp_split = Split(i, choice, split_chi, highest_p_join, dof, split_name=ind_var.name)
        better_split = (not split.valid() or p_split < split.p or (p_split == split.p and chi > split.score)) and choice is not None
        if better_split: split, temp_split = temp_split, split

        if split.valid() and choice is not None:
            chi_threshold = self.split_threshold * split.score

            if temp_split.valid() and temp_split.score >= chi_threshold:
                for sur in temp_split.surrogates:
                    if sur.column_id != i and sur.score >= chi_threshold:
                        split.surrogates.append(sur)

                temp_split.surrogates = []
                split.surrogates.append(temp_split)

            split.sub_split_values(ind[split.column_id].metadata)

    return split
