import argparse
import pandas as pd
from CHAID import CHAID


def main():
    """Entry point when module is run from command line"""

    parser = argparse.ArgumentParser(description='Run the chaid algorithm on a csv file.')
    parser.add_argument('file')
    parser.add_argument('dependent_variable', nargs=1)
    parser.add_argument('independent_variables', nargs='+')

    parser.add_argument('--max-depth', type=int, help='Max depth of generated tree')
    parser.add_argument('--min-samples', type=int, help='Minimum number of samples required to split node')
    parser.add_argument('--alpha-merge', type=float, help='Alpha Merge')
    nspace = parser.parse_args()

    df = pd.read_csv(nspace.file)

    config = {}
    if nspace.max_depth:
        config['max_depth'] = nspace.max_depth
    if nspace.alpha_merge:
        config['alpha_merge'] = nspace.alpha_merge
    if nspace.min_samples:
        config['min_sample'] = nspace.min_samples
    CHAID.from_pandas_df(df, nspace.independent_variables, nspace.dependent_variable[0], **config).print_tree()


if __name__ == "__main__":
    main()
