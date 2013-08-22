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
from qiime.util import load_qiime_config, get_tmp_filename
from os import remove
from fastunifrac.make_html_heatmap import (LD_NAME, LD_HEADERS, LD_HEADERS_VER,
    LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES, LD_TABLE_TITLE)
from fastunifrac.make_beta_significance_heatmap import (
    generate_headers_and_matrix, generate_dict_data, generate_data_make_html)

class MakeBetaSignificanceHeatmapTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        # Get the tmp folder
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        # Initialize some variables
        self.input_file = get_tmp_filename(tmp_dir = self.tmp_dir)
        self.dict_data = {('s1', 's2'):(0.01, 0.15),
            ('s1', 's3'):(0.0, 0.01),
            ('s1', 's4'):(0.02, 0.3),
            ('s2', 's3'):(0.82, 1.0),
            ('s2', 's4'):(0.4, 1.0),
            ('s3', 's4'):(0.0, 0.01)}
        self.name = "Sample name"
        self.headers = {LD_HEADERS_VER: ['s1', 's2', 's3'],
            LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']}
        self.matrix = [[None, 0.01, 0.0, 0.02],
            [None, None, 0.82, 0.4],
            [None, None, None, 0.0]]
        self.test_name = "Example test name"
        self._paths_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)

    def test_generate_headers_and_matrix(self):
        """The headers and the matrix is retrieved correctly"""
        obs_headers, obs_matrix = generate_headers_and_matrix(self.dict_data, 0)

        exp_headers = {LD_HEADERS_VER: ['s1', 's2', 's3'],
            LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']}

        exp_matrix = [[None, 0.01, 0.0, 0.02],
            [None, None, 0.82, 0.4],
            [None, None, None, 0.0]]

        self.assertEqual(obs_headers, exp_headers)
        self.assertEqual(obs_matrix, exp_matrix)

        obs_headers, obs_matrix = generate_headers_and_matrix(self.dict_data, 1)

        exp_headers = {LD_HEADERS_VER: ['s1', 's2', 's3'],
            LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']}

        exp_matrix = [[None, 0.15, 0.01, 0.3],
            [None, None, 1.0, 1.0],
            [None, None, None, 0.01]]

        self.assertEqual(obs_headers, exp_headers)
        self.assertEqual(obs_matrix, exp_matrix)

        self.assertRaises(ValueError, generate_headers_and_matrix,
            self.dict_data, 2)

    def test_generate_dict_data(self):
        """The dictionary with the plot data is generated correctly"""
        obs_dict_data = generate_dict_data(self.name, self.headers,
            self.matrix, self.test_name)

        exp_dict_data = {LD_NAME: "Sample name",
            LD_HEADERS: {LD_HEADERS_VER: ['s1', 's2', 's3'],
                LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']},
            LD_MATRIX : [[None, 0.01, 0.0, 0.02],
                [None, None, 0.82, 0.4],
                [None, None, None, 0.0]],
            LD_TRANSFORM_VALUES: {(None, None) : (0, ""),
                (None, 0.001): (1, "(<0.001)\nHighly\nsignificant"),
                (0.001, 0.01): (2, "(0.001-0.01)\nSignificant"),
                (0.01, 0.05): (3, "(0.01-0.05)\nMarginally\nsignificant"),
                (0.05, 0.1): (4, "(0.05-0.1)\nSuggestive"),
                (0.1, None): (5, "(>0.1)\nNot\nsignificant")},
            LD_TABLE_TITLE: "Example test name: Sample name"}

        self.assertEqual(obs_dict_data, exp_dict_data)

    def test_generate_data_make_html(self):
        """The list of dicts is generated correctly"""
        out = open(self.input_file, 'w')
        out.write(bs_file_content)
        out.close()

        self._paths_to_clean_up = [self.input_file]

        bs_lines = open(self.input_file, 'U')

        obs_list_data = generate_data_make_html(bs_lines)

        dict_raw = {LD_NAME: "Raw values",
            LD_HEADERS: {LD_HEADERS_VER: ['s1', 's2', 's3'],
                LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']},
            LD_MATRIX : [[None, 0.01, 0.0, 0.02],
                [None, None, 0.82, 0.4],
                [None, None, None, 0.0]],
            LD_TRANSFORM_VALUES: {(None, None) : (0, ""),
                (None, 0.001): (1, "(<0.001)\nHighly\nsignificant"),
                (0.001, 0.01): (2, "(0.001-0.01)\nSignificant"),
                (0.01, 0.05): (3, "(0.01-0.05)\nMarginally\nsignificant"),
                (0.05, 0.1): (4, "(0.05-0.1)\nSuggestive"),
                (0.1, None): (5, "(>0.1)\nNot\nsignificant")},
            LD_TABLE_TITLE: "Comment with the name of the test realized: Raw values"}

        dict_corr = {LD_NAME: "Corrected values",
            LD_HEADERS: {LD_HEADERS_VER: ['s1', 's2', 's3'],
                LD_HEADERS_HOR: ['s1', 's2', 's3', 's4']},
            LD_MATRIX : [[None, 0.15, 0.01, 0.3],
                [None, None, 1.0, 1.0],
                [None, None, None, 0.01]],
            LD_TRANSFORM_VALUES: {(None, None) : (0, ""),
                (None, 0.001): (1, "(<0.001)\nHighly\nsignificant"),
                (0.001, 0.01): (2, "(0.001-0.01)\nSignificant"),
                (0.01, 0.05): (3, "(0.01-0.05)\nMarginally\nsignificant"),
                (0.05, 0.1): (4, "(0.05-0.1)\nSuggestive"),
                (0.1, None): (5, "(>0.1)\nNot\nsignificant")},
            LD_TABLE_TITLE: "Comment with the name of the test realized: Corrected values"}

        exp_list_data = [dict_raw, dict_corr]

        self.assertEqual(obs_list_data, exp_list_data)

bs_file_content = """#Comment with the name of the test realized
Sample1\tSample2\tp value\tp value (Bonferroni corrected)
s1\ts2\t0.01\t0.15
s1\ts3\t0.0\t<=1.0e-02
s1\ts4\t0.02\t0.3
s2\ts3\t0.82\t1.0
s2\ts4\t0.4\t1.0
s3\ts4\t0.0\t<=1.0e-02
"""

if __name__ == '__main__':
    main()