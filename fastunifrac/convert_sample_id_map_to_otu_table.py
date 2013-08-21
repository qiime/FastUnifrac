#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas", ]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from fastunifrac.check_id_map import sample_id_filter, filename_has_space
from os.path import splitext, split
from biom.table import SparseOTUTable, dict_to_sparsedict
from biom.parse import generatedby

def convert(lines):
    """
        lines: sample id mapping file file

        Returns the OTU Table Json string of the sample id mapping file 'lines'
    """
    otu_ids = []
    sample_ids = []
    two_d_dict = {} #{(row, col):value}, row is otu

    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                try:
                    sec_id, sample_id, times = line.split('\t')
                except ValueError:
                    try:
                        sec_id, sample_id = line.split('\t')
                        times = 1
                    except ValueError:
                        raise ValueError,("The sample ID mapping file must be a tab delimited file where first column is sequence ID, the second column is sample ID and the third column is the number of times the sequence was oserved.")
                if not sec_id in otu_ids:
                    otu_ids.append(sec_id)
                sample_id, e = sample_id_filter.resultAndError(sample_id)
                if not sample_id in sample_ids:
                    sample_ids.append(sample_id)
                two_d_dict[(otu_ids.index(sec_id),sample_ids.index(sample_id))] = float(times)

    data = dict_to_sparsedict(two_d_dict)
    table_obj = SparseOTUTable(Data=data,
        SampleIds=sample_ids, ObservationIds=otu_ids,
        SampleMetadata=None, ObservationMetadata=None)

    return table_obj.getBiomFormatJsonString(generatedby())

def convert_sample_id_map_to_otu_table(input_fp, output_fp):
    fpath, ext = splitext(input_fp)
    input_dir, fname = split(fpath)

    #Check it the file name contains spaces and fix it, in case we'll need it
    fname, err = filename_has_space(fname)

    if output_fp:
        #Check if the output file name contains spaces and fix it
        output_fp, err = filename_has_space(output_fp)
    else:
        output_fp = fname + "_corrected.biom"

    #Check if it's possible to create the output file
    try:
        outf = open(output_fp, 'w')
    except IOError:
        print "Unable to create corrected output file " + output_fp
        quit()

    inf = open(input_fp, 'U')

    biom_otu_table = convert(inf)

    outf.write(biom_otu_table)

    inf.close()
    outf.close()