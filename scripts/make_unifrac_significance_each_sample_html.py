#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.util import parse_command_line_parameters, make_option
from fastunifrac.parse import parse_beta_significance_output_each_sample
from fastunifrac.make_unifrac_significance_each_sample_html import \
    make_html_file

script_info = {}
script_info['brief_description'] = """Generates a html file with a table\
 showing the beta significance output test (each sample individually)."""
script_info['script_description'] = """Takes a beta significance each sample\
 individually test output file (file output of beta_significance.py) and\
 generates a html file containing a table showing the results."""
script_info['script_usage'] = [
    ("Example", "Generate a html file named 'index.html' with a table showing " +
        "the beta significance test results represented in 'beta_output.txt'",
        "%prog -i beta_output.txt -o index.html")
]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--input_fp', type="existing_filepath",
                help='Beta significance output filepath'),
    make_option('-o', '--output_html_fp', type="new_filepath",
                help='Html filepath')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    bs_fp = opts.input_fp
    html_fp = opts.output_html_fp

    bs_lines = open(bs_fp, 'U')

    dict_data, test_name = parse_beta_significance_output_each_sample(bs_lines)

    make_html_file(dict_data, test_name, html_fp)
