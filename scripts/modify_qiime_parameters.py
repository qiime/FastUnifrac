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
from fastunifrac.modify_qiime_parameters import modify_qiime_parameters

script_info = {}
script_info['brief_description'] = """Takes a QIIME parameter file and creates a copy modifying the desired parameters"""
script_info['script_description'] = """ Takes a QIIME parameter file and creates a copy modifying the parameters indicated \
in a comma separated list by the -p option assigning them the values indicated in a comma separated list by the -n option.
For a multiple value assignment (more than one value to a parameter), separate them by '-'. The lists in -p and -n options \
must be in the same order."""
script_info['script_usage'] = [("Example", " Make a copy from 'qiime_params.txt' saved in 'output.txt' modifying \
the split_libraries:min-seq-length and pick_otus:otu_picking_method parameters by assigning them \
' ' (space) and uclust values, respectively", \
"%prog -i qiime_params.txt -p split_libraries:min-seq-length,pick_otus:otu_picking_method -n  ,uclust -o output.txt")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--parameter_fp', type='existing_filepath',
                help='Original parameter file to make a copy with changes'),
    make_option('-p', '--parameters', type="string",
                help='Comma separated list with script:parameter to change. Example: split_libraries:min-seq-length,pick_otus:otu_picking_method'),
    make_option('-n', '--new_values', type="string",
                help='Comma separated list with new values. Must be the same order as --parameters option. Multiple values separated by "-". Example: ,uclust'),
    make_option('-o', '--output_fp', type='new_filepath',
                help='Output parameter file with changes done')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    parameter_file = opts.parameter_fp
    parameters = opts.parameters
    new_values = opts.new_values
    output_fp = opts.output_fp

    modify_qiime_parameters(parameter_file, output_fp, parameters, new_values)