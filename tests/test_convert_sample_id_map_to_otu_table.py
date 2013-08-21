#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

import json
from cogent.util.unit_test import TestCase, main
from biom.table import SparseOTUTable, dict_to_sparsedict
from biom.parse import generatedby
from fastunifrac.convert_sample_id_map_to_otu_table import convert

class SampleIdMapToOtuTableParserTest(TestCase):
    def setUp(self):
        self.sample_id_map_lines = sample_id_map_correct.split('\n')
        self.otu_ids = ['111', '222', '333']
        self.sample_ids = ['S1', 'S2', 'S3']
        self.two_d_dict = {(0, 0):76.0,
                (0, 1):43.0,
                (1, 0):23.0,
                (1, 1):84.0,
                (2, 2):46.0}
        self.data = dict_to_sparsedict(self.two_d_dict)
        self.table_obj = SparseOTUTable(Data=self.data,
            SampleIds=self.sample_ids, ObservationIds=self.otu_ids,
            SampleMetadata=None, ObservationMetadata=None)

        self.sample_id_map_lines_bad_chars = sample_id_map_bad_char_sample_id.split('\n')
        self.sample_ids_bad_chars = ['S.1', 'S.2', 'S.3']
        self.data = dict_to_sparsedict(self.two_d_dict)
        self.table_obj_bad_chars = SparseOTUTable(Data=self.data,
            SampleIds=self.sample_ids_bad_chars, ObservationIds=self.otu_ids,
            SampleMetadata=None, ObservationMetadata=None)

        self.sample_id_map_lines_2_cols = sample_id_map_2_cols.split('\n')
        self.two_d_dict_2_cols = {(0, 0):1.0,
                (0, 1):1.0,
                (1, 0):1.0,
                (1, 1):1.0,
                (2, 2):1.0}
        self.data_2_cols = dict_to_sparsedict(self.two_d_dict_2_cols)
        self.table_obj_2_cols = SparseOTUTable(Data=self.data_2_cols,
            SampleIds = self.sample_ids, ObservationIds=self.otu_ids,
            SampleMetadata=None, ObservationMetadata=None)

    def test_convert(self):
        obs = convert(self.sample_id_map_lines)
        exp = self.table_obj.getBiomFormatJsonString(generatedby())
        self.assertEqualOtuTable(obs, exp)

        sample_id_map_lines = sample_id_map_wrong.split('\n')
        self.assertRaises(ValueError, convert, sample_id_map_lines)

        obs = convert(self.sample_id_map_lines_bad_chars)
        exp = self.table_obj_bad_chars.getBiomFormatJsonString(generatedby())
        self.assertEqualOtuTable(obs, exp)

        obs = convert(self.sample_id_map_lines_2_cols)
        exp = self.table_obj_2_cols.getBiomFormatJsonString(generatedby())
        self.assertEqualOtuTable(obs, exp)

    def assertEqualOtuTable(self,obs,exp):
        obs = json.loads(obs)
        exp = json.loads(exp)
        for e in ['generated_by', 'date']:
            del obs[e]
            del exp[e]
        self.assertEqual(obs,exp)

        

sample_id_map_correct="""111    S1  76
111 S2  43
222 S1  23
222 S2  84
333 S3  46
"""

sample_id_map_2_cols="""111 S1
111 S2
222 S1
222 S2
333 S3
"""

sample_id_map_wrong="""111 S1
111 S2
222 S1
222 S2
333 S3
"""

sample_id_map_bad_char_sample_id="""111 S#1 76
111 S#2 43
222 S#1 23
222 S#2 84
333 S#3 46
"""

if __name__ == '__main__':
    main()
