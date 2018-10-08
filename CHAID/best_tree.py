from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from hyperopt import hp, tpe, fmin
from tqdm import tqdm
import pickle
from .tree import Tree


class BestTree(object):
    def __init__(self, ind, dep, n=100, split_titles=None, variable_types=None):
        """
        Finds the best tree, while preventing overfitting

        * only supports categorical dependent var
        """
        self.pbar = tqdm(total=n, desc="Finding best CHAID params")
        self.ind = ind
        self.dep = dep
        self.n = n
        self.split_titles = split_titles
        self.variable_types = variable_types

    def calculate(self):
        space = [
            ('Alpha Merge', hp.normal('alpha_merge', 0.3, 0.2)),
            ('Max Depth', hp.randint('max_depth', 10)),
            ('Min Parent Node Size', hp.randint('min_parent_node_size', 100)),
            ('Min Child Node Size', hp.randint('min_child_node_size', 100)),
        ]

        best = fmin(fn=lambda config: 1 - self.train(self.ind, self.dep, self.n, self.split_titles, self.variable_types, config),
            space=space,
            algo=tpe.suggest,
            max_evals=self.n)

        self.pbar.close()

        return best

    def train(self, ind, dep, n, split_titles, variable_types, conf):
        alpha_merge, max_depth, min_parent_node_size, min_child_node_size = conf
        accuracies = []
        for _ in range(0, n):
            X_train, X_test, Y_train, Y_test = train_test_split(ind, dep)
            tree = Tree.from_numpy(X_train, Y_train, alpha_merge=alpha_merge[1],
                min_child_node_size=min_child_node_size[1], max_depth=max_depth[1],
                variable_types=variable_types, split_titles=split_titles,
                min_parent_node_size=min_parent_node_size[1],
            )
            predictions = tree.predict(X_test)
            if predictions is None or np.isnan(predictions).any():
                continue
            acc = accuracy_score(Y_test, predictions)
            accuracies.append(acc)
        self.pbar.update()
        if len(accuracies) == 0:
            return 0
        return sum(accuracies) / float(len(accuracies))
