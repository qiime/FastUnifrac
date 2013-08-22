#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from fastunifrac.make_html_heatmap import (LD_NAME, LD_HEADERS, LD_HEADERS_VER,
    LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES, LD_TABLE_TITLE)
from fastunifrac.make_distance_matrix_heatmap import (get_upper_triangle,
    compute_quartiles, make_quartiles, generate_trans_values_dict,
    generate_data_make_html)

class MakeDistanceMatrixHeatmapTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        self.dm_lines = dm_lines.splitlines()

        self.matrix = [[0, 1, 2, 3],
        [1, 0, 4, 5],
        [2, 4, 0, 6],
        [3, 5, 6, 0]]

        self.upper_triangle = [[None, 1, 2, 3],
        [None, None, 4, 5],
        [None, None, None, 6],
        [None, None, None, None]]

    def test_get_upper_triangle(self):
        """The upper triangle of a matrix is retrieved correctly"""
        obs_result = get_upper_triangle(self.matrix)
        exp_result =[[None, 1, 2, 3],
            [None, None, 4, 5],
            [None, None, None, 6],
            [None, None, None, None]]

        self.assertEqual(obs_result, exp_result)

    def test_compute_quartiles(self):
        """The quartiles are computed correctly"""
        data = [1, 2, 3, 4, 5, 6]
        lq, qmedian, uq = compute_quartiles(data)
        lq_exp = 2
        qmedian_exp = 3.5
        uq_exp = 5

        self.assertEqual(lq, lq_exp)
        self.assertEqual(qmedian, qmedian_exp)
        self.assertEqual(uq, uq_exp)

        data = [1, 2, 3, 4, 5]
        lq, qmedian, uq = compute_quartiles(data)
        lq_exp = 1.5
        qmedian_exp = 3
        uq_exp = 4.5

        self.assertEqual(lq, lq_exp)
        self.assertEqual(qmedian, qmedian_exp)
        self.assertEqual(uq, uq_exp)

        data = [1, 2, 3]
        self.assertRaises(ValueError, compute_quartiles, data)

    def test_make_quartiles(self):
        """The dict with the quartile ranges are computed correctly"""
        obs_quart = make_quartiles(self.upper_triangle)
        exp_quart ={
            (0.99, 2):(1, "(0-25%)\nLower\nquartile"),
            (2, 3.5):(2.0, "(25-50%)"),
            (3.5, 5):(3.0, "(50-75%)"),
            (5, 6.01):(4.0,"(75-100%)\nUpper\nquartile")
        }
        self.assertEqual(obs_quart, exp_quart)

    def test_generate_trans_values_dict(self):
        """The transformation dictionary is generated correctly"""
        obs_trans_values = generate_trans_values_dict(self.upper_triangle)
        exp_trans_values = {
            (0.99, 2):(1, "(0-25%)\nLower\nquartile"),
            (2, 3.5):(2.0, "(25-50%)"),
            (3.5, 5):(3.0, "(50-75%)"),
            (5, 6.01):(4.0,"(75-100%)\nUpper\nquartile"),
            (None, None): (0, "")
        }
        self.assertEqual(obs_trans_values, exp_trans_values)

    def test_generate_data_make_html(self):
        """The dict with the plot data is generated correctly"""
        obs_data = generate_data_make_html(self.dm_lines)

        exp_data = {}
        exp_data[LD_NAME] = "Distance matrix"
        headers = {}
        headers[LD_HEADERS_HOR] = ['a', 'b', 'c', 'd']
        headers[LD_HEADERS_VER] = ['a', 'b', 'c', 'd']
        exp_data[LD_HEADERS] = headers
        exp_data[LD_MATRIX] = [[None, 1, 2, 3],
                                [None, None, 4, 5],
                                [None, None, None, 6],
                                [None, None, None, None]]
        exp_data[LD_TRANSFORM_VALUES] = {
            (0.99, 2):(1, "(0-25%)\nLower\nquartile"),
            (2, 3.5):(2.0, "(25-50%)"),
            (3.5, 5):(3.0, "(50-75%)"),
            (5, 6.01):(4.0,"(75-100%)\nUpper\nquartile"),
            (None, None): (0, "")}
        exp_data[LD_TABLE_TITLE] = "Distance matrix"

        self.assertEqual(obs_data, exp_data)

dm_lines = """\ta\tb\tc\td
a\t0\t1\t2\t3
b\t1\t0\t4\t5
c\t2\t4\t0\t6
d\t3\t5\t6\t0
"""

if __name__ == '__main__':
    main()