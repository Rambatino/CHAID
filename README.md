<img src="https://img.shields.io/pypi/pyversions/pytest.svg">
<img src="https://circleci.com/gh/Rambatino/CHAID.png?style=shield&circle-token=031aab51ad1dea4a698d02f02288887f06c1a9ef">
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/7400e498230e4df6b7aa00d4064c5f93/badge.svg)](https://www.quantifiedcode.com/app/project/7400e498230e4df6b7aa00d4064c5f93)


Chi-Squared Automatic Inference Detection
=========================================

This package provides a python implementation of the [Chi-Squared Automatic Inference Detection (CHAID) decision tree](https://en.wikipedia.org/wiki/CHAID)


Installation
------------

CHAID is distributed via [pypi](https://pypi.python.org/pypi/CHAID) and can be installed like:

``` bash
pip install CHAID
```

Alternatively, you can clone the repository and install via
``` bash
pip install -e path/to/your/checkout
```

Creating a Tree
---------------

``` python

from CHAID import Tree

pandas_data_frame = ...
independent_variable_columns = ['a', 'b', 'c']
dep_variable = 'd'
Tree.from_pandas_df(df, independent_variable_columns, dep_variable)
```
Parameters
----------
* `df`: Pandas DataFrame
* `i_variables: Array<string>`: Independent variable column names
* `d_variable: String`: Dependent variable column name
* `opts: {}`:
  * `alpha_merge: Float (default = 0.05)`: If the respective test for a given pair of predictor categories is not statistically significant as defined by an `alpha_merge` value, the least significant predictor categories are merged and the splitting of the node is attempted with the newly formed categories
  * `max_depth: Integer (default = 2)`: The maximum depth of the tree
  * `min_parent_node_size: Float (default = 30)`: The minimum number of respondents required for a split to occur on the parent node
  * `min_child_node_size: Float (default = 0)`: All child nodes must have at least this number of respondents for a split to occur
  * `split_threshold: Float (default = 0)`: The split threshold when bucketing root node surrogate splits
  * `weight: String (default = None)`: The name of the weight column

Running from the Command Line
-----------------------------

You can play around with the repo by cloning and running this from the command line:

```
python -m CHAID tests/data/titanic.csv survived sex embarked --max-depth 4 --min-parent-node-size 2 --alpha-merge 0.05
```

It calls the `print_tree()` method, which prints the tree to terminal:

```
([], {0: 809, 1: 500}, (sex, p=1.47145310169e-81, chi=365.886947811, groups=[['female'], ['male']]))
├── (['female'], {0: 127, 1: 339}, (embarked, p=9.17624191599e-07, chi=24.0936494474, groups=[['C', '<missing>'], ['Q', 'S']]))
│   ├── (['C', '<missing>'], {0: 11, 1: 104}, <Invalid Chaid Split>)
│   └── (['Q', 'S'], {0: 116, 1: 235}, <Invalid Chaid Split>)
└── (['male'], {0: 682, 1: 161}, (embarked, p=5.017855245e-05, chi=16.4413525404, groups=[['C'], ['Q', 'S']]))
    ├── (['C'], {0: 109, 1: 48}, <Invalid Chaid Split>)
    └── (['Q', 'S'], {0: 573, 1: 113}, <Invalid Chaid Split>)
```
To get a LibTree object, call to_tree() on the CHAID instance
Parameters
----------
Run `python -m CHAID -h` to see description of command line arguments

Testing
-------

CHAID uses [`pytest`](https://pypi.python.org/pypi/pytest) for its unit testing. The tests can be run from the root of a checkout with:
``` bash
py.test
```

Caveats
-------

* Unlike SPSS, this library doesn't modify the data internally. This means that weight variables aren't rounded as they are in SPSS.
* Every row is valid, even if all values are NaN or undefined. This is different to SPSS where in the weighted case it will strip out all rows if all the independent variables are NaN
* All columns are currently treated as nominal


Upcoming Features
-------

* Splitting Rules (under development)
* Accuracy Estimation using Machine Learning techniques on the data
* Allow both ordinal and nominal columns (under development)
* Allow continuous dependent variable which uses the F-test
* Binning of continuous independent variables
