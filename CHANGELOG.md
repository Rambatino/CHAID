<h2>__A python implementation of Chi-Squared Automatic Interaction Detection (CHAID)__</h2>

###  3.0.0 (2017-03-20)

- Enabled continuous dependent variables to be passed through CHAID using Bartlett's and Levene's tests
  ([af3e3b1](https://github.com/Rambatino/CHAID/commit/af3e3b15aa9c14995526916be50f7b61a8d4cd27))

- Min Child Node Size now defaults to 30
  ([ba5545e](https://github.com/Rambatino/CHAID/commit/ba5545e2929d7555817f8f53babad9cb2731e138))

- Added codecov to PRs
  ([2cf68d9](https://github.com/Rambatino/CHAID/commit/2cf68d94ca9162c92f43ab1bc8ed50db6758fccc))

- Removed Node's `is_terminal` constructor key and created the property via a decorator based on the split object it contains
  ([07b0830](https://github.com/Rambatino/CHAID/commit/07b0830e106ad0aee5e9930e6647ae150867b02d))

- Added method to return the classification rules of the tree or node
  ([70290f2](https://github.com/Rambatino/CHAID/commit/70290f2b6613fd2ba92efef27bb6a717d6a6ce18))

###  2.1.0 (2016-08-17)

- Added min child node size
  ([54e805b](https://github.com/Rambatino/CHAID/commit/54e805b8d044c1aa2d3b2fbbc4b3395659170812))

###  2.0.0 (2016-08-27)

- Refactored and renamed classes
  ([994fdaf](https://github.com/Rambatino/CHAID/commit/994fdaf7919e7ff047b0458c1bd0d38aa82f3b21))

- Renamed min_sample to min_parent_node_size
  ([ee474f2](https://github.com/Rambatino/CHAID/commit/ee474f26837f666b326d2a7c39969db388e99e66))

###  1.0.1 (2016-08-25)

- fixed weighting slice to slice on the sliced version, rather than the original
  ([e6ff0b4](https://github.com/Rambatino/CHAID/commit/e6ff0b4e0782eafda7fda55c9cb860746de59e2a))

---

### Bug Fixes

- fixed truth value of terminal indices ndarray
  ([a2d0cff7](https://github.com/Rambatino/CHAID/commit/a2d0cff7e0546bf1b52375eab8c6a466e055f591))


### Features

- Add version to CHAID python module. (#33)
  ([586c9a95](https://github.com/Rambatino/CHAID/commit/586c9a954aa36014b1568cbaa526f8fbb9146e49))
