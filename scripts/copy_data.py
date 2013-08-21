#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from shutil import copyfile

script_info = {}
script_info['brief_description'] = """Copy the contents of the input file to the output file"""
script_info['script_description'] = """Copy the contents of the input file to the output file"""
script_info['script_usage'] = [("Example", "Copy the contents of the input file 'input_file.txt' to the output file 'output_file.txt'", "%prog -i input_file.txt -o output_file.txt")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--input_fp', type="existing_filepath",
                help='Input file to be copied'),
    make_option('-o', '--output_fp', type="new_filepath",
                help='File path to copy the input file')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_fp = opts.input_fp
    output_fp = opts.output_fp

    copyfile(input_fp, output_fp)
