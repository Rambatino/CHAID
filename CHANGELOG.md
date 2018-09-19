# Change Log

## [v5.0.5](https://github.com/Rambatino/CHAID/tree/v5.0.5) (2018-09-19)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.4...v5.0.5)

**Fixed bugs:**

- Created passing unit test case for issue in \#87 [\#88](https://github.com/Rambatino/CHAID/pull/88) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- model\_predictions fails with categorical dependant variables [\#87](https://github.com/Rambatino/CHAID/issues/87)
- Couple questions [\#85](https://github.com/Rambatino/CHAID/issues/85)
- Why isn't there a predict function ? [\#72](https://github.com/Rambatino/CHAID/issues/72)

**Merged pull requests:**

- House keeping [\#86](https://github.com/Rambatino/CHAID/pull/86) ([Rambatino](https://github.com/Rambatino))

## [v5.0.4](https://github.com/Rambatino/CHAID/tree/v5.0.4) (2017-12-20)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.3...v5.0.4)

**Merged pull requests:**

- Reverted back heuristic approach [\#84](https://github.com/Rambatino/CHAID/pull/84) ([Rambatino](https://github.com/Rambatino))

## [v5.0.3](https://github.com/Rambatino/CHAID/tree/v5.0.3) (2017-09-29)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.2...v5.0.3)

**Fixed bugs:**

- Valid splits discounted when most significant split is generated below base size [\#81](https://github.com/Rambatino/CHAID/issues/81)
- Fixing minimum node sizes whereby combined choices aren't selected [\#83](https://github.com/Rambatino/CHAID/pull/83) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- Maybe an error in the doc? [\#79](https://github.com/Rambatino/CHAID/issues/79)

## [v5.0.2](https://github.com/Rambatino/CHAID/tree/v5.0.2) (2017-08-24)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.1...v5.0.2)

**Fixed bugs:**

- Specs and fix [\#78](https://github.com/Rambatino/CHAID/pull/78) ([Rambatino](https://github.com/Rambatino))

## [v5.0.1](https://github.com/Rambatino/CHAID/tree/v5.0.1) (2017-08-22)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.0...v5.0.1)

**Fixed bugs:**

- Fixed numpy for 1.11.1 [\#77](https://github.com/Rambatino/CHAID/pull/77) ([Rambatino](https://github.com/Rambatino))

## [v5.0.0](https://github.com/Rambatino/CHAID/tree/v5.0.0) (2017-08-21)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v4.0.0...v5.0.0)

**Implemented enhancements:**

- Formalised tree initialisation method to use Column classes [\#76](https://github.com/Rambatino/CHAID/pull/76) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- Continuous independent variables? [\#75](https://github.com/Rambatino/CHAID/issues/75)
- CHAID tree to json [\#71](https://github.com/Rambatino/CHAID/issues/71)
- Output Tree as pandas DataFrame [\#69](https://github.com/Rambatino/CHAID/issues/69)
- Basic clarifications [\#66](https://github.com/Rambatino/CHAID/issues/66)

**Merged pull requests:**

- First draft of the how to guide [\#67](https://github.com/Rambatino/CHAID/pull/67) ([Rambatino](https://github.com/Rambatino))

## [v4.0.0](https://github.com/Rambatino/CHAID/tree/v4.0.0) (2017-06-14)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v4.0.0-alpha.2...v4.0.0)

**Implemented enhancements:**

- Changed architecture of from\_pandas\_df to align variable types and instance variables into a single parameter [\#70](https://github.com/Rambatino/CHAID/pull/70) ([Rambatino](https://github.com/Rambatino))
- Adding invalid split messages [\#68](https://github.com/Rambatino/CHAID/pull/68) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- Creating tree different from README [\#65](https://github.com/Rambatino/CHAID/issues/65)
- any working example? [\#64](https://github.com/Rambatino/CHAID/issues/64)
- User shouldn't have to pass in variables and variable types [\#53](https://github.com/Rambatino/CHAID/issues/53)

## [v4.0.0-alpha.2](https://github.com/Rambatino/CHAID/tree/v4.0.0-alpha.2) (2017-06-07)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v4.0.0-alpha.1...v4.0.0-alpha.2)

**Fixed bugs:**

- Fix for printing unicode characters [\#63](https://github.com/Rambatino/CHAID/pull/63) ([Rambatino](https://github.com/Rambatino))
- Change version regex to allow for alpha versions [\#59](https://github.com/Rambatino/CHAID/pull/59) ([xulaus](https://github.com/xulaus))

## [v4.0.0-alpha.1](https://github.com/Rambatino/CHAID/tree/v4.0.0-alpha.1) (2017-05-04)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v3.0.0...v4.0.0-alpha.1)

**Implemented enhancements:**

- Switched chi to score in node [\#58](https://github.com/Rambatino/CHAID/pull/58) ([Rambatino](https://github.com/Rambatino))
- Increase Circle CI caching [\#56](https://github.com/Rambatino/CHAID/pull/56) ([Rambatino](https://github.com/Rambatino))
- Ignore setup.py and test files [\#55](https://github.com/Rambatino/CHAID/pull/55) ([Rambatino](https://github.com/Rambatino))
- Added codecov file [\#54](https://github.com/Rambatino/CHAID/pull/54) ([Rambatino](https://github.com/Rambatino))

**Fixed bugs:**

- Added Failing Python 3 Spec [\#57](https://github.com/Rambatino/CHAID/pull/57) ([Rambatino](https://github.com/Rambatino))

## [v3.0.0](https://github.com/Rambatino/CHAID/tree/v3.0.0) (2017-03-21)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v2.2.0...v3.0.0)

**Implemented enhancements:**

- Updated min\_child\_node\_size to default to 30 [\#49](https://github.com/Rambatino/CHAID/pull/49) ([Rambatino](https://github.com/Rambatino))
- Added Levene & Bartlett test for continuous dependent variables [\#48](https://github.com/Rambatino/CHAID/pull/48) ([Rambatino](https://github.com/Rambatino))
- Add classification rules to Tree [\#47](https://github.com/Rambatino/CHAID/pull/47) ([xulaus](https://github.com/xulaus))

**Fixed bugs:**

- Created is\_terminal property and removed setting it in the Node const… [\#50](https://github.com/Rambatino/CHAID/pull/50) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- min\_child\_node\_size defaults to None [\#44](https://github.com/Rambatino/CHAID/issues/44)
- test model performance on validation dataset [\#23](https://github.com/Rambatino/CHAID/issues/23)
- Use bin count instead of unique to get frequencies. [\#19](https://github.com/Rambatino/CHAID/issues/19)
- Unify CHAIDNode.is\_terminal and CHAIDSplit.valid\(\) [\#17](https://github.com/Rambatino/CHAID/issues/17)

**Merged pull requests:**

- Testing circle CI [\#51](https://github.com/Rambatino/CHAID/pull/51) ([Rambatino](https://github.com/Rambatino))

## [v2.2.0](https://github.com/Rambatino/CHAID/tree/v2.2.0) (2016-10-25)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v2.1.0...v2.2.0)

**Implemented enhancements:**

- Added python 3 to circle [\#46](https://github.com/Rambatino/CHAID/pull/46) ([Rambatino](https://github.com/Rambatino))
- Added ordinal variable type to independent variables [\#45](https://github.com/Rambatino/CHAID/pull/45) ([xulaus](https://github.com/xulaus))

## [v2.1.0](https://github.com/Rambatino/CHAID/tree/v2.1.0) (2016-10-17)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v2.0.0...v2.1.0)

**Implemented enhancements:**

- Added min\_child\_node\_sixe for both weighted and unweighted case [\#43](https://github.com/Rambatino/CHAID/pull/43) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- Add weighting for respondents. [\#35](https://github.com/Rambatino/CHAID/issues/35)

## [v2.0.0](https://github.com/Rambatino/CHAID/tree/v2.0.0) (2016-09-29)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v1.0.2...v2.0.0)

**Implemented enhancements:**

- Renamed min\_sample to min\_parent\_node\_size [\#42](https://github.com/Rambatino/CHAID/pull/42) ([Rambatino](https://github.com/Rambatino))

## [v1.0.2](https://github.com/Rambatino/CHAID/tree/v1.0.2) (2016-09-26)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v1.0.1...v1.0.2)

**Fixed bugs:**

- Hotfix/weight base size fix [\#40](https://github.com/Rambatino/CHAID/pull/40) ([Rambatino](https://github.com/Rambatino))

## [v1.0.1](https://github.com/Rambatino/CHAID/tree/v1.0.1) (2016-09-22)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v1.0.0...v1.0.1)

## [v1.0.0](https://github.com/Rambatino/CHAID/tree/v1.0.0) (2016-09-22)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.4...v1.0.0)

**Implemented enhancements:**

- Added SPSS weighting to the CHAID Algorithm [\#37](https://github.com/Rambatino/CHAID/pull/37) ([Rambatino](https://github.com/Rambatino))

## [v0.3.4](https://github.com/Rambatino/CHAID/tree/v0.3.4) (2016-07-27)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.3...v0.3.4)

## [v0.3.3](https://github.com/Rambatino/CHAID/tree/v0.3.3) (2016-07-25)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.2...v0.3.3)

**Merged pull requests:**

- Add version to CHAID python module. [\#33](https://github.com/Rambatino/CHAID/pull/33) ([xulaus](https://github.com/xulaus))

## [v0.3.2](https://github.com/Rambatino/CHAID/tree/v0.3.2) (2016-07-25)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.1...v0.3.2)

**Fixed bugs:**

- Ensure metadata for CHAIDVector contains all values, and all members … [\#32](https://github.com/Rambatino/CHAID/pull/32) ([xulaus](https://github.com/xulaus))
- Fix force splitting of nodes that should not be split [\#31](https://github.com/Rambatino/CHAID/pull/31) ([xulaus](https://github.com/xulaus))

## [v0.3.1](https://github.com/Rambatino/CHAID/tree/v0.3.1) (2016-07-14)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.0...v0.3.1)

**Merged pull requests:**

- Revert "Hotfix/numpy 1 9 feature removal" [\#28](https://github.com/Rambatino/CHAID/pull/28) ([Rambatino](https://github.com/Rambatino))

## [v0.3.0](https://github.com/Rambatino/CHAID/tree/v0.3.0) (2016-07-14)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.2.0...v0.3.0)

**Implemented enhancements:**

- Switched yates correction off to match spss [\#25](https://github.com/Rambatino/CHAID/pull/25) ([Rambatino](https://github.com/Rambatino))
- Add --classify command for command line tool [\#14](https://github.com/Rambatino/CHAID/pull/14) ([xulaus](https://github.com/xulaus))

**Fixed bugs:**

- Now checking for CHI as well due to 0.0 p-values being the same across multiple groupings [\#24](https://github.com/Rambatino/CHAID/pull/24) ([Rambatino](https://github.com/Rambatino))

**Merged pull requests:**

- Hotfix/numpy 1 9 feature removal [\#27](https://github.com/Rambatino/CHAID/pull/27) ([Rambatino](https://github.com/Rambatino))
- Fixed risk value calculation [\#26](https://github.com/Rambatino/CHAID/pull/26) ([Rambatino](https://github.com/Rambatino))

## [v0.2.0](https://github.com/Rambatino/CHAID/tree/v0.2.0) (2016-06-28)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.1.1...v0.2.0)

**Fixed bugs:**

- Remove surrogate split if column already has split. [\#18](https://github.com/Rambatino/CHAID/pull/18) ([xulaus](https://github.com/xulaus))

## [v0.1.1](https://github.com/Rambatino/CHAID/tree/v0.1.1) (2016-06-23)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/Rambatino/CHAID/tree/v0.1.0) (2016-06-23)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.11...v0.1.0)

**Implemented enhancements:**

- Added risk method [\#15](https://github.com/Rambatino/CHAID/pull/15) ([Rambatino](https://github.com/Rambatino))
- Maintain a list of surrogate splits [\#13](https://github.com/Rambatino/CHAID/pull/13) ([xulaus](https://github.com/xulaus))

## [v0.0.11](https://github.com/Rambatino/CHAID/tree/v0.0.11) (2016-06-22)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.10...v0.0.11)

**Implemented enhancements:**

- Feature/indices at every level [\#12](https://github.com/Rambatino/CHAID/pull/12) ([Rambatino](https://github.com/Rambatino))

## [v0.0.10](https://github.com/Rambatino/CHAID/tree/v0.0.10) (2016-06-22)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.9...v0.0.10)

## [v0.0.9](https://github.com/Rambatino/CHAID/tree/v0.0.9) (2016-06-21)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.8...v0.0.9)

**Implemented enhancements:**

- Add iteration and node accessor interface [\#11](https://github.com/Rambatino/CHAID/pull/11) ([xulaus](https://github.com/xulaus))

## [v0.0.8](https://github.com/Rambatino/CHAID/tree/v0.0.8) (2016-06-21)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.7...v0.0.8)

## [v0.0.7](https://github.com/Rambatino/CHAID/tree/v0.0.7) (2016-06-20)
[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.0.6...v0.0.7)

**Implemented enhancements:**

- Enable passing through of column names [\#5](https://github.com/Rambatino/CHAID/pull/5) ([Rambatino](https://github.com/Rambatino))

**Fixed bugs:**

- Properly label aggregations of dependent variable [\#4](https://github.com/Rambatino/CHAID/pull/4) ([xulaus](https://github.com/xulaus))

## [v0.0.6](https://github.com/Rambatino/CHAID/tree/v0.0.6) (2016-06-17)
**Fixed bugs:**

- Python 3 fixes [\#2](https://github.com/Rambatino/CHAID/pull/2) ([Rambatino](https://github.com/Rambatino))
- Enabled numpy to be of type float and added metadata [\#1](https://github.com/Rambatino/CHAID/pull/1) ([Rambatino](https://github.com/Rambatino))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*