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
from qiime.util import load_qiime_config
from os import path, remove, mkdir, rmdir
from fastunifrac.make_heatmap import (get_info_from_dict, get_matrix_value,
    make_plot_data, plot_heatmap, HEADERS_VER, HEADERS_HOR)

class MakeHeatmapTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'

        self.plot_name = "example_name"

        self.headers = {}
        self.headers[HEADERS_HOR] = ["Sample1", "Sample2", "Sample3", "Sample4"]
        self.headers[HEADERS_VER] = ["Sample1", "Sample2", "Sample3", "Sample4"]

        self.matrix = matrix

        self.trans_values = {}
        self.trans_values[(None, None)] = (0, "")
        self.trans_values[(0.0, 0.25)] = (1, "(0-25%)")
        self.trans_values[(0.25, 0.5)] = (2, "(25-50%)")
        self.trans_values[(0.5, 0.75)] = (3, "(50-75%)")
        self.trans_values[(0.75, 1.0)] = (4, "(75-100%)")

        self.output_dir = path.join(self.tmp_dir, self.plot_name)

        self.plot_name_ns = "not_a_square_matrix"
        self.headers_ns = {}
        self.headers_ns[HEADERS_HOR] = ["Sample1", "Sample2",
                                            "Sample3", "Sample4"]
        self.headers_ns[HEADERS_VER] = ["Sample1", "Sample2", "Sample3"]
        self.matrix_ns = not_a_square_matrix
        self.output_dir_ns = path.join(self.tmp_dir, self.plot_name_ns)

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)
        map(rmdir, self._dirs_to_clean_up)

    def test_get_info_from_dict(self):
        """The information for the plot is retrieved correctly from the dict"""
        n_values, boundaries, ticks, ticklabels = \
            get_info_from_dict(self.trans_values)

        result_boundaries = [0.5, 1.5, 2.5, 3.5, 4.5]
        result_ticks = [1.0, 2.0, 3.0, 4.0]
        result_ticklabels = ["(0-25%)", "(25-50%)", "(50-75%)", "(75-100%)"]

        self.assertEqual(n_values, 5)
        self.assertEqual(boundaries, result_boundaries)
        self.assertEqual(ticks, result_ticks)
        self.assertEqual(ticklabels, result_ticklabels)

    def test_get_matrix_value(self):
        """The matrix value is translated correctly"""
        self.assertEqual(get_matrix_value(None, self.trans_values), 0)
        self.assertEqual(get_matrix_value(0.15, self.trans_values), 1)
        self.assertEqual(get_matrix_value(0.35, self.trans_values), 2)
        self.assertEqual(get_matrix_value(0.65, self.trans_values), 3)
        self.assertEqual(get_matrix_value(0.85, self.trans_values), 4)

        self.assertEqual(get_matrix_value(0.0, self.trans_values), None)
        self.assertEqual(get_matrix_value(0.25, self.trans_values), 1)
        self.assertEqual(get_matrix_value(0.5, self.trans_values), 2)
        self.assertEqual(get_matrix_value(0.75, self.trans_values), 3)
        self.assertEqual(get_matrix_value(1.0, self.trans_values), 4)

    def test_make_plot_data(self):
        """The plot data is retrieved correctly from the matrix values"""
        result_matrix = [[0, 1, 4, 2],
                            [0, 0, 4, 3],
                            [0, 0, 0, 2],
                            [0, 0, 0, 0]]

        self.assertEqual(make_plot_data(self.matrix, self.trans_values),
            result_matrix)

        result_matrix = [[0, 1, 4, 2],
                            [0, 0, 4, 3],
                            [0, 0, 0, 2]]

        self.assertEqual(make_plot_data(self.matrix_ns, self.trans_values),
            result_matrix)

    def test_plot_heatmap(self):
        """The heatmap images are generated correctly"""
        png_img_fp = path.join(self.output_dir, self.plot_name + '.png')
        eps_gz_fp = path.join(self.output_dir, self.plot_name + '.eps.gz')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp]
        self._dirs_to_clean_up = [self.output_dir]

        mkdir(self.output_dir)

        width, height, plot = plot_heatmap(self.plot_name, self.headers,
            self.matrix, self.trans_values, self.output_dir)

        self.assertEqual(width, 10)
        self.assertEqual(height, 10)
        self.assertTrue(path.exists(png_img_fp),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp),
            'The eps file was not created in the appropiate location')


        png_img_fp_ns = path.join(self.output_dir_ns,
            self.plot_name_ns + '.png')
        eps_gz_fp_ns = path.join(self.output_dir_ns,
            self.plot_name_ns + '.eps.gz')

        self._paths_to_clean_up.append(png_img_fp_ns)
        self._paths_to_clean_up.append(eps_gz_fp_ns)
        self._dirs_to_clean_up.append(self.output_dir_ns)

        mkdir(self.output_dir_ns)

        width, height, plot = plot_heatmap(self.plot_name_ns, self.headers_ns,
            self.matrix_ns, self.trans_values, self.output_dir_ns)

        self.assertEqual(width, 10)
        self.assertEqual(height, 10)
        self.assertTrue(path.exists(png_img_fp_ns),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp_ns),
            'The eps file was not created in the appropiate location')

matrix = [[None, 0.1, 0.9, 0.5],
    [None, None, 0.8, 0.7],
    [None, None, None, 0.4],
    [None, None, None, None]]

not_a_square_matrix = [[None, 0.1, 0.9, 0.5],
    [None, None, 0.8, 0.7],
    [None, None, None, 0.4]]

if __name__ == '__main__':
    main()