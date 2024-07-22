# Changelog

## [Unreleased](https://github.com/Rambatino/CHAID/tree/HEAD)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.4.0...HEAD)

**Closed issues:**

- to\_graphviz\(\) returns NoneType [\#139](https://github.com/Rambatino/CHAID/issues/139)
- RuntimeWarning: invalid value encountered in cast [\#137](https://github.com/Rambatino/CHAID/issues/137)
- np.float is deprecated [\#133](https://github.com/Rambatino/CHAID/issues/133)
- Failed to execute 'getPointAtLength' on 'SVGGeometryElement': The element's path is empty. [\#132](https://github.com/Rambatino/CHAID/issues/132)
- Error while running tree.render\(\) [\#131](https://github.com/Rambatino/CHAID/issues/131)
- question about output [\#130](https://github.com/Rambatino/CHAID/issues/130)
- tree.render\(\) throws error while working with data bricks azure [\#129](https://github.com/Rambatino/CHAID/issues/129)
- Prediction [\#128](https://github.com/Rambatino/CHAID/issues/128)
- Continuous Column name arg & Plotting Tree [\#127](https://github.com/Rambatino/CHAID/issues/127)
- Prior Nodes [\#126](https://github.com/Rambatino/CHAID/issues/126)
- Slow [\#125](https://github.com/Rambatino/CHAID/issues/125)
- missing value in ordinal feature and bonferroni adjustment [\#124](https://github.com/Rambatino/CHAID/issues/124)
- Feature selection difference with SPSS [\#123](https://github.com/Rambatino/CHAID/issues/123)
- how to get feature\_importance  [\#122](https://github.com/Rambatino/CHAID/issues/122)
- Issue exporting tree graph [\#121](https://github.com/Rambatino/CHAID/issues/121)
- Nominal Column is not defined [\#119](https://github.com/Rambatino/CHAID/issues/119)
- Documentation for library [\#118](https://github.com/Rambatino/CHAID/issues/118)
- I got the path to work, but now I'm back to the initial problem I had with the invalid argument in trees. -\_- [\#117](https://github.com/Rambatino/CHAID/issues/117)
- Not being able to visualize it in Colab [\#116](https://github.com/Rambatino/CHAID/issues/116)
- is it copy of https://github.com/codingblg/CHAID\_phi [\#115](https://github.com/Rambatino/CHAID/issues/115)

**Merged pull requests:**

- Fix one numpy deprecated function \(in1d -\> isin\) [\#140](https://github.com/Rambatino/CHAID/pull/140) ([jihaekor](https://github.com/jihaekor))
- Use an explicit sentinel value rather than relying on integer cast of np.nan [\#138](https://github.com/Rambatino/CHAID/pull/138) ([jihaekor](https://github.com/jihaekor))
- Add a new max\_splits parameter; make a couple of fix updates [\#136](https://github.com/Rambatino/CHAID/pull/136) ([jihaekor](https://github.com/jihaekor))
- Fix errors due to numpy deprecation; split required packages further; update specs [\#135](https://github.com/Rambatino/CHAID/pull/135) ([jihaekor](https://github.com/jihaekor))
- Fixed README imports [\#120](https://github.com/Rambatino/CHAID/pull/120) ([Rambatino](https://github.com/Rambatino))
- Added exhaustive CHAID [\#113](https://github.com/Rambatino/CHAID/pull/113) ([Rambatino](https://github.com/Rambatino))
- Added graph specs and switched off true divide warnings for specs [\#111](https://github.com/Rambatino/CHAID/pull/111) ([Rambatino](https://github.com/Rambatino))

## [v5.4.0](https://github.com/Rambatino/CHAID/tree/v5.4.0) (2020-10-30)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5...v5.4.0)

**Closed issues:**

- Exhaustive chaid  [\#112](https://github.com/Rambatino/CHAID/issues/112)
- Not being able to visualize the tree [\#110](https://github.com/Rambatino/CHAID/issues/110)
- No Attribute "from\_numpy" [\#109](https://github.com/Rambatino/CHAID/issues/109)
- Error while importing in Jupyter Notebook [\#108](https://github.com/Rambatino/CHAID/issues/108)
- Issue with members property [\#107](https://github.com/Rambatino/CHAID/issues/107)
- Need to spec out the graphing architecture  [\#106](https://github.com/Rambatino/CHAID/issues/106)
- Warnings have appeared when running specs locally. The bit rot is real [\#105](https://github.com/Rambatino/CHAID/issues/105)
- Issue in running the "tree.render\(path=None, view=False\)" [\#99](https://github.com/Rambatino/CHAID/issues/99)

## [v5](https://github.com/Rambatino/CHAID/tree/v5) (2020-01-13)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.3.0...v5)

## [v5.3.0](https://github.com/Rambatino/CHAID/tree/v5.3.0) (2020-01-13)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.2.0...v5.3.0)

**Closed issues:**

- Missing dependencies [\#102](https://github.com/Rambatino/CHAID/issues/102)
- Python 2 incompatibility: invalid\_split\_reason.py uses enum [\#101](https://github.com/Rambatino/CHAID/issues/101)
- tree.to\_tree\(\)  is not working for creating the dot file in CHAID analysis  and also tried "tree.render\(path=None, view=False\)" to get tree but failed get so.. please any suggestion  [\#98](https://github.com/Rambatino/CHAID/issues/98)
- Export error [\#97](https://github.com/Rambatino/CHAID/issues/97)
- how to graphically display the tree? [\#93](https://github.com/Rambatino/CHAID/issues/93)

**Merged pull requests:**

- Fix graph installations in the README.md. Add note about python 2.7 [\#104](https://github.com/Rambatino/CHAID/pull/104) ([Rambatino](https://github.com/Rambatino))
- Py2 compat: add conditional dep [\#103](https://github.com/Rambatino/CHAID/pull/103) ([mjpieters](https://github.com/mjpieters))
- Refactor Graph to avoid cross-platform issues [\#100](https://github.com/Rambatino/CHAID/pull/100) ([mjpieters](https://github.com/mjpieters))

## [v5.2.0](https://github.com/Rambatino/CHAID/tree/v5.2.0) (2019-04-03)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.1.0...v5.2.0)

**Implemented enhancements:**

- Added render method and graph export with path variable [\#94](https://github.com/Rambatino/CHAID/pull/94) ([Rambatino](https://github.com/Rambatino))
- Added accuracy method [\#90](https://github.com/Rambatino/CHAID/pull/90) ([Rambatino](https://github.com/Rambatino))

**Closed issues:**

- IS ID5 tree equalst to CHAID in concepts? [\#92](https://github.com/Rambatino/CHAID/issues/92)
- Make predictions on testing set and calculate the propensity scores  [\#89](https://github.com/Rambatino/CHAID/issues/89)
- Risk broken, needs speccing [\#74](https://github.com/Rambatino/CHAID/issues/74)

**Merged pull requests:**

- Attempting new cirlce ci file [\#95](https://github.com/Rambatino/CHAID/pull/95) ([Rambatino](https://github.com/Rambatino))

## [v5.1.0](https://github.com/Rambatino/CHAID/tree/v5.1.0) (2018-10-03)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.5...v5.1.0)

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
- Reverted back heuristic approach [\#84](https://github.com/Rambatino/CHAID/pull/84) ([Rambatino](https://github.com/Rambatino))

## [v5.0.4](https://github.com/Rambatino/CHAID/tree/v5.0.4) (2017-12-20)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v5.0.3...v5.0.4)

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

**Implemented enhancements:**

- Added SPSS weighting to the CHAID Algorithm [\#37](https://github.com/Rambatino/CHAID/pull/37) ([Rambatino](https://github.com/Rambatino))

## [v1.0.0](https://github.com/Rambatino/CHAID/tree/v1.0.0) (2016-09-22)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.4...v1.0.0)

## [v0.3.4](https://github.com/Rambatino/CHAID/tree/v0.3.4) (2016-07-27)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.3...v0.3.4)

## [v0.3.3](https://github.com/Rambatino/CHAID/tree/v0.3.3) (2016-07-25)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.2...v0.3.3)

## [v0.3.2](https://github.com/Rambatino/CHAID/tree/v0.3.2) (2016-07-25)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.1...v0.3.2)

## [v0.3.1](https://github.com/Rambatino/CHAID/tree/v0.3.1) (2016-07-14)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.3.0...v0.3.1)

**Implemented enhancements:**

- Switched yates correction off to match spss [\#25](https://github.com/Rambatino/CHAID/pull/25) ([Rambatino](https://github.com/Rambatino))

**Merged pull requests:**

- Hotfix/numpy 1 9 feature removal [\#27](https://github.com/Rambatino/CHAID/pull/27) ([Rambatino](https://github.com/Rambatino))
- Fixed risk value calculation [\#26](https://github.com/Rambatino/CHAID/pull/26) ([Rambatino](https://github.com/Rambatino))

## [v0.3.0](https://github.com/Rambatino/CHAID/tree/v0.3.0) (2016-07-14)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/v0.2.0...v0.3.0)

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

## [v0.0.6](https://github.com/Rambatino/CHAID/tree/v0.0.6) (2016-06-17)

[Full Changelog](https://github.com/Rambatino/CHAID/compare/af4ce7e062ec847f92f7b7eb4884910a7f6fc92f...v0.0.6)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
