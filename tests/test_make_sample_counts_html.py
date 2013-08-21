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
from fastunifrac.make_sample_counts_html import get_html_table, get_html_page_string, make_html_file
from os import remove, path

class MakeSampleCountsHtmlTest(TestCase):
    def setUp(self):
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'

        self.map_dict = {}
        self.map_dict["SampleID1"] = {'Description':'SampleID1 test description',
                                    'NumIndividuals':'100',
                                    'BarcodeSequence':'AAAAAAAAAACT',
                                    'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
                                    'ExampleHeader1':'Value1',
                                    'ExampleHeader2':'Val2'}
        self.map_dict["SampleID2"] = {'Description':'SampleID2 test description',
                                    'NumIndividuals':'200',
                                    'BarcodeSequence':'AAAAAAAAAGCT',
                                    'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
                                    'ExampleHeader1':'Value2',
                                    'ExampleHeader2':'Val2'}
        self.map_dict["SampleID3"] = {'Description':'SampleID3 test description',
                                    'NumIndividuals':'300',
                                    'BarcodeSequence':'ACGAAAAAAACT',
                                    'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
                                    'ExampleHeader1':'Value1',
                                    'ExampleHeader2':'Val1'}

        self.mapping_file_lines = mapping_file_lines.splitlines()

        self._paths_to_clean_up = []

    def tearDown(self):
        map(remove, self._paths_to_clean_up)

    def test_get_html_table(self):
        obs = get_html_table(self.map_dict)
        self.assertEqual(obs, exp_get_html_table)

    def test_get_html_page_string(self):
        obs = get_html_page_string(self.map_dict)
        self.assertEqual(obs, exp_get_html_page_string)

    def test_make_html_file(self):
        html_fp = get_tmp_filename(tmp_dir = self.tmp_dir)
        make_html_file(self.mapping_file_lines, html_fp)
        self.assertTrue(path.exists(html_fp), 'The html file was not created in the appropiate location')

exp_get_html_table = """<table cellpadding=3 cellspacing=3 border=1>
<tr><td colspan=3 class="header">Sample counts</td></tr>
<tr>
    <td class="header">Sample ID</td>
    <td class="header">Count</td>
    <td class="header">Description</td>
</tr>
<tr>
    <td class="row_header">SampleID2</td>
    <td class="table_cell">200</td>
    <td class="table_cell">SampleID2 test description</td>
</tr>
<tr>
    <td class="row_header">SampleID3</td>
    <td class="table_cell">300</td>
    <td class="table_cell">SampleID3 test description</td>
</tr>
<tr>
    <td class="row_header">SampleID1</td>
    <td class="table_cell">100</td>
    <td class="table_cell">SampleID1 test description</td>
</tr>
<tr>
    <td class="row_header">Total</td>
    <td class="table_cell">600</td>
    <td class="table_cell"></td>
</tr>

</table>
<br>
"""

exp_get_html_page_string = """
<html>
    <head>
        <style type="text/css">
            .normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
            .header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
            .row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
            .table_cell { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal; background-color:#EBD9B2;}
        </style>
        <title>FastUniFrac</title>
    </head>
    <body>
<table cellpadding=3 cellspacing=3 border=1>
<tr><td colspan=3 class="header">Sample counts</td></tr>
<tr>
    <td class="header">Sample ID</td>
    <td class="header">Count</td>
    <td class="header">Description</td>
</tr>
<tr>
    <td class="row_header">SampleID2</td>
    <td class="table_cell">200</td>
    <td class="table_cell">SampleID2 test description</td>
</tr>
<tr>
    <td class="row_header">SampleID3</td>
    <td class="table_cell">300</td>
    <td class="table_cell">SampleID3 test description</td>
</tr>
<tr>
    <td class="row_header">SampleID1</td>
    <td class="table_cell">100</td>
    <td class="table_cell">SampleID1 test description</td>
</tr>
<tr>
    <td class="row_header">Total</td>
    <td class="table_cell">600</td>
    <td class="table_cell"></td>
</tr>

</table>
<br>

    </body>
</html>
"""

mapping_file_lines = """#SampleID\tBarcodeSequence\tLinkerPrimerSequence\tNumIndividuals\tExampleHeader1\tExampleHeader2\tDescription
#Sample mapping file for testing
SampleID1\tAAAAAAAAAACT\tAAAAAAAAAAAAAAAAAAAAA\t100\tValue1\tVal2\tSampleID1 test description
SampleID2\tAAAAAAAAAGCT\tAAAAAAAAAAAAAAAAAAAAA\t200\tValue2\tVal2\tSampleID2 test description
SampleID3\tACGAAAAAAACT\tAAAAAAAAAAAAAAAAAAAAA\t300\tValue1\tVal1\tSampleID3 test description
"""

if __name__ == '__main__':
    main()