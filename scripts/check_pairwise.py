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
from qiime.parse import parse_mapping_file

# Limits from fastunifrac by Hamady.
PAIRWISE_LIMITS = {
    '50':2,
    '100':3,
    '500':7,
    '750':9,
    '1000':10
}

script_info = {}
script_info['brief_description'] = """Checks if the maximum number of samples\
 for 0.05 significance with a given population is not exceeded."""
script_info['script_description'] = """Specifically, the maximum number of\
 samples and for fixed populations sizes are:
\tPopulation\tMax samples
\t50\t\t2
\t100\t\t3
\t500\t\t7
\t750\t\t9
\t1000\t\t10
"""
script_info['script_usage'] = [
    ("Example","","%prog -i category_map.txt -p 50 -o output_file.txt")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-i', '--category_map_fp', type='existing_filepath',
        help='FastUniFrac category mapping file'),
    make_option('-p', '--population', type='choice',
        choices=sorted(PAIRWISE_LIMITS.keys()),
        help='Population size. Available values: %s' % \
            sorted(PAIRWISE_LIMITS.keys())),
    make_option('-o', '--output_fp', type='new_filepath',
        help='Output file path')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    map_fp = opts.category_map_fp
    population = opts.population
    out_fp = opts.output_fp

    mapf = open(map_fp, 'U')
    outf = open(out_fp, 'w');

    mapping_data, header, comments = parse_mapping_file(mapf)
    sample_counts = len(mapping_data)

    if PAIRWISE_LIMITS[population] < sample_counts:
        outf.write("The maximum number of samples for 0.05 significance with" +
            " population %s is %d: (%d given)\n" % (population,
                PAIRWISE_LIMITS[population], sample_counts))
        outf.close()
        mapf.close()
        exit(1)

    outf.write("Ok")
    outf.close()
    mapf.close()