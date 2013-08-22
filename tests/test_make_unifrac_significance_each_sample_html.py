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
from os import remove, path
from fastunifrac.make_unifrac_significance_each_sample_html import (
    get_html_table, get_html_legend_table, get_html_page_string, make_html_file)

class MakeUnifracSignificanceEachSampleHtmlTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.output_file = get_tmp_filename(tmp_dir = self.tmp_dir)

        self.d_data = {'s1':(0.005, 0.08),
            's2':(0.0, 0.01),
            's3':(0.02, 0.3),
            's4':(0.82, 1.0)}

        self.title_0 = "Example title: 0"
        self.title_1 = "Example title: 1"

        self.name = "Example name"

        self._paths_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)

    def test_get_html_table(self):
        """The HTML table is correct"""
        obs = get_html_table(self.d_data, self.title_0, 0)
        self.assertEqual(obs, exp_html_table_0)

        obs = get_html_table(self.d_data, self.title_1, 1)
        self.assertEqual(obs, exp_html_table_1)

        self.assertRaises(ValueError, get_html_table,
            self.d_data, self.title_1, 2)

    def test_get_html_legend_table(self):
        """The HTML table for the legend is correct"""
        obs = get_html_legend_table()
        self.assertEqual(obs, exp_html_legend_table)

    def test_get_html_page_string(self):
        """The HTML page is correct"""
        obs = get_html_page_string(self.d_data, self.name)
        self.assertEqual(obs, exp_html_page)

    def test_make_html_file(self):
        """The HTML file is created in the right position"""
        self._paths_to_clean_up = [self.output_file]

        make_html_file(self.d_data, self.name, self.output_file)
        self.assertTrue(path.exists(self.output_file),
            'The html file was not created in the appropiate location')
        

exp_html_table_0 = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Example title: 0</td></tr>
<tr>
    <td class="header">Sample</td>
    <td class="header" nowrap>P Value</td>
</tr>
<tr>
<td class="row_header">s1</td>
<td class="normal" bgcolor="#F8FE83" nowrap>0.005</td>
</tr>
<tr>
<td class="row_header">s2</td>
<td class="normal" bgcolor="#FF8582" nowrap>0.0</td>
</tr>
<tr>
<td class="row_header">s3</td>
<td class="normal" bgcolor="#82FF8B" nowrap>0.02</td>
</tr>
<tr>
<td class="row_header">s4</td>
<td class="normal" bgcolor="#dddddd" nowrap>0.82</td>
</tr>

</table>
<br>
"""

exp_html_table_1 = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Example title: 1</td></tr>
<tr>
    <td class="header">Sample</td>
    <td class="header" nowrap>P Value</td>
</tr>
<tr>
<td class="row_header">s1</td>
<td class="normal" bgcolor="#99CCFF" nowrap>0.08</td>
</tr>
<tr>
<td class="row_header">s2</td>
<td class="normal" bgcolor="#F8FE83" nowrap>0.01</td>
</tr>
<tr>
<td class="row_header">s3</td>
<td class="normal" bgcolor="#dddddd" nowrap>0.3</td>
</tr>
<tr>
<td class="row_header">s4</td>
<td class="normal" bgcolor="#dddddd" nowrap>1.0</td>
</tr>

</table>
<br>
"""

exp_html_legend_table = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Color description</td></tr>
<tr>
<td class="normal" bgcolor="#FF8582" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(<0.001) Highly significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#F8FE83" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.001-0.01) Significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#82FF8B" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.01-0.05) Marginally significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#99CCFF" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.05-0.1) Suggestive</td>
</tr>
<tr>
<td class="normal" bgcolor="#dddddd" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(>0.1) Not significant</td>
</tr>

</table>
<br>
"""

exp_html_page = """
<html>
    <head>
        <style type="text/css">
            .normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
            .header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
            .row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
            .float_left { width: 33%; float: left;}
            .container { overflow: hidden;}
        </style>
    <title>Fastunifrac</title>
    </head>
    <body>
        <div class="container">
            <div class="float_left">
            <table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Example name: Raw values</td></tr>
<tr>
    <td class="header">Sample</td>
    <td class="header" nowrap>P Value</td>
</tr>
<tr>
<td class="row_header">s1</td>
<td class="normal" bgcolor="#F8FE83" nowrap>0.005</td>
</tr>
<tr>
<td class="row_header">s2</td>
<td class="normal" bgcolor="#FF8582" nowrap>0.0</td>
</tr>
<tr>
<td class="row_header">s3</td>
<td class="normal" bgcolor="#82FF8B" nowrap>0.02</td>
</tr>
<tr>
<td class="row_header">s4</td>
<td class="normal" bgcolor="#dddddd" nowrap>0.82</td>
</tr>

</table>
<br>

            </div>
            <div class="float_left">
            <table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Example name: Corrected values</td></tr>
<tr>
    <td class="header">Sample</td>
    <td class="header" nowrap>P Value</td>
</tr>
<tr>
<td class="row_header">s1</td>
<td class="normal" bgcolor="#99CCFF" nowrap>0.08</td>
</tr>
<tr>
<td class="row_header">s2</td>
<td class="normal" bgcolor="#F8FE83" nowrap>0.01</td>
</tr>
<tr>
<td class="row_header">s3</td>
<td class="normal" bgcolor="#dddddd" nowrap>0.3</td>
</tr>
<tr>
<td class="row_header">s4</td>
<td class="normal" bgcolor="#dddddd" nowrap>1.0</td>
</tr>

</table>
<br>

            </div>
            <div class="float_left">
            <table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Color description</td></tr>
<tr>
<td class="normal" bgcolor="#FF8582" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(<0.001) Highly significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#F8FE83" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.001-0.01) Significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#82FF8B" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.01-0.05) Marginally significant</td>
</tr>
<tr>
<td class="normal" bgcolor="#99CCFF" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(0.05-0.1) Suggestive</td>
</tr>
<tr>
<td class="normal" bgcolor="#dddddd" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">(>0.1) Not significant</td>
</tr>

</table>
<br>

            </div>
        </div>
    </body>
</html>
"""

if __name__ == '__main__':
    main()