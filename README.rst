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
------------

.. code-block:: python
	
	import CHAID from CHAID

	pandas_data_frame = ...
	independent_variable_columns = ['a', 'b', 'c']
	dep_variable = ['d']
	CHAID.from_pandas_df(df, independent_variable_columns, dep_variable).print_tree()

.. _here: http://www.python.org/
.. _pypi: https://pypi.python.org/pypi/CHAID