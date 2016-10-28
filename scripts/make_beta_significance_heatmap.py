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
from fastunifrac.make_beta_significance_heatmap import \
    make_beta_significance_heatmap
import os

script_info = {}
script_info['brief_description'] = """Generates a html file with a heatmap of\
 the beta significance output test (each pair of samples)."""
script_info['script_description'] = """Takes a beta significance pairwise test\
 output file (file output of beta_significance.py) and generates a html file\
 containing the image of the heatmap of the results. [Note: The html file will\
 not work in a browser unless the html file is placed in the output_dir]"""
script_info['script_usage'] = [
    ("Example", "Generate a html file named 'index.html' with the heatmap of " +
     "the beta significance test results represented in 'beta_sig_output.txt' " +
     "and place the images and the scripts in 'output_dir'",
     "%prog -i beta_sig_output.txt -m mapping_file.txt -o index.html" +
     " --output_dir=output_dir")
]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--input_fp', type="existing_filepath",
                help='Beta significance output filepath'),
    make_option('-m', '--mapping_fp', type="existing_filepath",
                help='Mapping file path'),
    make_option('-o', '--output_html_fp', type="new_filepath",
                help='Html filepath'),
    make_option('--output_dir', type="new_dirpath",
                help='A directory which will contain the images and scripts')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    bs_fp = opts.input_fp
    mapping_fp = opts.mapping_fp
    html_fp = opts.output_html_fp
    output_dir = opts.output_dir

    try:
        os.mkdir(opts.output_dir)
    except OSError:
        pass

    make_beta_significance_heatmap(bs_fp, mapping_fp, html_fp, output_dir)
