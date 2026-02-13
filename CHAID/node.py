from .split import Split
from .column import ContinuousColumn
import numpy as np


def convert_to_python_type(value):
    """
    Convert numpy scalar types to Python native types.
    This ensures compatibility with numpy >= 2.0.0 where numpy scalars
    are preserved in operations like np.unique().

    Parameters
    ----------
    value : any
        The value to convert (may be a numpy scalar or Python native type)

    Returns
    -------
    The value converted to a Python native type if it was a numpy scalar,
    otherwise the original value
    """
    if hasattr(value, 'item'):
        # numpy scalars have an item() method that returns the Python scalar
        return value.item()
    return value


class Node(object):
    """
    A node in the CHAID tree

    Parameters
    ----------
    choices : array-like
        Contains a list of the splits that gave rise to that node
    split_variable : number or string
        A value indicating what independent variable the node derived from
    score : float
        The score for the split
    p : float
        The p-value for the split
    indices : array-like or None
        The row index that ended up in the node (only occurs in terminal nodes)
    node_id : float
        A float representing the id of the node
    parent : float or None
        The node_id of the parent of that node
    dep_v : array-like
        The dependent variable set
    is_terminal : boolean
        Whether the node is terminal
    """
    def __init__(self, choices=None, split=None, indices=None, node_id=0, parent=None, dep_v=None):
        indices = [] if indices is None else indices
        self.choices = list(choices or [])
        self.split = split or Split(None, None, None, None, 0)
        self.indices = indices
        self.node_id = node_id
        self.parent = parent
        self.dep_v = dep_v
        self._members = None

    def __hash__(self):
        return hash(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        format_str = u'({0.choices}, {0.members}, {0.split})'
        return format_str.format(self)

    def __lt__(self, other):
        return self.node_id < other.node_id

    @property
    def score(self):
        return self.split.score

    @property
    def p(self):
        return self.split.p

    @property
    def split_variable(self):
        return self.split.column

    @property
    def is_terminal(self):
        return not self.split.valid()

    @property
    def members(self):
        if self._members is None:
            dep_v = self.dep_v
            if isinstance(dep_v, ContinuousColumn):
                self._members = {
                    'mean': convert_to_python_type(self.dep_v.arr.mean()),
                    's.t.d': convert_to_python_type(self.dep_v.arr.std())
                }
            else:
                metadata = dep_v.metadata
                self._members = {}
                for member in metadata.values():
                    self._members[convert_to_python_type(member)] = 0

                if dep_v.weights is None:
                    counts = np.transpose(np.unique(dep_v.arr, return_counts=True))
                else:
                    counts = np.array([
                        [i, dep_v.weights[dep_v.arr == i].sum()] for i in set(dep_v.arr)
                    ])

                self._members.update(
                    (convert_to_python_type(metadata[k]), convert_to_python_type(v))
                    for k, v in counts
                )

        return self._members
