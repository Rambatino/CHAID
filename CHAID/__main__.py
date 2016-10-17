"""
This package provides a python implementation of the Chi-Squared Automatic
Inference Detection (CHAID) decision tree.
"""
import argparse
import savReaderWriter as spss
from .tree import Tree
import pandas as pd

def main():
    """Entry point when module is run from command line"""

    parser = argparse.ArgumentParser(description='Run the chaid algorithm on a'
                                     ' csv/sav file.')
    parser.add_argument('file')
    parser.add_argument('dependent_variable', nargs=1)
    parser.add_argument('independent_variables', nargs='+')
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
                       'input with the value of the  dependent varaible that '
                       'the majority of respondents in that node selected')
    nspace = parser.parse_args()

    data = pd.read_csv(nspace.file)

    # raw_data = spss.SavReader(nspace.file, returnHeader = True, rawMode=True)
    # raw_data_list = list(raw_data)
    # data = pd.DataFrame(raw_data_list)
    # data = data.rename(columns=data.loc[0]).iloc[1:]

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
    tree = Tree.from_pandas_df(data, nspace.independent_variables,
                                nspace.dependent_variable[0], **config)

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
    else:
        tree.print_tree()


if __name__ == "__main__":
    main()
