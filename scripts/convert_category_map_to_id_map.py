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
from fastunifrac.convert_category_map_to_id_map import convert_category_map_to_id_map

script_info = {}
script_info['brief_description'] = """Takes a fastunifrac category mapping file and creates a QIIME mapping file"""
script_info['script_description'] = """ Specifically:

	- Check if the output filename has spaces, and fix it.
	- Check if there is any blank header and return an error if exists.
	- Check if there is any bad char in headers, and fix it.
	- Check if exists the SampleId header and return an error if not.
	- Check if exists the Barcode header and fix it (and add a default barcode for each sample).
	- Check if exists the Linker Primer header and fix it (and add a default linker primer for each sample).
	- Check if exists the Description header and fix it (and add a default description for each sample).
	- Check if there is any bad char in the sample id's and fix it.
	- Check if there is any bad char in any other field and fix it.
"""
script_info['script_usage'] = [("Example", "Generate a QIIME mapping file from a fastunifrac category mapping file (in this case category_map_file.txt)", "%prog -i category_map_file.txt")]
script_info['output_description'] = "A QIIME mapping file."
script_info['required_options'] = [
	make_option('-i', '--categ_map_fp', type="existing_filepath",
				help='category mapping file'),
]
script_info['optional_options'] = [
	make_option('-o', '--id_map_fp', type="new_filepath",
				help='id map file'),
]
script_info['version'] = __version__

if __name__ == '__main__':
	option_parser, opts, args = parse_command_line_parameters(**script_info)
	input_fp = opts.categ_map_fp
	output_fp = opts.id_map_fp

	convert_category_map_to_id_map(input_fp, output_fp)