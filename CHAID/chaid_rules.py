import numpy as np
import pandas as pd

class CHAIDRules(object):
    """
    A class that manages the rules of a tree

    Parameters
    ----------
    tree : CHAIDTree
        a tree object
    """
    def __init__(self, tree):
        self._tree = tree

    def rules(self):
        """
        Calculates the row criteria that give rise
        to a particular terminal node
        """
        rules = pd.DataFrame()
        for node in self._tree:
            if node.is_terminal:
                sliced_arr = self._tree.independent_set[node.indices]
                unique_set = np.vstack({ tuple(row) for row in sliced_arr })
                index = pd.MultiIndex.from_arrays(np.transpose(unique_set))
                if rules.empty:
                    rules = pd.DataFrame([[node.node_id, node.predict]] * len(index), index=index)
                else:
                    rules = rules.append(pd.DataFrame([[node.node_id, node.predict]] * len(index), index=index))
        rules.columns = ['node_id', 'prediction']
        return rules

    def rules_predictions(self):
        assert False
        return 1
