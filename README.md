<img src="https://img.shields.io/pypi/pyversions/pytest.svg">
<img src="https://circleci.com/gh/Rambatino/CHAID.png?style=shield&circle-token=031aab51ad1dea4a698d02f02288887f06c1a9ef">


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

import CHAID from CHAID

pandas_data_frame = ...
independent_variable_columns = ['a', 'b', 'c']
dep_variable = ['d']
CHAID.from_pandas_df(df, independent_variable_columns, dep_variable)
```
Running from the Command Line
-----------------------------

You can play around with the repo by cloning and running this from the command line:

```
python -m CHAID tests/data/titanic.csv survived sex embarked --max-depth 4 --min-samples 2 --alpha-merge 0.05
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

Testing
-------

CHAID uses [`pytest`](https://pypi.python.org/pypi/pytest) for its unit testing. The tests can be run from the root of a checkout with:
``` bash
py.test
```
