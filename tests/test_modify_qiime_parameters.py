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
from fastunifrac.modify_qiime_parameters import create_dict_of_changes, replace_value, modify_qiime_parameters
from qiime.util import load_qiime_config, get_tmp_filename
from os import remove, path

class ModifyQiimeParametersTest(TestCase):
    def setUp(self):
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.param_file = get_tmp_filename(tmp_dir = self.tmp_dir)
        self.output_file = get_tmp_filename(tmp_dir = self.tmp_dir)

        self.lines = qiime_params_string.splitlines()
        self.params = "scriptA:parameterA,scriptC:parameterA"
        self.values = "valA,valB"

        self._paths_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)

    def test_create_dict_of_changes(self):
        self.assertRaises(ValueError, create_dict_of_changes, "a:a,b:b", " ")

        obs_dict = create_dict_of_changes(self.params, self.values)
        exp_dict = {'scriptA:parameterA':'valA',
                    'scriptC:parameterA':'valB'}

        self.assertEqual(obs_dict, exp_dict)

    def test_replace_value(self):
        # Modify one value
        key = "scriptA:parameterA"
        value = "vC"
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\tvC\n",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvA,vB",
            "",
            "#Comment line",
            "scriptC:parameterA\t "]
        self.assertEqual(obs_lines, exp_lines)

        # Modify one value assigning empty string
        key = "scriptA:parameterA"
        value = " "
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\t \n",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvA,vB",
            "",
            "#Comment line",
            "scriptC:parameterA\t "]
        self.assertEqual(obs_lines, exp_lines)

        # Modify one value assigning multiples values
        key = "scriptA:parameterA"
        value = "valA-valB"
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\tvalA,valB\n",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvA,vB",
            "",
            "#Comment line",
            "scriptC:parameterA\t "]
        self.assertEqual(obs_lines, exp_lines)

        # Modify multiple value assigning one value
        key = "scriptB:parameterA"
        value = "valA"
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\tvA",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvalA\n",
            "",
            "#Comment line",
            "scriptC:parameterA\t "]

        # Modify an empty value by a value
        key = "scriptC:parameterA"
        value = "valA"
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\tvA",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvA,vB",
            "",
            "#Comment line",
            "scriptC:parameterA\tvalA\n"]
        self.assertEqual(obs_lines, exp_lines)

        # Add new parameter
        key = "scriptD:parameterA"
        value = "valueA"
        obs_lines = replace_value(self.lines, key, value)
        exp_lines = ["#Comment line",
            "scriptA:parameterA\tvA",
            "scriptA:parameterB\tvB",
            "",
            "#Comment line",
            "scriptB:parameterA\tvA,vB",
            "",
            "#Comment line",
            "scriptC:parameterA\t ",
            "scriptD:parameterA\tvalueA\n"]
        self.assertEqual(obs_lines, exp_lines)

    def test_modify_qiime_parameters(self):
        self._paths_to_clean_up = [self.param_file, self.output_file]

        input_file = open(self.param_file, 'w')
        input_file.write(qiime_params_string)
        input_file.close()

        modify_qiime_parameters(self.param_file, self.output_file, self.params, self.values)
        self.assertTrue(path.exists(self.output_file), 'The new QIIME parameters file was not created in the appropiate location')

qiime_params_string = """#Comment line
scriptA:parameterA\tvA
scriptA:parameterB\tvB

#Comment line
scriptB:parameterA\tvA,vB

#Comment line
scriptC:parameterA\t 
"""

if __name__ == '__main__':
    main()