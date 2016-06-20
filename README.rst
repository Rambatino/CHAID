======================================== 
Chi-Squared Automatic Inference Detection
======================================== 

This package provides a python implementation of the Chi-Squared Automatic Inference Detection (CHAID) decision tree. More details can be found here_.


Installation
------------

CHAID is distributed via pypi_ and can be installed like:

.. code-block:: bash
	
	pip install CHAID


Creating a Tree
---------------

.. code-block:: python
	
	import CHAID from CHAID

	pandas_data_frame = ...
	independent_variable_columns = ['a', 'b', 'c']
	dep_variable = ['d']
	CHAID.from_pandas_df(df, independent_variable_columns, dep_variable)

Running from the Command Line
-----------------------------

You can play around with the repo by cloning and running this from the command line:

.. code-block:: bash

	python3 -m CHAID CHAID/data/CHAID.csv loves_chocolate Q14b Q Qb Qx qa_001 qa_002 qa_003 qa_005 qa_006 --max-depth 2 --min-samples 2 --alpha-merge 0.05

It calls the `print_tree()` method, which prints the tree to terminal:

.. code-block:: bash

	([], {'<missing>': 1.0, 1.0: 15560.0, 2.0: 9961.0}, Q14b, 4.5, 0.033894853524689295)
	├── (['-2', '-3', '-4', 'Does poort describe the company at all (1)'], {'<missing>': 1.0, 1.0: 12871.0, 2.0: 1605.0}, Q, 3.5555555555555554, 0.05934643879191998)
	│   ├── (['-2', '-3', '-4', '-5', 'Describes the company perfectly (7)', 'Does poort describe the company at all (1)'], {'<missing>': 1.0, 1.0: 12671.0, 2.0: 1428.0}, None, 0, 0)
	│   └── (['-6', '<missing>'], {1.0: 200.0, 2.0: 177.0}, None, 0, 0)
	└── (['-5', '-6', 'Describes the company perfectly (7)', '<missing>'], {1.0: 2689.0, 2.0: 8356.0}, Q, 4.5, 0.033894853524689295)
	    ├── (['-2', '-3', '-4', 'Does poort describe the company at all (1)'], {1.0: 1103.0, 2.0: 688.0}, None, 0, 0)
	    └── (['-5', '-6', 'Describes the company perfectly (7)', '<missing>'], {1.0: 1586.0, 2.0: 7668.0}, None, 0, 0

To get a LibTree object, call to_tree() on the CHAID instance

.. _here: http://www.python.org/
.. _pypi: https://en.wikipedia.org/wiki/CHAID