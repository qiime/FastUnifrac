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
from fastunifrac.newick_to_asciiArt import make_interactive_sample_id_tree_file
import os

script_info = {}
script_info['brief_description'] = """Generates an html file with an ascii representation of a tree where de SampleIDs are interactive."""
script_info['script_description'] = """Takes a file with a tree in newick format and outputs a html file with an ascii representation of the tree and the SampleIDs are interactive, showing the description provided in the mapping file."""
script_info['script_usage'] = [("Example", "Generates an html file named 'tree_asciiArt_file.html' with the ascii representation of the tree stored at 'tree_newick_file.tre' in newick format.",
    "%prog -t tree_newick_file.tre -m mapping_file.txt -o tree_asciiArt_file.html --output_dir=output_dir")]
script_info['output_description'] = ""
script_info['required_options'] = [
    make_option('-t', '--tree_fp', type="existing_filepath",
                help='Tree file in newick format'),
    make_option('-m', '--mapping_fp', type="existing_filepath",
                help='Mapping file path'),
    make_option('-o', '--html_fp', type="new_filepath",
                help='HTML file path'),
    make_option('--output_dir', type="new_dirpath",
                help='Output directory which will contain the scripts for the html file')
]
script_info['optional_options'] = []
script_info['version'] = __version__

if __name__ == '__main__':
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    tree_path = opts.tree_fp
    mapping_path = opts.mapping_fp
    html_fp = opts.html_fp
    output_dir = opts.output_dir

    # Create output directory
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    # Parse the tree
    tree = parse_newick(open(tree_path, 'U'), PhyloNode)

    # Parse mapping file
    mapping_data = parse_mapping_file_to_dict(open(mapping_path, 'U'))

    # Generate the HTML file
    make_interactive_sample_id_tree_file(tree, mapping_data, html_fp, output_dir)
