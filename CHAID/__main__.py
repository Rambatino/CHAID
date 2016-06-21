import argparse
import pandas as pd
from CHAID import CHAID


def main():
    """Entry point when module is run from command line"""
    parser = argparse.ArgumentParser(description='Run the chaid algorithm on a csv file.')
    parser.add_argument('--csv')
    parser.add_argument('--dependent-variable', help='The name of the dependent variable')
    parser.add_argument('--independent-variables', nargs='+', help='The names of the independent variables')
    parser.add_argument('--independent-variable-types', nargs='+', 
        help='The types of independent variables. Defaults to nominal (categorical)')
    parser.add_argument('--dependent-variable-type', 
        help='The type of dependent variable. Defult is nominal (categorical)')
    parser.add_argument('--max-depth', type=int, help='Max depth of generated tree')
    parser.add_argument('--min-samples', type=int, help='Minimum number of samples required to split node')
    parser.add_argument('--alpha-merge', type=float, help='Alpha Merge')
    nspace = parser.parse_args()
    df = pd.read_csv(nspace.csv)

    config = {}
    if nspace.max_depth:
        config['max_depth'] = nspace.max_depth
    if nspace.alpha_merge:
        config['alpha_merge'] = nspace.alpha_merge
    if nspace.min_samples:
        config['min_sample'] = nspace.min_samples
    if nspace.independent_variable_types:
        config['independent_variable_types'] = nspace.independent_variable_types
    if nspace.dependent_variable_type:
        config['dependent_variable_type'] = nspace.dependent_variable_type
    CHAID.from_pandas_df(df, nspace.independent_variables, nspace.dependent_variable, **config).print_tree()


if __name__ == "__main__":
    main()
