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
from fastunifrac.make_pcoa_html import make_html_file

script_info = {}
script_info['brief_description'] = """Generates a html file which shows the\
 PCoA results."""
script_info['script_description'] = """ Generates a html file which shows the\
 PCoA results."""
script_info['script_usage'] = [
	("Example", "Generates a html file named 'index.html' with the PCoA " + 
		"results stored under the folder 'pcoa_output_dir'",
    	"%prog -d pcoa_output_dir -o index.html")
]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-o', '--output_html_fp', type="new_filepath",
                help='Html filepath'),
    make_option('-d', '--pcoa_output_directory', type="existing_dirpath",
                help='Directory which contains the PCoA results')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    html_fp = opts.output_html_fp
    pcoa_dir = opts.pcoa_output_directory

    make_html_file(pcoa_dir, html_fp)