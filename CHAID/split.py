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
    score : float
        The score value of that split
    p : float
        The p value of that split
    dof : int
        The degrees of freedom as a result of this split
    invalid_reason : InvalidSplitReason()
        The reason why the node failed to split
    """
    def __init__(self, column, splits, score, p, dof, invalid_reason=None, split_name=None):
        """
        Initialize the splits.

        Args:
            self: (todo): write your description
            column: (list): write your description
            splits: (todo): write your description
            score: (todo): write your description
            p: (int): write your description
            dof: (int): write your description
            invalid_reason: (str): write your description
            split_name: (str): write your description
        """
        splits = splits or []
        self.surrogates = []
        self.column_id = column
        self.split_name = split_name
        self.splits = list(splits)
        self.split_map = [None] * len(self.splits)
        self.score = score
        self.p = p
        self._dof = dof
        self._invalid_reason = invalid_reason

    def sub_split_values(self, sub):
        """ Substitutes the splits with other values into the split_map """
        for i, arr in enumerate(self.splits):
            self.split_map[i] = [sub.get(x, x) for x in arr]
        for split in self.surrogates:
            split.sub_split_values(sub)

    def name_columns(self, sub):
        """ Substitutes the split column index with a human readable string """
        if self.column_id is not None and len(sub) > self.column_id:
            self.split_name = sub[self.column_id]
        for split in self.surrogates:
            split.name_columns(sub)

    def __repr__(self):
        """
        Return a human - readable representation of this object.

        Args:
            self: (todo): write your description
        """
        if not self.valid():
            return '<Invalid Chaid Split> - {}'.format(self.invalid_reason)
        format_str = u'({0.column}, p={0.p}, score={0.score}, groups={0.groupings})'\
                     ', dof={0.dof})'
        return format_str.format(self)

    @property
    def column(self):
        """
        Returns the column name.

        Args:
            self: (todo): write your description
        """
        if not self.valid():
            return None
        return self.split_name or str(self.column_id)

    @property
    def groupings(self):
        """
        Return a list of groupings

        Args:
            self: (todo): write your description
        """
        if not self.valid():
            return "[]"
        if all(x is None for x in self.split_map):
            return str(self.splits)
        return str(self.split_map)

    @property
    def dof(self):
        """
        Dof of dof

        Args:
            self: (todo): write your description
        """
        return self._dof

    @property
    def invalid_reason(self):
        """
        Return the reason for the reason.

        Args:
            self: (todo): write your description
        """
        return self._invalid_reason

    @invalid_reason.setter
    def invalid_reason(self, value):
        """
        Set the reason for the given value.

        Args:
            self: (todo): write your description
            value: (todo): write your description
        """
        self._invalid_reason = value

    def valid(self):
        """
        Validate the validator.

        Args:
            self: (todo): write your description
        """
        return self.column_id is not None
