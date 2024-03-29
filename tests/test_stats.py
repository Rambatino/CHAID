"""
Testing module for the class Stats
"""

from unittest import TestCase
from setup_tests import CHAID
import numpy as np
import pandas as pd

class TestContinuousStats(TestCase):
    """ Tests for continuous stats"""
    def setUp(self):
        """ Setup test data for continuous data """
        self.random_arr = np.array(
           [0.23198952,  0.26550251,  0.96461057,  0.13733767,  0.76674088,
            0.60637166,  0.18822053,  0.78785506,  0.47786053,  0.44448984,
            0.88632344,  0.94060264,  0.52900520,  0.68301794,  0.00485769,
            0.09299505,  0.41767638,  0.22345506,  0.61899892,  0.53763263,
            0.41424529,  0.87527060,  0.10843391,  0.22902548,  0.52043049,
            0.82396842,  0.64215622,  0.42827082,  0.76920710,  0.27736853,
            0.95756523,  0.45140920,  0.12405161,  0.53774033,  0.72198885,
            0.37880053,  0.93554955,  0.44434796,  0.62834896,  0.02788777,
            0.30288893,  0.07198041,  0.59731867,  0.63485262,  0.79936557,
            0.41154027,  0.82900816,  0.49216809,  0.56649288,  0.26539558,
            0.12304309,  0.03233878,  0.64612524,  0.69844021,  0.30560065,
            0.05408900,  0.31020185,  0.93087523,  0.27952452,  0.57186781,
            0.36214135,  0.34114557,  0.82028983,  0.29795183,  0.21028335,
            0.41612748,  0.24781879,  0.19125266,  0.17214954,  0.44039645,
            0.84397111,  0.91060384,  0.70898285,  0.27049457,  0.15502956,
            0.47580771,  0.21507488,  0.68243381,  0.56233427,  0.22376202,
            0.76630117,  0.00162193,  0.15057895,  0.10145753,  0.69406461,
            0.81280760,  0.79726816,  0.42523241,  0.56025856,  0.10287649,
            0.53337746,  0.82185783,  0.38270064,  0.77411309,  0.01754383,
            0.84690273,  0.20057135,  0.37194360,  0.24657089,  0.91520048,
            0.65575302,  0.03220805,  0.71449568,  0.97194268,  0.94031990,
            0.61484448,  0.46961425,  0.38495625,  0.41865701,  0.81394666,
            0.57147433,  0.33414233,  0.13847757,  0.31316325,  0.04371212,
            0.36556674,  0.56316862,  0.66761528,  0.02491041,  0.12124478]
        )
        self.normal_arr = np.array([
            215.74655491,  237.0905247 ,  193.72021408,  152.89363815,
            175.36670032,  232.59086085,  204.20219942,  248.99321897,
            267.95686148,  165.7204985 ,  177.38110221,  220.40618705,
            262.71893125,  240.00774431,  210.85572027,  255.06583994,
            232.85274614,  274.71932373,  186.83175676,  241.47832856,
            294.98781486,  190.82037054,  143.7991682 ,  170.32090888,
            207.20320791,  208.10226642,  187.09923858,  178.9242382 ,
            155.17266333,  140.69923988,  210.80029533,  193.85525698,
            232.69854217,  230.4408611 ,  149.34523942,  303.6243051 ,
            171.1562868 ,  185.24131426,  195.80616026,  224.38213062,
            261.77203837,  170.81218927,  216.37943211,  265.25650174,
            203.3098626 ,  229.84982086,  212.14777791,  265.25335911,
            296.11334434,  242.40424522,  270.30264815,   77.97401496,
            176.80382943,  156.35135782,  155.29031942,  262.11885208,
            161.33251252,  256.05120377,  158.32542953,  189.07183278,
            155.72524265,  244.68956731,  286.68689241,   94.08648606,
            253.80300049,  161.17371005,  116.94584491,  182.88557535,
            182.85752412,  253.42111371,  131.25146323,  264.86407965,
            197.3742505 ,  296.95506279,  221.01600673,  234.04694958,
            154.42957223,  176.94139196,  200.59554949,  170.4040058 ,
            229.39358115,  127.43357367,  249.09735255,  227.90731765,
            238.9667355 ,  163.83410357,  194.88998826,  134.49013182,
            154.54356067,  254.19699384,  143.93816979,  256.11031829,
            186.56096688,  178.40462838,  159.79032932,  187.7542398 ,
            267.18537402,  190.99969385,  130.30080584,  216.12902248,
            247.8707783 ,  246.49016072,  275.3636918 ,  165.69987612,
            181.16709806,  193.87951446,  156.03720504,  221.44032879,
            182.21405831,  119.22571297,  219.14946203,  140.358539  ,
            210.5826685 ,  256.57132523,  244.82587339,  153.26377344,
            198.44006972,  172.6057332 ,  140.26518016,  171.32162943]
        )
        self.wt = np.array(([1.0] * 60) + ([1.2] * 60))
        ndarr = np.array(([2, 3] * 20) + ([2, 5] * 20) + ([3, 4] * 19) + [2, 3] + [1, 2, 5] * 80 + [1, 2, 3] * 40).reshape(120, 4)
        self.ndarr = [CHAID.NominalColumn(ndarr[:, i]) for i in range(ndarr.shape[1])]
        self.stats_random_data = CHAID.Stats(0.5, 10, None, .95, self.random_arr)
        self.stats_normal_data = CHAID.Stats(0.5, 10, None, .95, self.normal_arr)
        self.stats_random_data_max_splits = CHAID.Stats(0.5, 10, 2, .95, self.random_arr)
        self.stats_normal_data_max_splits = CHAID.Stats(0.5, 10, 2, .95, self.normal_arr)

    def test_p_and_chi_values_for_random_data(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_random_data.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.random_arr)
        )
        assert round(split.score, 4) == 1.0588
        assert round(split.p, 4) == 0.3056
        assert split.dof == 118.

    def test_p_and_chi_values_for_normal_data(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_normal_data.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.normal_arr)
        )
        assert round(split.score, 4) == 2.7346
        assert round(split.p, 4) == 0.0982
        assert split.dof == 118.

    def test_p_and_chi_values_for_random_data_weighted(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_random_data.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.random_arr, weights=self.wt)
        )
        assert round(split.score, 4) == 2.0056
        assert round(split.p, 4) == 0.1594
        assert split.dof == 118.

    def test_p_and_chi_values_for_normal_data_weighted(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_normal_data.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.normal_arr, weights=self.wt)
        )
        assert round(split.score, 4) == 2.238
        assert round(split.p, 4) == 0.1347
        assert split.dof == 118.

    def test_p_and_chi_values_for_random_data_max_splits(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_random_data_max_splits.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.random_arr)
        )
        assert round(split.score, 4) == 1.0588
        assert round(split.p, 4) == 0.3056
        assert split.dof == 118.

    def test_p_and_chi_values_for_normal_data_max_splits(self):
        """
        Check chi and p value against hand calculated values
        """
        split = self.stats_normal_data_max_splits.best_con_split(
            self.ndarr,
            CHAID.ContinuousColumn(self.normal_arr)
        )
        assert round(split.score, 4) == 2.8841
        assert round(split.p, 4) == 0.0895
        assert split.dof == 118.
