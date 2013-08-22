#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from qiime.util import load_qiime_config, get_tmp_filename
from os import remove
from fastunifrac.add_counts_to_mapping import add_counts_to_mapping

class AddCountsToMappingTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        # Get the tmp folder
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        # Initialize some variables
        self.biom_table = biom_table.splitlines()
        self.mapping = mapping_file.splitlines()
        self._paths_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)

    def test_add_counts_to_mapping(self):
        """NumIndividuals is added to the mapping file"""
        # Get the output filepath
        out_fp = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='.txt')
        # Add the output filepath to clean variable
        self._paths_to_clean_up = [out_fp]
        # Perform the test
        add_counts_to_mapping(self.biom_table, self.mapping, False, out_fp)
        f = open(out_fp, 'U')
        obs = f.readlines()
        f.close()
        self.assertEqual(obs, exp_mapping_file_seqs.splitlines(True))
        # Get the output filepath
        out_fp = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='.txt')
        # Add the output filepath to clean variable
        self._paths_to_clean_up.append(out_fp)
        # Perform the test
        add_counts_to_mapping(self.biom_table, self.mapping, True, out_fp)
        f = open(out_fp, 'U')
        obs = f.readlines()
        f.close()
        self.assertEqual(obs, exp_mapping_file_otu.splitlines(True))

mapping_file = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample3
"""

exp_mapping_file_seqs = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tNumIndividuals\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\t4.0\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\t2.0\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\t2.0\tDescription of sample3
"""

exp_mapping_file_otu = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tNumIndividuals\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\t2\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\t1\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\t1\tDescription of sample3
"""

biom_table = """{"id": "None","format": "Biological Observation Matrix 1.0.0",\
"format_url": "http://biom-format.org","type": "OTU table","generated_by": \
"FastUnifrac software","date": "2013-08-21T18:55:44.872736","matrix_type": \
"sparse","matrix_element_type": "float","shape": [2, 3],"data": [[0,0,3.0],\
[0,2,2.0],[1,0,1.0],[1,1,2.0]],"rows": [{"id": "OTU1", "metadata": null},\
{"id": "OTU2", "metadata": null}],"columns": [{"id": "sample1", "metadata": \
null},{"id": "sample2", "metadata": null},{"id": "sample3", "metadata": \
null}]}"""

if __name__ == '__main__':
    main()