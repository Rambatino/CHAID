"""
This package provides a python implementation of the Chi-Squared Automatic
Inference Detection (CHAID) decision tree.
"""
import argparse
import savReaderWriter as spss
from .tree import Tree
import pandas as pd
import numpy as np


def main():
    """Entry point when module is run from command line"""

    parser = argparse.ArgumentParser(description='Run the chaid algorithm on a'
                                     ' csv/sav file.')
    parser.add_argument('file')
    parser.add_argument('dependent_variable', nargs=1)
    parser.add_argument('--dependent-variable-type', type=str)

    var = parser.add_argument_group('Independent Variable Specification')
    var.add_argument('nominal_variables', nargs='*', help='The names of '
                     'independent variables to use that have no intrinsic '
                     'order to them')
    var.add_argument('--ordinal-variables', type=str, nargs='*',
                     help='The names of independent variables to use that '
                     'have an intrinsic order but a finite amount of states')
    parser.add_argument('--weights', type=str, help='Name of weight column')

    parser.add_argument('--max-depth', type=int, help='Max depth of generated '
                        'tree')
    parser.add_argument('--min-parent-node-size', type=int, help='Minimum number of '
                        'samples required to split the parent node')
    parser.add_argument('--min-child-node-size', type=int, help='Minimum number of '
                        'samples required to split the child node')
    parser.add_argument('--alpha-merge', type=float, help='Alpha Merge')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--classify', action='store_true', help='Add column to'
                       ' input with the node id of the node that that '
                       'respondent has been placed into')
    group.add_argument('--predict', action='store_true', help='Add column to '
                       'input with the value of the  dependent variable that '
                       'the majority of respondents in that node selected')
    group.add_argument('--rules', action='store_true')


    nspace = parser.parse_args()

    if nspace.file[-4:] == '.csv':
        data = pd.read_csv(nspace.file)
    elif nspace.file[-4:] == '.sav':
        raw_data = spss.SavReader(nspace.file, returnHeader=True)
        raw_data_list = list(raw_data)
        data = pd.DataFrame(raw_data_list)
        data = data.rename(columns=data.loc[0]).iloc[1:]
    else:
        print('Unknown file type')
        exit(1)

    config = {}
    if nspace.max_depth:
        config['max_depth'] = nspace.max_depth
    if nspace.alpha_merge:
        config['alpha_merge'] = nspace.alpha_merge
    if nspace.min_parent_node_size:
        config['min_parent_node_size'] = nspace.min_parent_node_size
    if nspace.min_child_node_size:
        config['min_child_node_size'] = nspace.min_child_node_size
    if nspace.weights:
        config['weight'] = nspace.weights
    if nspace.dependent_variable_type:
        config['dep_variable_type'] = nspace.dependent_variable_type


    ordinal = nspace.ordinal_variables or []
    nominal = nspace.nominal_variables or []
    independent_variables = nominal + ordinal
    types = dict(zip(nominal + ordinal, ['nominal'] * len(nominal) + ['ordinal'] * len(ordinal)))
    if len(independent_variables) == 0:
        print('Need to provide at least one independent variable')
        exit(1)
    tree = Tree.from_pandas_df(data, types, nspace.dependent_variable[0],
                               **config)

    if nspace.classify:
        predictions = pd.Series(tree.node_predictions())
        predictions.name = 'node_id'
        data = pd.concat([data, predictions], axis=1)
        print(data.to_csv())
    elif nspace.predict:
        predictions = pd.Series(tree.model_predictions())
        predictions.name = 'predicted'
        data = pd.concat([data, predictions], axis=1)
        print(data.to_csv())
    elif nspace.rules:
        print('\n'.join(str(x) for x in tree.classification_rules()))
    else:
        tree.print_tree()


if __name__ == "__main__":
    main()
