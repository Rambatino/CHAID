# CHAID review — 2026-10-03

## Request and scope

User prompt: "https://github.com/Rambatino/CHAID find any issues performance
optimisations and improvements and create a PR"

Reviewed published master at `9ba2361` in an isolated worktree. Existing local
changes in statistics code and tests were not included. The target repository
has no PLAN.md, PROGRESS.md or additional agent instructions.

## Findings and changes

- Nominal encoding overwrote original values with category IDs, then matched
  subsequent categories against the modified array. `[-1, 0, 1]` became
  `[2, 2, 2]`, silently corrupting predictors and outcomes.
- Encoding into the input dtype also truncated multi-digit IDs in one-character
  string arrays and overflowed narrow integers. Numeric string labels could
  collide with IDs as well.
- Replaced repeated replacement passes with NumPy inverse indices in a separate
  float64 array. Sorted IDs remain unchanged for comparable values; mixed types
  now receive deterministic first-occurrence IDs instead of set iteration order.
  Missing values keep code -1 and the existing missing-value label.
- Ordinal encoding relied on casting NaN to an integer sentinel. On this ARM
  machine it yielded zero, breaking 12 existing tests that CI deselected.
  Assign the int64 sentinel explicitly, including the custom-metadata path;
  restore all tests in CI and check conversion with invalid operations raised.
- Repeated `build_tree()` calls retained the old node counter, invalidating
  node lookup and classification rules. Reset it for every rebuild.
- A fresh graph-extra installation selected Plotly 7.1.0 with Kaleido 0.2.1,
  causing rendering to fail. Constrain Plotly to `<7`, consistent with the
  existing Kaleido `<1` constraint. Plotly documents the removal of legacy
  Kaleido support in https://plotly.com/python/static-image-generation-changes/.

## Verification

- Before fixes, the non-rendering baseline had 79 passes and 12 ordinal failures.
  The initial new nominal/tree regression cases produced 12 failures and 5 passes
  against the original implementation. The weighted fixture was then adjusted
  to avoid zero contingency cells and exercise the library's weighted statistic.
- Fresh isolated Python 3.13.3 environment: `pip install -e '.[test,graph]'`.
  Resolved NumPy 2.5.3, Plotly 6.9.0 and Kaleido 0.2.1; Graphviz 16.1.0 installed.
- `python -m pytest --cov=CHAID/ -q`: **113 passed**, 84% overall coverage,
  including real graph rendering. There are 15 legacy rendering deprecation
  warnings. No tests are skipped or deselected by the workflow.
- `python -m pip check`: no broken requirements.
- Titanic CLI classification-rule example completed successfully.
- 400 randomized nominal round-trips passed across integer, floating-point,
  string and object arrays, using seed 13.
- `git diff --check`: passed.
- Added 21 regression cases covering encoding, missing values, weighted and
  unweighted model predictions, and repeated tree rebuilds.

## Encoding benchmark

100,000 integer rows, NumPy RNG seed 42, five runs per case, minimum elapsed time
for constructing a complete NominalColumn. Compared this branch with the class
loaded from `git show 9ba2361:CHAID/column.py` in the same Python process.
Values were sampled with `rng.integers(100000, 100000 + categories, size=100000)`;
encoded arrays and metadata were asserted identical before timing.

| Categories | Before | After | Before / after |
|---|---:|---:|---:|
| 10 | 2.87 ms | 3.70 ms | 0.77x |
| 100 | 8.03 ms | 5.72 ms | 1.40x |
| 1,000 | 52.01 ms | 8.14 ms | 6.39x |
| 5,000 | 243.14 ms | 11.76 ms | 20.67x |

The former encoding makes one full-array replacement pass per category. The new
path sorts once and uses inverse indices. It trades some low-cardinality overhead
and temporary arrays for correct encoding and better high-cardinality scaling.
These measurements concern column construction, not total tree fitting time.

## Remaining work and observability

- GitHub's Python 3.9–3.13 matrix must verify the published commit; only Python
  3.13 was run locally. No release or deployment is part of this change.
- Migrating graph rendering to Kaleido 1 and its browser requirement is separate
  work; the compatible legacy pair still emits deprecation warnings.
- Other review findings left outside this patch: continuous `model_predictions`
  returns a ValueError object instead of raising, and setup classifiers/tox
  versions do not match the supported Python matrix.
- This is an in-process statistics library with no service metrics or Grafana
  integration. Regression tests, decoded values, classification rules, CI output
  and the benchmark expose the affected behavior; no runtime logging was added.
