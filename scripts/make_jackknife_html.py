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
from qiime.parse import parse_newick, PhyloNode, parse_mapping_file_to_dict
from fastunifrac.newick_to_asciiArt import make_jackknife_tree_html_file
from fastunifrac.parse import parse_jackknife_support_file
import os

script_info = {}
script_info['brief_description'] = """Generates a html file with the result tree of jackknife."""
script_info['script_description'] = """Takes the Jackknife support file and the Jackknife named nodes tree and generates a html file showing the tree colored by Jackknife fraction."""
script_info['script_usage'] = [("Example", "Generate a html file named 'index.html' with the the Jackknife tree represented in 'jackknife_named_nodes.tre' colored by Jackknife fraction stored in 'jackknife_support.txt'.",
    "%prog -s jackknife_support -t jackknife_named_nodes.tre -m mapping_file.txt -o index.html --output_dir=output_directory")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-s', '--support_fp', type="existing_filepath",
                help='Jackknife support filepath'),
    make_option('-t', '--tree_fp', type="existing_filepath",
                help='Jackknife named nodes tree filepath'),
    make_option('-m', '--mapping_fp', type="existing_filepath",
                help='Mapping file path'),
    make_option('-o', '--output_html_fp', type="new_filepath",
                help='Html filepath'),
    make_option('--output_dir', type="new_dirpath",
                help='Output directory which will contains scripts and images')
]
script_info['optional_options'] = []
script_info['version'] = __version__

# Dict which contains the color legend
DICT_TRANS_VALUES = {(None, None) : ("#FFFFFF", ""),
            (None, 0.5): ("#dddddd", "< 50%"),
            (0.5, 0.7): ("#99CCFF", "50-70%"),
            (0.7, 0.9): ("#82FF8B", "70-90%"),
            (0.9, 0.999): ("#F8FE83", "90-99.9%"),
            (0.999, None): ("#FF8582", "> 99.9%")}

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    support_fp = opts.support_fp
    tree_fp = opts.tree_fp
    mapping_fp = opts.mapping_fp
    html_fp = opts.output_html_fp
    output_dir = opts.output_dir

    # Create output directory
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    # Parse jackknife support file
    support = parse_jackknife_support_file(open(support_fp, 'U'))

    # Parse jackknife named nodes tree file
    tree = parse_newick(open(tree_fp, 'U'), PhyloNode)

    # Parse mapping file
    mapping_data = parse_mapping_file_to_dict(open(mapping_fp, 'U'))

    # Generate the html file
    make_jackknife_tree_html_file(tree, support, DICT_TRANS_VALUES, mapping_data, html_fp, output_dir)