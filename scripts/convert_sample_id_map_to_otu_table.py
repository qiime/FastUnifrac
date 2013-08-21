#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas", ]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.option_parsing import parse_command_line_parameters, make_option
from fastunifrac.convert_sample_id_map_to_otu_table import convert_sample_id_map_to_otu_table

script_info = {}
script_info['brief_description'] = """ Generates an OTU table biom file from a sample ID mapping file. """
script_info['script_description'] = """Takes a sample ID mapping file (tab-delimited file where the first column is the sequence ID, the second column is sample ID and the last column is the number of times the sequence was observed) and generates an OTU table in biom format. Also, this script checks:
    - If the output filename has spaces, and fix it.
    - If there is any bad char in the sample id's and fix it.
"""
script_info['script_usage'] = [("Example" , "Generate an OTU table biom file from a sample ID mapping file (in this case sample_id_mapping_file.txt", "%prog -i sample_id_mapping_file.txt")]
script_info['output_description'] = "An OTU table file in biom format."
script_info['required_options'] = [
    make_option('-i', '--sample_id_map_fp', type="existing_filepath",
                help='sample id mapping file'),
]
script_info['optional_options'] = [
    make_option('-o', '--biom_fp', type="new_filepath",
                help='OTU table biom file'),
]
script_info['version'] = __version__
    

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_fp = opts.sample_id_map_fp
    output_fp = opts.biom_fp

    convert_sample_id_map_to_otu_table(input_fp, output_fp)