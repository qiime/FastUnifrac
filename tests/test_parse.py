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
from fastunifrac.parse import parse_beta_significance_output_pairwise, parse_beta_significance_output_each_sample, parse_jackknife_support_file
from qiime.util import load_qiime_config, get_tmp_filename
from os import remove

class ParseTest(TestCase):
    def setUp(self):
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.input_file = get_tmp_filename(tmp_dir = self.tmp_dir)
        self.support_lines = support_lines.splitlines()
        self._paths_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)

    def test_parse_beta_significance_output_pairwise(self):
        out = open(self.input_file, 'w')
        out.write(bs_lines_pairwise)
        out.close()

        self._paths_to_clean_up = [self.input_file]

        bs_lines = open(self.input_file, 'U')

        obs_dict, obs_test_name = parse_beta_significance_output_pairwise(bs_lines)

        exp_dict = {('s1', 's2'):(0.01, 0.15),
            ('s1', 's3'):(0.0, 0.01),
            ('s1', 's4'):(0.02, 0.3),
            ('s2', 's3'):(0.82, 1.0),
            ('s2', 's4'):(0.4, 1.0),
            ('s3', 's4'):(0.0, 0.01)}
        exp_test_name = "Comment with the name of the test realized"

        self.assertEqual(obs_dict, exp_dict)
        self.assertEqual(obs_test_name, exp_test_name)

    def test_parse_beta_significance_output_each_sample(self):
        out = open(self.input_file, 'w')
        out.write(bs_lines_each_sample)
        out.close()

        self._paths_to_clean_up = [self.input_file]

        bs_lines = open(self.input_file, 'U')

        obs_dict, obs_test_name = parse_beta_significance_output_each_sample(bs_lines)

        exp_dict = {'s1':(0.01, 0.15),
            's2':(0.0, 0.01),
            's3':(0.02, 0.3),
            's4':(0.82, 1.0)}
        exp_test_name = "Comment with the name of the test realized"

        self.assertEqual(obs_dict, exp_dict)
        self.assertEqual(obs_test_name, exp_test_name)

    def test_parse_jackknife_support_file(self):
        obs_dict = parse_jackknife_support_file(self.support_lines)
        exp_dict = {'trees_considered': 10,
            'support_dict': {'node0':1.0,
                            'node1':0.7,
                            'node2':0.4,
                            'node3':0.7,
                            'node4':0.6}
            }
        self.assertEqual(obs_dict, exp_dict)

bs_lines_pairwise = """#Comment with the name of the test realized
Sample1\tSample2\tp value\tp value (Bonferroni corrected)
s1\ts2\t0.01\t0.15
s1\ts3\t0.0\t<=1.0e-02
s1\ts4\t0.02\t0.3
s2\ts3\t0.82\t1.0
s2\ts4\t0.4\t1.0
s3\ts4\t0.0\t<=1.0e-02
"""

bs_lines_each_sample = """#Comment with the name of the test realized
sample\tp value\tp value (Bonferroni corrected)
s1\t0.01\t0.15
s2\t0.0\t<=1.0e-02
s3\t0.02\t0.3
s4\t0.82\t1.0
"""

support_lines = """#total support trees considered: 10
#node support is fractional - in range [0,1]
node0\t1.0
node1\t0.7
node2\t0.4
node3\t0.7
node4\t0.6
"""

if __name__ == '__main__':
    main()
