# -----------------------------------------------------------------------------
# Copyright (c) 2013, The FastUnifrac Development Team.
#
# Distributed under the terms of the GPLv2 License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from biom import load_table
from biom.util import compute_counts_per_sample_stats
from qiime.parse import parse_mapping_file
from qiime.check_id_map import write_corrected_mapping


def add_counts_to_mapping(biom_fp, map_fp, qualitative, output_fp):
    """Adds the seqs/OTUs counts to the mapping file

    Parameters
    ----------
    biom_fp : str
        Path to the biom table
    map_fp : str
        Path to the mapping file
    qualitative : bool
        If True, present counts as number of unique observation ids per
        sample, rather than counts of observations per sample.
    output_fp : str
        Path to the output mapping file
    """
    # Parse biom file
    biom = load_table(biom_fp)
    # Parse mapping file
    with open(map_fp, 'U') as map_lines:
        map_data, headers, comments = parse_mapping_file(map_lines)

    # Compute the counts per sample
    min_count, max_count, median_count, mean_count, counts_per_sample =\
        compute_counts_per_sample_stats(biom, binary_counts=qualitative)

    # Add the counts to the mapping data
    index = len(headers) - 1
    headers.insert(index, "NumIndividuals")
    for row in map_data:
        row.insert(index, str(counts_per_sample[row[0]]))

    # Write the corrected mapping file
    write_corrected_mapping(output_fp, headers, comments, map_data)
