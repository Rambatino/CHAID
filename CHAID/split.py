class Split(object):
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
