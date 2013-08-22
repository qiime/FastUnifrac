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
from fastunifrac.add_counts_to_mapping import add_counts_to_mapping

script_info = {}
script_info['brief_description'] = "Adds sequence/OTU counts to a mapping file"
script_info['script_description'] = "Computes the sequence/OTU counts and\
 adds it to the mapping file in a new column called NumIndividuals"
script_info['script_usage'] = [
    ("Example", "Count the number of sequences per sample present in " + \
        "'otu_table.biom' and add this counts to 'mapping_file.txt'", 
        "%prog -i otu_table.biom -m mapping_file.txt -o mapping_w_counts.txt"),
    ("Example", "Count the number of OTUs per sample present in " + \
        "'otu_table.biom' and add this counts to 'mapping_file.txt'", 
        "%prog -i otu_table.biom -m mapping_file.txt --otu_counts " + \
        "-o mapping_w_counts.txt")
    ]
script_info['output_description'] = "The mapping file with the counts added"
script_info['required_options'] = [
    make_option('-i', '--input_fp', type="existing_filepath",
                help='Biom table filepath'),
    make_option('-m', '--mapping_fp', type="existing_filepath",
                help='Mapping file filepath'),
    make_option('-o', '--output_fp', type="new_filepath",
                help='Output mapping filepath')
]
script_info['optional_options'] = [
    make_option('--otu_counts', action='store_true', default=False,
        help='Counts are presented as number of observed OTUs per sample, ' + 
            'rather than counts of sequences per sample [default: %default]')
]
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    biom_fp = opts.input_fp
    mapping_fp = opts.mapping_fp
    output_fp = opts.output_fp
    otu_counts = opts.otu_counts

    add_counts_to_mapping(open(biom_fp, 'U'), open(mapping_fp, 'U'), otu_counts,
        output_fp)