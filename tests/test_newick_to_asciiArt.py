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
from qiime.parse import parse_newick, PhyloNode
from os import remove, path
from fastunifrac.newick_to_asciiArt import (asciiArt_length,
    get_tree_by_length_string, add_interactive_sample_id,
    make_interactive_sample_id_tree_file, get_formated_char_html,
    get_last_char_of_html_string, remove_first_chars_of_html_string,
    asciiArt_length_html, draw_jackknife_tree_html, get_legend_table_html,
    get_jackknife_tree_html_string, make_jackknife_tree_html_file)

class NewickToAsciiArtTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        self.newick = "((s1:0.2,s2:0.2):0.6,s3:0.8);"
        self.tree = parse_newick(self.newick, PhyloNode)

        self.newick_scaled = "((s1:25,s2:25):75,s3:100);"
        self.tree_scaled = parse_newick(self.newick_scaled, PhyloNode)
        self.tree_scaled.scaleBranchLengths(max_length=100, ultrametric=True)

        self.num_trees_considered = 10
        self.trans_values = {(None, None) : ("#FFFFFF", ""),
                        (None, 0.5): ("#dddddd", "< 50%"),
                        (0.5, 0.7): ("#99CCFF", "50-70%"),
                        (0.7, 0.9): ("#82FF8B", "70-90%"),
                        (0.9, 0.999): ("#F8FE83", "90-99.9%"),
                        (0.999, None): ("#FF8582", "> 99.9%")}

        self.jack_newick = "((s1:0.2,s2:0.2)0.8:0.6,s3:0.8)1.0;"
        self.jack_tree = parse_newick(self.jack_newick, PhyloNode)

        self.jack_newick_scaled = "((s1:25,s2:25)0.8:75,s3:100)1.0;"
        self.jack_tree_scaled = parse_newick(self.jack_newick_scaled, PhyloNode)
        self.jack_tree_scaled.scaleBranchLengths(max_length=100,
            ultrametric=True)

        self.support = { 'trees_considered': 10,
            'support_dict': {"node0":1.0,
                            "node1":0.8}}

        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.output_file = get_tmp_filename(tmp_dir = self.tmp_dir)

        dict_mapping_data = {}
        dict_mapping_data["s1"] = {
            'Description':'s1 test description',
            'NumIndividuals':'100',
            'BarcodeSequence':'AAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value1',
            'ExampleHeader2':'Val2'}
        dict_mapping_data["s2"] = {
            'Description':'s2 test description',
            'NumIndividuals':'200',
            'BarcodeSequence':'CAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value2',
            'ExampleHeader2':'Val1'}
        dict_mapping_data["s3"] = {
            'Description':'s3 test description',
            'NumIndividuals':'300',
            'BarcodeSequence':'GAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value2',
            'ExampleHeader2':'Val3'}

        self.mapping_data = [dict_mapping_data,
            "Example comment string for test"]

        self._paths_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)

    def test_asciiArt_length(self):
        """The ASCII lines are correct"""
        obs_lines, obs_mid = asciiArt_length(self.tree_scaled)

        exp_mid = 1

        self.assertEqual(obs_lines, exp_lines)
        self.assertEqual(obs_mid, exp_mid)

    def test_get_tree_by_length_string(self):
        """The ASCII string is correct"""
        obs_string = get_tree_by_length_string(self.tree)

        self.assertEqual(obs_string, exp_string)

    def test_add_interactive_sample_id(self):
        """The sample ID string is substituted by an HTML string correctly"""
        obs = add_interactive_sample_id(line_add_interactive_1,
            self.mapping_data, '>')
        self.assertEqual(obs, exp_add_interactive_1)

        obs = add_interactive_sample_id(line_add_interactive_2,
            self.mapping_data, '+')
        self.assertEqual(obs, exp_add_interactive_2)

    def test_get_formated_char_html(self):
        """The char is formated correctly"""
        c = '/'
        f = 0.4
        obs_string = get_formated_char_html(c, self.num_trees_considered, f,
            self.trans_values)
        self.assertEqual(obs_string, exp_get_formated_char_html_1)

        c = '|'
        f = 0.8
        obs_string = get_formated_char_html(c, self.num_trees_considered, f,
            self.trans_values)
        self.assertEqual(obs_string, exp_get_formated_char_html_2)

        c = '\\'
        f = 1.0
        obs_string = get_formated_char_html(c, self.num_trees_considered, f,
            self.trans_values)
        self.assertEqual(obs_string, exp_get_formated_char_html_3)

    def test_get_last_char_of_html_string(self):
        """The last char of an HTML string is retrieved correctly"""
        html_string = """Some chars<a href="#">|</a>"""
        obs_string = get_last_char_of_html_string(html_string)
        exp_string = """<a href="#">|</a>"""
        self.assertEqual(obs_string, exp_string)

        html_string = """<a href="#">|</a>Some chars"""
        obs_string = get_last_char_of_html_string(html_string)
        exp_string = "s"
        self.assertEqual(obs_string, exp_string)

        html_string = ""
        obs_string = get_last_char_of_html_string(html_string)
        exp_string = ""
        self.assertEqual(obs_string, exp_string)

    def test_remove_first_chars_of_html_string(self):
        """The chars are removed of an HTML string correctly"""
        html_string = """<a href="#">|</a>Some chars"""
        obs_string = remove_first_chars_of_html_string(html_string, 0)
        exp_string = """<a href="#">|</a>Some chars"""
        self.assertEqual(obs_string, exp_string)

        html_string = """<a href="#">|</a>Some chars"""
        obs_string = remove_first_chars_of_html_string(html_string, 1)
        exp_string = """Some chars"""
        self.assertEqual(obs_string, exp_string)

        html_string = """<a href="#">|</a>Some chars"""
        obs_string = remove_first_chars_of_html_string(html_string, 2)
        exp_string = """ome chars"""
        self.assertEqual(obs_string, exp_string)

        html_string = """Some chars<a href="#">|</a>"""
        obs_string = remove_first_chars_of_html_string(html_string, 1)
        exp_string = """ome chars<a href="#">|</a>"""
        self.assertEqual(obs_string, exp_string)

        html_string = """Some chars<a href="#">|</a>"""
        obs_string = remove_first_chars_of_html_string(html_string, 2)
        exp_string = """me chars<a href="#">|</a>"""
        self.assertEqual(obs_string, exp_string)

        html_string = """<a href="#">|</a>"""
        obs_string = remove_first_chars_of_html_string(html_string, 2)
        exp_string = ""
        self.assertEqual(obs_string, exp_string)

        html_string = ""
        obs_string = remove_first_chars_of_html_string(html_string, 1)
        exp_string = ""
        self.assertEqual(obs_string, exp_string)

    def test_asciiArt_length_html(self):
        """The HTML-ASCII lines are generated correctly"""
        obs_jack_lines, obs_mid = asciiArt_length_html(self.jack_tree_scaled,
            self.num_trees_considered, self.trans_values)

        exp_mid = 1

        self.assertEqual(obs_jack_lines, exp_jack_lines)
        self.assertEqual(obs_mid, exp_mid)

    def test_draw_jackknife_tree_html(self):
        """The HTML-ASCII string is correct"""
        obs_string = draw_jackknife_tree_html(self.jack_tree,
            self.num_trees_considered, self.trans_values, self.mapping_data)

        self.assertEqual(obs_string, exp_jack_string)

    def test_get_legend_table_html(self):
        """The HTML table with the legend is generated correctly"""
        obs_string = get_legend_table_html(self.trans_values)

        self.assertEqual(obs_string, exp_legend_string)

    def test_get_jackknife_tree_html_string(self):
        """The full HTML page is generated correctly"""
        obs_string = get_jackknife_tree_html_string(self.jack_tree,
            self.num_trees_considered, self.trans_values, self.mapping_data)

        self.assertEqual(obs_string, exp_html_string)

    def test_make_jackknife_tree_html_file(self):
        """The HTML file is generated in the right place"""
        self._paths_to_clean_up = [self.output_file,
            path.join(self.tmp_dir, 'overlib.js')]
        make_jackknife_tree_html_file(self.jack_tree, self.support,
            self.trans_values, self.mapping_data, self.output_file,
            self.tmp_dir)

        self.assertTrue(path.exists(self.output_file),
            'The html file was not created in the appropiate location')
        self.assertTrue(path.exists(path.join(self.tmp_dir, 'overlib.js')),
            'The javascript file was not moved in the appropiate location')

#########################
# Long string variables #
#########################

line_add_interactive_1 = '  /------------------------------------------------------------------------- /------------------------>s1'
line_add_interactive_2 = """  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">/</font></a>------------------------------------------------------------------------- <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">/</font></a>------------------------+s1"""

exp_add_interactive_1 = """  /------------------------------------------------------------------------- /------------------------&#62;<a href="#" onmouseover="return overlib('<b>Sample ID:</b> s1<br><b>Description:</b> s1 test description');" onmouseout="return nd();">s1</a>"""
exp_add_interactive_2 = """  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">/</font></a>------------------------------------------------------------------------- <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">/</font></a>------------------------&#62;<a href="#" onmouseover="return overlib('<b>Sample ID:</b> s1<br><b>Description:</b> s1 test description');" onmouseout="return nd();">s1</a>"""

exp_get_formated_char_html_1 = """<a href="#" onmouseover="return overlib('<b>Jackknife Count:</b> 4.000<br><b>Jackknife Fraction:</b> 0.400');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#dddddd">/</font></a>"""
exp_get_formated_char_html_2 = """<a href="#" onmouseover="return overlib('<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">|</font></a>"""
exp_get_formated_char_html_3 = """<a href="#" onmouseover="return overlib('<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">\\</font></a>"""

exp_lines = ['  /------------------------------------------------------------------------- /------------------------>s1',
'-|                                                                           \\------------------------>s2',
'  \\--------------------------------------------------------------------------------------------------->s3']

exp_string = ['Scale: 1 dash, slash, backslash ~ 0.0080 branch length units',
'  /------------------------------------------------------------------------- /------------------------>s1',
'-|                                                                           \\------------------------>s2',
'  \\--------------------------------------------------------------------------------------------------->s3']

exp_jack_lines = ['  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">/</font></a>------------------------------------------------------------------------- <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">/</font></a>------------------------+s1',
'-<a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">|</font></a>                                                                           <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">\\</font></a>------------------------+s2',
'  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">\\</font></a>---------------------------------------------------------------------------------------------------+s3']

exp_jack_string = """<pre>Scale: 1 dash, slash, backslash ~ 0.0080 branch length units<br>
  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">/</font></a>------------------------------------------------------------------------- <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">/</font></a>------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s1<br><b>Description:</b> s1 test description\');" onmouseout="return nd();">s1</a>
-<a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">|</font></a>                                                                           <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">\\</font></a>------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s2<br><b>Description:</b> s2 test description\');" onmouseout="return nd();">s2</a>
  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">\\</font></a>---------------------------------------------------------------------------------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s3<br><b>Description:</b> s3 test description\');" onmouseout="return nd();">s3</a>\n</pre>"""

exp_legend_string = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Color description</td></tr>
<tr>
<td class="normal" bgcolor="#dddddd" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">&#60; 50%</td>
</tr>
<tr>
<td class="normal" bgcolor="#99CCFF" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">50-70%</td>
</tr>
<tr>
<td class="normal" bgcolor="#82FF8B" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">70-90%</td>
</tr>
<tr>
<td class="normal" bgcolor="#F8FE83" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">90-99.9%</td>
</tr>
<tr>
<td class="normal" bgcolor="#FF8582" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">&#62; 99.9%</td>
</tr>

</table>
<br>
"""

exp_html_string = """
<html>
<head>
<title>Fastunifrac</title>
<script type="text/javascript" src="overlib.js"></script>
<style type="text/css">
.normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
.header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
.row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
</style>
</head>
<body>
<pre>Scale: 1 dash, slash, backslash ~ 0.0080 branch length units<br>
  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">/</font></a>------------------------------------------------------------------------- <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">/</font></a>------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s1<br><b>Description:</b> s1 test description\');" onmouseout="return nd();">s1</a>
-<a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">|</font></a>                                                                           <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 8.000<br><b>Jackknife Fraction:</b> 0.800\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#82FF8B">\\</font></a>------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s2<br><b>Description:</b> s2 test description\');" onmouseout="return nd();">s2</a>
  <a href="#" onmouseover="return overlib(\'<b>Jackknife Count:</b> 10.000<br><b>Jackknife Fraction:</b> 1.000\');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:#FF8582">\\</font></a>---------------------------------------------------------------------------------------------------&#62;<a href="#" onmouseover="return overlib(\'<b>Sample ID:</b> s3<br><b>Description:</b> s3 test description\');" onmouseout="return nd();">s3</a>
</pre><table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Color description</td></tr>
<tr>
<td class="normal" bgcolor="#dddddd" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">&#60; 50%</td>
</tr>
<tr>
<td class="normal" bgcolor="#99CCFF" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">50-70%</td>
</tr>
<tr>
<td class="normal" bgcolor="#82FF8B" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">70-90%</td>
</tr>
<tr>
<td class="normal" bgcolor="#F8FE83" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">90-99.9%</td>
</tr>
<tr>
<td class="normal" bgcolor="#FF8582" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">&#62; 99.9%</td>
</tr>

</table>
<br>

</body>
</html>
"""

if __name__ == '__main__':
    main()