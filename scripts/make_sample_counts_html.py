#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from fastunifrac.make_sample_counts_html import make_html_file

script_info = {}
script_info['brief_description'] = """Generates an html file with a table with the results of the sample counts analysis."""
script_info['script_description'] = """Generates an html file with a table with the results of the sample counts analysis."""
script_info['script_usage'] = [("Example", "Generate an html called 'index.html' with the sample counts stored at 'per_library_stats_output_file'", 
    "%prog -m per_library_stats_output_file -o index.html")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-m', '--mapping_fp', type='existing_filepath', help="Mapping file output from per_library_stats.py"),
    make_option('-o', '--output_html_fp', type='new_filepath', help="Html filepath")
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    mapping_fp = opts.mapping_fp
    html_fp = opts.output_html_fp

    make_html_file(open(mapping_fp, 'U'), html_fp)