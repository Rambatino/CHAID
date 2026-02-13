<img src="https://img.shields.io/pypi/v/CHAID.svg"> <img src="https://img.shields.io/pypi/dm/chaid.svg?maxAge=2592000&label=installs&color=%2327B1FF"> <img src="https://img.shields.io/pypi/pyversions/CHAID.svg"> <img src="https://github.com/Rambatino/CHAID/actions/workflows/tests.yml/badge.svg"> <a href="https://codecov.io/gh/Rambatino/CHAID"><img src="https://codecov.io/gh/Rambatino/CHAID/branch/master/graph/badge.svg" alt="Codecov" /></a>

# CHAID — Chi-Squared Automatic Interaction Detection

A Python implementation of the [Chi-Squared Automatic Interaction Detection (CHAID)](https://en.wikipedia.org/wiki/CHAID) decision tree, including support for [Exhaustive CHAID](https://github.com/Rambatino/CHAID/issues/112).

CHAID is a statistical method for segmentation and classification. It builds decision trees by repeatedly splitting a dataset based on the independent variable that has the strongest interaction with the dependent variable, as measured by the chi-squared statistic (for categorical targets) or Bartlett's/Levene's test (for continuous targets).

## Features

- **Categorical & continuous** dependent variables
- **Nominal & ordinal** independent variable types
- **Exhaustive CHAID** — evaluates all possible merges at each step for more thorough splitting
- **Weighted observations** — supports a weight column for survey data
- **Missing value handling** — automatically groups `NaN` values into a `<missing>` category
- **Predictions & classification** — assign observations to terminal nodes or predict the modal/mean outcome
- **Tree visualisation** — render publication-quality tree diagrams via Graphviz and Plotly
- **CLI interface** — build trees directly from CSV or SPSS `.sav` files

## Installation

CHAID requires **Python 3.9+** and is distributed via [PyPI](https://pypi.python.org/pypi/CHAID):

```bash
pip install CHAID
```

### Optional extras

```bash
pip install CHAID[graph]   # Tree visualisation (graphviz, plotly, kaleido)
pip install CHAID[spss]    # SPSS .sav file support (savReaderWriter)
pip install CHAID[graph,spss]  # Both
```

> **Note:** The `graph` extra also requires the [Graphviz system package](https://graphviz.org/download/) to be installed on your machine (e.g. `brew install graphviz` on macOS or `sudo apt-get install graphviz` on Debian/Ubuntu).

## Quick Start

```python
from CHAID import Tree
import pandas as pd
import numpy as np

# Create sample data
ndarr = np.array(([1, 2, 3] * 5) + ([2, 2, 3] * 5)).reshape(10, 3)
df = pd.DataFrame(ndarr, columns=['a', 'b', 'c'])
df['d'] = np.array(([1] * 5) + ([2] * 5))

>>> df
   a  b  c  d
0  1  2  3  1
1  1  2  3  1
2  1  2  3  1
3  1  2  3  1
4  1  2  3  1
5  2  2  3  2
6  2  2  3  2
7  2  2  3  2
8  2  2  3  2
9  2  2  3  2
```

### Building a tree

There are three ways to construct a tree:

```python
from CHAID import Tree, NominalColumn

# 1. From a pandas DataFrame
tree = Tree.from_pandas_df(df, dict(a='nominal', b='nominal', c='nominal'), 'd')

# 2. From numpy arrays
tree = Tree.from_numpy(ndarr, arr, split_titles=['a', 'b', 'c'], min_child_node_size=5)

# 3. Using the Tree constructor directly
cols = [
    NominalColumn(ndarr[:,0], name='a'),
    NominalColumn(ndarr[:,1], name='b'),
    NominalColumn(ndarr[:,2], name='c')
]
tree = Tree(cols, NominalColumn(arr, name='d'), {'min_child_node_size': 5})
```

```python
>>> tree.print_tree()
([], {1: 5, 2: 5}, ('a', p=0.001565402258, score=10.0, groups=[[1], [2]]), dof=1))
├── ([1], {1: 5, 2: 0}, <Invalid Chaid Split>)
└── ([2], {1: 0, 2: 5}, <Invalid Chaid Split>)
```

### Accessing nodes and splits

```python
root = tree.tree_store[0]

>>> root.members
{1: 5, 2: 5}

>>> root.split.column
'a'
>>> root.split.p
0.001565402258002549
>>> root.split.score
10.0
>>> root.split.dof
1

# Get a treelib Tree object
>>> tree.to_tree()
<treelib.tree.Tree object at 0x114e2e350>
```

## Continuous Dependent Variables

When the dependent variable is continuous, the chi-squared test is replaced with [Bartlett's test](https://en.wikipedia.org/wiki/Bartlett%27s_test) (for normally distributed data) or [Levene's test](https://en.wikipedia.org/wiki/Levene%27s_test) (for non-normal data). The test is selected automatically based on the distribution of the dependent variable.

```python
df['d'] = np.random.normal(300, 100, 10)

tree = Tree.from_pandas_df(
    df,
    dict(a='nominal', b='nominal', c='nominal'),
    'd',
    dep_variable_type='continuous'
)

>>> tree.print_tree()
([], {'s.t.d': 86.562258585515579, 'mean': 297.52027436303212}, <Invalid Chaid Split>)
```

Node members for continuous targets show the mean and standard deviation instead of category frequencies. Any `NaN` values in the dependent variable are automatically converted to `0.0`.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `alpha_merge` | `float` | `0.05` | Significance threshold for merging predictor categories. If the test for a pair of categories is not significant at this level, the least significant pair is merged. |
| `max_depth` | `int` | `2` | Maximum depth of the tree. |
| `min_parent_node_size` | `int` or `float` | `30` | Minimum number of observations required for a node to be split. Values between 0 and 1 are treated as fractions of the total dataset size. |
| `min_child_node_size` | `int` or `float` | `30` | Minimum number of observations in a child node. Child nodes below this threshold are merged with the most similar sibling. If only one child would remain, the split is cancelled. Values between 0 and 1 are treated as fractions. |
| `max_splits` | `int` or `None` | `None` | Maximum number of child nodes per split. If set, categories continue merging until at most this many groups remain. |
| `split_threshold` | `float` | `0` | Threshold for surrogate split selection. |
| `weight` | `str` or `None` | `None` | Column name to use as observation weights. |
| `dep_variable_type` | `str` | `'categorical'` | `'categorical'` or `'continuous'`. |
| `is_exhaustive` | `bool` | `False` | Whether to use Exhaustive CHAID, which evaluates all possible category merges at each step. |

## Classification Rules

Extract the decision path for each terminal node:

```python
>>> tree.classification_rules()
[
    {'node': 2, 'rules': [{'variable': 'sex', 'data': ['female']}, {'variable': 'embarked', 'data': ['C']}]},
    {'node': 3, 'rules': [{'variable': 'sex', 'data': ['male']}, {'variable': 'embarked', 'data': ['C']}]},
    ...
]
```

## Tree Visualisation

Install the `graph` extra and the [Graphviz system package](https://graphviz.org/download/), then:

```python
tree.render(path='my_tree', view=False)
```

This generates a `.gv` file and a `.png` at the specified path.

![](https://github.com/Rambatino/CHAID/blob/master/docs/2019-04-01%2011:45:43.gv.png?raw=true "CHAID Tree")

### Exporting to DOT format

```python
treelib_tree = tree.to_tree()
treelib_tree.to_graphviz()
```

## Command-Line Interface

CHAID can be run directly from the terminal on CSV or SPSS `.sav` files:

```bash
python -m CHAID <file> <dependent_var> <nominal_vars...> [options]
```

### Examples

```bash
# Basic tree
python -m CHAID tests/data/titanic.csv survived sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05

# Continuous dependent variable
python -m CHAID tests/data/titanic.csv fare sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05 \
    --dependent-variable-type continuous

# Export classification rules
python -m CHAID tests/data/titanic.csv survived sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05 --rules

# Export tree visualisation
python -m CHAID tests/data/titanic.csv survived sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05 --export

# Exhaustive CHAID
python -m CHAID tests/data/titanic.csv survived sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05 --exhaustive
```

Run `python -m CHAID -h` for the full list of options.

## How to Read the Tree

Using the Titanic dataset as an example:

```
python -m CHAID tests/data/titanic.csv survived sex embarked \
    --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05
```

```
([], {0: 809, 1: 500}, (sex, p=1.47e-81, score=365.89, groups=[['female'], ['male']]), dof=1))
├── (['female'], {0: 127, 1: 339}, (embarked, p=9.18e-07, score=24.09, groups=[['C', '<missing>'], ['Q', 'S']]), dof=1))
│   ├── (['C', '<missing>'], {0: 11, 1: 104}, <Invalid Chaid Split>)
│   └── (['Q', 'S'], {0: 116, 1: 235}, <Invalid Chaid Split>)
└── (['male'], {0: 682, 1: 161}, (embarked, p=5.02e-05, score=16.44, groups=[['C'], ['Q', 'S']]), dof=1))
    ├── (['C'], {0: 109, 1: 48}, <Invalid Chaid Split>)
    └── (['Q', 'S'], {0: 573, 1: 113}, <Invalid Chaid Split>)
```

Each node displays:

1. **Choices** — the categories from the parent split that lead to this node (e.g. `['female']`)
2. **Members** — the frequency distribution of the dependent variable (e.g. `{0: 127, 1: 339}`)
3. **Split** — the variable chosen for further splitting, its p-value, test score, group assignments, and degrees of freedom
4. **`<Invalid Chaid Split>`** — the node is terminal (either pure, or a stopping criterion was met)

**Interpretation:** Gender was the strongest predictor of survival on the Titanic. Females had a much higher survival rate. Among females, those who embarked in first class (class `'C'`) had the highest survival rate.

## Caveats

- Unlike SPSS, this library does not modify data internally — weight variables are not rounded.
- Every row is included in the analysis, even if all independent variable values are `NaN`. In SPSS, such rows are excluded in the weighted case.

## Testing

```bash
pip install -e '.[test]'
pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/Rambatino/CHAID).

## License

Apache License 2.0 — see [LICENSE.txt](LICENSE.txt) for details.
