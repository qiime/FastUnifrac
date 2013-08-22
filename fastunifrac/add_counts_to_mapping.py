#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from biom.util import compute_counts_per_sample_stats
from biom.parse import parse_biom_table
from qiime.parse import parse_mapping_file
from convert_category_map_to_id_map import write_corrected_file

def add_counts_to_mapping(biom_lines, mapping_lines, otu_counts, output_fp):
    """Counts the number of seqs/OTUs per sample and add its to the mapping file

    Inputs:
        biom_lines:
        mapping_lines:
        otu_counts:
        output_fp:
    """
    # Parse biom file
    biom = parse_biom_table(biom_lines)
    # Parse mapping file
    map_data, headers, comments = parse_mapping_file(mapping_lines)
    # Compute the counts per sample
    min_count, max_count, median_count, mean_count, counts_per_sample =\
        compute_counts_per_sample_stats(biom, binary_counts=otu_counts)
    # Add the counts to the mapping data
    index = len(headers) - 1
    headers.insert(index, "NumIndividuals")
    for row in map_data:
        row.insert(index, str(counts_per_sample[row[0]]))
    # Add the '#' character to the first header
    headers[0] = '#' + headers[0]
    # Add headers to the data
    map_data.insert(0, headers)
    # Write the corrected mapping file
    write_corrected_file(map_data, comments, output_fp)