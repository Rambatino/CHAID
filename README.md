# CHAID
A python implementation of the common CHAID algorithm

## Installing

Install the package using:

```
pip install CHAID
```

## Usage

Currently the only use case is running the CHAID algorithm on a respondent-level (pandas)[https://github.com/pydata/pandas] dataframe. Defining which are the independent variables and which is the dependent variable along with some tree growing conditions is all that is necessary.

After installing the package it can be used like so:

``` python
ipdb> config
{'alpha_merge': 0.05, 'min_sample': 2, 'max_depth': 2}


ipdb> ind_df.head(n=10)
                                       Q14b  Q15              Q15b Q15x  \
0                                       (3)  (4)  probably not (2)  (2)
1  Does not describe the company at all (1)  (3)               NaN  (2)
2                                       (2)  (3)               NaN  (2)
3                                       (4)  (4)  probably not (2)  (4)
4                                       (4)  (4)  probably not (2)  (4)
5                                       (4)  (4)               NaN  (4)
6                                       (5)  (5)      probably (4)  (5)
7                                       (4)  (4)  probably not (2)  (4)
8                                       (4)  (4)      probably (4)  (3)
9                                       (4)  (4)               NaN  (3)

  q16_001          q16_002          q16_003          q16_005          q16_006         
0            yes             no             no             no             no
1            NaN            NaN            NaN            NaN            NaN
2            NaN            NaN            NaN            NaN            NaN
3             no             no             no             no             no
4             no             no             no             no             no
5            NaN            NaN            NaN            NaN            NaN
6            yes            yes            yes            yes            yes
7             no             no             no             no             no
8            yes             no            yes             no             no
9            NaN            NaN            NaN            NaN            NaN


ipdb> dep_series.head(n=10)
   loves_chocolate
0             1
1             1
2             1
3             1
4             1
5             1
6             2
7             1
8             2
9             1


ipdb> CHAID().from_pandas_df(ind_df, dep_series, config).print_tree()
(None, {1.0: 126803.0, 2.0: 79286.0}, 1, 449.77801448767661, 8.0616844894670792e-100)
├── (['(3)'], {1.0: 24987.0, 2.0: 1776.0}, 0, 32.71862390124268, 1.0651178345362606e-08)
│   ├── (['(6)', 'Describes the company perfectly (7)'], {1.0: 192.0, 2.0: 179.0}, None, 0, 0)
│   ├── (['Does not describe the company at all (1)', '(3)', '(2)'], {1.0: 16983.0, 2.0: 436.0}, None, 0, 0)
│   ├── (['(5)'], {1.0: 1057.0, 2.0: 504.0}, None, 0, 0)
│   └── (['(4)', '-1.0'], {1.0: 6755.0, 2.0: 657.0}, None, 0, 0)
├── (['Does not describe the company at all (1)', '(2)'], {1.0: 31724.0, 2.0: 969.0}, 5, 611.29756842520374, 5.8415188001114804e-135)
│   ├── (['-1.0', 'no'], {1.0: 31138.0, 2.0: 836.0}, None, 0, 0)
│   └── (['yes'], {1.0: 586.0, 2.0: 133.0}, None, 0, 0)
├── (['(6)'], {1.0: 4627.0, 2.0: 26762.0}, 4, 768.19026834017575, 4.4488201139125303e-169)
│   ├── (['-1.0', 'no'], {1.0: 4124.0, 2.0: 18563.0}, None, 0, 0)
│   └── (['yes'], {1.0: 503.0, 2.0: 8199.0}, None, 0, 0)
├── (['(5)', '-1.0'], {1.0: 16060.0, 2.0: 23836.0}, 0, 136.4309803213948, 1.6060004981823772e-31)
│   ├── (['(6)', '-1.0', 'Describes the company perfectly (7)'], {1.0: 1086.0, 2.0: 4799.0}, None, 0, 0)
│   ├── (['Does not describe the company at all (1)', '(3)', '(2)'], {1.0: 1516.0, 2.0: 364.0}, None, 0, 0)
│   ├── (['(5)'], {1.0: 6591.0, 2.0: 15302.0}, None, 0, 0)
│   └── (['(4)'], {1.0: 6867.0, 2.0: 3371.0}, None, 0, 0)
├── (['(4)'], {1.0: 48083.0, 2.0: 8685.0}, 0, 48.642879985856638, 3.0708112865511942e-12)
│   ├── (['(6)', 'Describes the company perfectly (7)'], {1.0: 684.0, 2.0: 1029.0}, None, 0, 0)
│   ├── (['Does not describe the company at all (1)', '(3)', '(2)'], {1.0: 7143.0, 2.0: 564.0}, None, 0, 0)
│   ├── (['(5)', '-1.0'], {1.0: 4618.0, 2.0: 3191.0}, None, 0, 0)
│   └── (['(4)'], {1.0: 35638.0, 2.0: 3901.0}, None, 0, 0)
└── (['Describes the company perfectly (7)'], {1.0: 1322.0, 2.0: 17258.0}, 8, 305.50020959228249, 2.0868755309384378e-68)
    ├── (['-1.0', 'no'], {1.0: 856.0, 2.0: 6921.0}, None, 0, 0)
    └── (['yes'], {1.0: 466.0, 2.0: 10337.0}, None, 0, 0)
```