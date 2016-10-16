# -----------------------------------------------------------------------------
# Copyright (c) 2013, The FastUnifrac Development Team.
#
# Distributed under the terms of the GPLv2 License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main
from tempfile import mkstemp
from os import close, remove

from biom import Table
from biom.util import biom_open

from fastunifrac.add_counts_to_mapping import add_counts_to_mapping


class AddCountsToMappingTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        fd, self.biom_fp = mkstemp(suffix='.biom')
        close(fd)
        table = Table([[0, 0, 3.0], [0, 2, 2.0], [1, 0, 1.0], [1, 1, 2.0]],
                      ["OTU1", "OTU2"], ["sample1", "sample2", "sample3"])
        with biom_open(self.biom_fp, 'w') as f:
            table.to_hdf5(f, "example")

        fd, self.map_fp = mkstemp(suffix=".txt")
        close(fd)
        with open(self.map_fp, 'w') as f:
            f.write(mapping_file)

        self._paths_to_clean_up = [self.biom_fp, self.map_fp]

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)

    def test_add_counts_to_mapping(self):
        """NumIndividuals is added to the mapping file"""
        # Get the output filepath
        fd, out_fp = mkstemp(suffix=".txt")
        close(fd)
        self._paths_to_clean_up.append(out_fp)

        add_counts_to_mapping(self.biom_fp, self.map_fp, False, out_fp)
        with open(out_fp, 'U') as f:
            obs = f.read()
        self.assertEqual(obs, exp_mapping_file_seqs)

        fd, out_fp = mkstemp(suffix=".txt")
        close(fd)
        self._paths_to_clean_up.append(out_fp)
        add_counts_to_mapping(self.biom_fp, self.map_fp, True, out_fp)
        with open(out_fp, 'U') as f:
            obs = f.read()
        self.assertEqual(obs, exp_mapping_file_otu)

mapping_file = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\tDescription of sample3
"""

exp_mapping_file_seqs = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\
\tNumIndividuals\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\t4.0\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\t2.0\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\t2.0\tDescription of sample3
"""

exp_mapping_file_otu = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\
\tNumIndividuals\tDescription
#Comments
#One comment more
sample1\tAAAAAAAAAAAA\tAAAAAAAAAAAAAAAAAAAAA\t2\tDescription of sample1
sample2\tAAAAAAAAAAAC\tAAAAAAAAAAAAAAAAAAAAA\t1\tDescription of sample2
sample3\tAAAAAAAAAAAG\tAAAAAAAAAAAAAAAAAAAAA\t1\tDescription of sample3
"""

if __name__ == '__main__':
    main()
