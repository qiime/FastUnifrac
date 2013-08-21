#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from fastunifrac.make_distance_matrix_heatmap import make_distance_matrix_heatmap
import os

script_info = {}
script_info['brief_description'] = """Generates a html file with a heatmap of the distance matrix."""
script_info['script_description'] = """Takes a distance matrix file (file output of beta_diversity.py) and generates a html file containing the image of the heatmap of the distance matrix. [Note: The html file will not work in a browser unless the html file is placed in the output_dir]"""
script_info['script_usage'] = [("Example", "Generate a html file named 'index.html' with the heatmap of \
    the distance matrix represented in 'distance_matrix.txt' and place the images and the scripts in 'output_dir'",
    "%prog -i distance_matrix.txt -m mapping_file.txt -o index.html --output_dir=output_dir/")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--distance_matrix_fp', type="existing_filepath",
                help='Distance matrix filepath'),
    make_option('-m', '--mapping_fp', type='existing_filepath',
                help='Mapping file path'),
    make_option('-o', '--output_html_fp', type="new_filepath",
                help='Html filepath'),
    make_option('--output_dir', type="new_dirpath",
                help='The directory which will contain the images and scripts')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    dm_fp = opts.distance_matrix_fp
    mapping_fp = opts.mapping_fp
    html_fp = opts.output_html_fp
    output_dir = opts.output_dir

    try:
        os.mkdir(opts.output_dir)
    except OSError:
        pass

    make_distance_matrix_heatmap(open(dm_fp, 'U'), open(mapping_fp, 'U'), html_fp, output_dir)