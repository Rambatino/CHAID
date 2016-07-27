
.. code:: python

    import numpy as np
    male = 0
    female = 1
    a = 0
    b = 1
    c = 2
    gender = np.array([0,0,0,1,0,0,1,1,0,0,1])
    income = np.array([0,0,1,0,2,0,1,2,1,0,1])
    weighting = np.array([0.9,0.8,0.9,1.1,1.2,0.8,1.3,0.2,0.5,0.7,1.1])

.. code:: python

    total_gender = np.transpose(np.unique(gender, return_counts=True))
    total_gender




.. parsed-literal::

    array([[0, 7],
           [1, 4]])



.. code:: python

    total_income = np.transpose(np.unique(income, return_counts=True))
    total_income




.. parsed-literal::

    array([[0, 5],
           [1, 4],
           [2, 2]])



.. code:: python

    gender_keys = np.unique(gender)
    n_ij = np.array([
            np.unique(income[np.where(gender == x)], return_counts=True)[1]
            for x in gender_keys
    ])
    n_ij




.. parsed-literal::

    array([[4, 2, 1],
           [1, 2, 1]])



.. code:: python

    gender_keys = np.unique(gender)
    x = 0
    weighting[gender == x][income[gender == x] == 0]




.. parsed-literal::

    array([ 0.9,  0.8,  0.8,  0.7])



.. code:: python

    gender_keys = np.unique(gender)
    income_keys = np.unique(income)
    w_ij = np.array(
        [
                [
                    weighting[gender == x][income[gender == x] == y].sum()
                    for y in income_keys
                ]
            for x in gender_keys
        ]
    )
    w_ij




.. parsed-literal::

    array([[ 3.2,  1.4,  1.2],
           [ 1.1,  2.4,  0.2]])



.. code:: python

    w_ij_1 = n_ij / w_ij
    w_ij_1




.. parsed-literal::

    array([[ 1.25      ,  1.42857143,  0.83333333],
           [ 0.90909091,  0.83333333,  5.        ]])



.. code:: python

    k = 0
    a = np.array([1,1])
    b = np.array([1,1,1])
    m_ij = w_ij_1
    
    new_a = (n_ij.sum(axis=1) * a) / m_ij.sum(axis=1)
    new_b = n_ij.sum(axis=0) / (m_ij * np.vstack(new_a)).sum(axis=0)
    m_ij_1 = m_ij
    m_ij = m_ij * np.vstack(new_a) * new_b
    m_ij




.. parsed-literal::

    array([[ 4.11027333,  3.40825165,  0.71791917],
           [ 0.88972667,  0.59174835,  1.28208083]])



.. code:: python

    max = np.max(np.absolute(m_ij - m_ij_1))
    max




.. parsed-literal::

    3.7179191703020824



.. code:: python

    while max > 0.0000001:
        new_a = (n_ij.sum(axis=1) * new_a) / m_ij.sum(axis=1)
        new_b = n_ij.sum(axis=0) / (w_ij_1 * np.vstack(new_a)).sum(axis=0)
        m_ij_1 = m_ij
        m_ij = w_ij_1 * np.vstack(new_a) * new_b
        max = np.max(np.absolute(m_ij - m_ij_1))

.. code:: python

    m_ij = w_ij_1 * np.vstack(new_a) * new_b
    m_ij




.. parsed-literal::

    array([[ 3.540006  ,  3.00570902,  0.454285  ],
           [ 1.459994  ,  0.99429098,  1.545715  ]])



.. code:: python

    from scipy import stats

.. code:: python

    exp = ( np.vstack(n_ij.sum(axis=1)) * n_ij.sum(axis=0) ) / n_ij.sum().astype(float)
    exp




.. parsed-literal::

    array([[ 3.18181818,  2.54545455,  1.27272727],
           [ 1.81818182,  1.45454545,  0.72727273]])



.. code:: python

    chi_square = (n_ij - exp)**2 / exp
    chi_square




.. parsed-literal::

    array([[ 0.21038961,  0.11688312,  0.05844156],
           [ 0.36818182,  0.20454545,  0.10227273]])



.. code:: python

    dof = (n_ij.shape[0] - 1) * (n_ij.shape[1] - 1)
    dof




.. parsed-literal::

    2



.. code:: python

    chisquare = stats.chisquare(n_ij, f_exp=m_ij, ddof= n_ij.size - 1 - dof, axis=None)
    chisquare




.. parsed-literal::

    Power_divergenceResult(statistic=2.4066797881947619, pvalue=0.30018993316754855)



The p-value of the weighted Chi-Square is 0.30018993316754855
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

