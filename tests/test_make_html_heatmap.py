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
from fastunifrac.make_heatmap import plot_heatmap
from qiime.util import load_qiime_config, get_tmp_filename
from os import path, remove, mkdir, rmdir
from fastunifrac.make_html_heatmap import (get_coords, generate_xmap,
    make_html_file, get_html_table_string, get_html_page_string, LD_NAME,
    LD_HEADERS, LD_HEADERS_VER, LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES,
    LD_TABLE_TITLE)

class MakeHtmlHeatmapTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'

        data = {}
        data[LD_NAME] = get_tmp_filename(tmp_dir="", suffix='').replace("\"","")

        headers = {}
        headers[LD_HEADERS_VER] = ["Sample1", "Sample2", "Sample3", "Sample4"]
        headers[LD_HEADERS_HOR] = ["Sample1", "Sample2", "Sample3", "Sample4"]
        data[LD_HEADERS] = headers

        matrix = [[None, 0.1, 0.9, 0.5],
                    [None, None, 0.8, 0.7],
                    [None, None, None, 0.4],
                    [None, None, None, None]]
        data[LD_MATRIX] = matrix

        trans_values = {}
        trans_values[(None, None)] = (0, "")
        trans_values[(0.0, 0.25)] = (1, "(0-25%)")
        trans_values[(0.25, 0.5)] = (2, "(25-50%)")
        trans_values[(0.5, 0.75)] = (3, "(50-75%)")
        trans_values[(0.75, 1.0)] = (4, "(75-100%)")
        data[LD_TRANSFORM_VALUES] = trans_values
        data[LD_TABLE_TITLE] = "Example table title"

        self.html_fp = path.join(self.tmp_dir, data[LD_NAME] + '.html')
        self.output_dir = path.join(self.tmp_dir, data[LD_NAME])

        self.list_data_single_plot = [data]

        data1 = {}
        data1[LD_NAME] = get_tmp_filename(tmp_dir="",suffix='').replace("\"","")
        data1[LD_HEADERS] = headers
        data1[LD_MATRIX] = matrix
        data1[LD_TRANSFORM_VALUES] = trans_values
        data1[LD_TABLE_TITLE] = "Example table title"

        self.list_data_multiple_plots = [data, data1]

        dict_mapping_data = {}
        dict_mapping_data["Sample1"] = {
            'Description':'Sample1 test description',
            'NumIndividuals':'100',
            'BarcodeSequence':'AAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value1',
            'ExampleHeader2':'Val2'
            }
        dict_mapping_data["Sample2"] = {
            'Description':'Sample2 test description',
            'NumIndividuals':'200',
            'BarcodeSequence':'CAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value2',
            'ExampleHeader2':'Val1'
            }
        dict_mapping_data["Sample3"] = {
            'Description':'Sample3 test description',
            'NumIndividuals':'300',
            'BarcodeSequence':'GAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value2',
            'ExampleHeader2':'Val3'
            }
        dict_mapping_data["Sample4"] = {
            'Description':'Sample4 test description',
            'NumIndividuals':'400',
            'BarcodeSequence':'TAAAAAAAAACT',
            'LinkerPrimerSequence':'AAAAAAAAAAAAAAAAAAAAA',
            'ExampleHeader1':'Value3',
            'ExampleHeader2':'Val1'
            }
        self.mapping_data = [dict_mapping_data, 
            "Example comment string for test"]

        self._paths_to_clean_up = []
        self._dirs_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(remove, self._paths_to_clean_up)
        map(rmdir, self._dirs_to_clean_up)

    def test_get_coords(self):
        """The XY coords for the AREA tag are retrieved correctly"""
        data = self.list_data_single_plot[0]

        plot_output_dir = path.join(self.tmp_dir, "plot_dir")
        png_img_fp = path.join(plot_output_dir, data[LD_NAME] + '.png')
        eps_gz_fp = path.join(plot_output_dir, data[LD_NAME] + '.eps.gz')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp]
        self._dirs_to_clean_up = [plot_output_dir]

        mkdir(plot_output_dir)

        width, height, plot = plot_heatmap(data[LD_NAME], data[LD_HEADERS],
            data[LD_MATRIX], data[LD_TRANSFORM_VALUES], plot_output_dir)

        all_cids, all_xcoords, all_ycoords = get_coords(data[LD_HEADERS],
            data[LD_MATRIX], plot, self.mapping_data)

        result_all_xcoords = [354.0, 466.0, 578.0, 466.0, 578.0, 578.0]
        result_all_ycoords = [664.0, 664.0, 664.0, 552.0, 552.0, 440.0]

        self.assertEqual(all_cids, result_all_cids)
        self.assertEqual(all_xcoords, result_all_xcoords)
        self.assertEqual(all_ycoords, result_all_ycoords)

    def test_generate_xmap(self):
        """The AREA tag is generated correctly"""
        data = self.list_data_single_plot[0]

        plot_output_dir = path.join(self.tmp_dir, "plot_dir")
        png_img_fp = path.join(plot_output_dir, data[LD_NAME] + '.png')
        eps_gz_fp = path.join(plot_output_dir, data[LD_NAME] + '.eps.gz')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp]
        self._dirs_to_clean_up = [plot_output_dir]

        mkdir(plot_output_dir)

        width, height, plot = plot_heatmap(data[LD_NAME], data[LD_HEADERS],
            data[LD_MATRIX], data[LD_TRANSFORM_VALUES], plot_output_dir)

        xmap, img_height, img_width = generate_xmap(width, height,
            data[LD_HEADERS], data[LD_MATRIX], plot, self.mapping_data)

        self.assertEqual(img_height, 800)
        self.assertEqual(img_width, 800)
        self.assertEqual(xmap, result_xmap)

    def test_get_html_table_string(self):
        """The HTML table is correct"""
        data = self.list_data_single_plot[0]

        png_img_fp = path.join(self.output_dir, data[LD_NAME] + '.png')
        eps_gz_fp = path.join(self.output_dir, data[LD_NAME] + '.eps.gz')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp]
        self._dirs_to_clean_up = [self.output_dir]

        mkdir(self.output_dir)

        html_table_string = get_html_table_string(data, self.mapping_data,
            self.output_dir)

        self.assertEqual(html_table_string, result_html_table_string % \
            (data[LD_NAME], data[LD_NAME], data[LD_NAME], data[LD_NAME]))
        self.assertTrue(path.exists(png_img_fp),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp),
            'The eps file was not created in the appropiate location')

    def test_get_html_page_string(self):
        """The HTML page is correct"""
        data = self.list_data_single_plot[0]
        data1 = self.list_data_multiple_plots[1]

        png_img_fp = path.join(self.output_dir, data[LD_NAME] + '.png')
        eps_gz_fp = path.join(self.output_dir, data[LD_NAME] + '.eps.gz')
        png_img_fp1 = path.join(self.output_dir, data1[LD_NAME] + '.png')
        eps_gz_fp1 = path.join(self.output_dir, data1[LD_NAME] + '.eps.gz')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp, png_img_fp1,
            eps_gz_fp1]
        self._dirs_to_clean_up = [self.output_dir]

        mkdir(self.output_dir)

        html_page_string = get_html_page_string(self.list_data_single_plot,
            self.mapping_data, self.output_dir)

        self.assertEqual(html_page_string, 
            result_html_page_string_single_plot % (data[LD_NAME], data[LD_NAME],
                data[LD_NAME], data[LD_NAME]))
        self.assertTrue(path.exists(png_img_fp),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp),
            'The eps file was not created in the appropiate location')

        html_page_string = get_html_page_string(self.list_data_multiple_plots,
            self.mapping_data, self.output_dir)

        self.assertEqual(html_page_string, 
            result_html_page_string_multiple_plot % (
                self.list_data_multiple_plots[0][LD_NAME],
                self.list_data_multiple_plots[0][LD_NAME],
                self.list_data_multiple_plots[0][LD_NAME],
                self.list_data_multiple_plots[0][LD_NAME],
                self.list_data_multiple_plots[1][LD_NAME],
                self.list_data_multiple_plots[1][LD_NAME],
                self.list_data_multiple_plots[1][LD_NAME],
                self.list_data_multiple_plots[1][LD_NAME]))
        self.assertTrue(path.exists(png_img_fp),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp),
            'The eps file was not created in the appropiate location')
        self.assertTrue(path.exists(png_img_fp1),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp1),
            'The eps file was not created in the appropiate location')

    def test_make_html_file(self):
        """The HTML file is generated in the correct place"""
        data = self.list_data_multiple_plots[0]
        data1 = self.list_data_multiple_plots[1]

        png_img_fp = path.join(self.output_dir, data[LD_NAME] + '.png')
        eps_gz_fp = path.join(self.output_dir, data[LD_NAME] + '.eps.gz')
        png_img_fp1 = path.join(self.output_dir, data1[LD_NAME] + '.png')
        eps_gz_fp1 = path.join(self.output_dir, data1[LD_NAME] + '.eps.gz')
        overlib_fp = path.join(self.output_dir, 'overlib.js')

        self._paths_to_clean_up = [png_img_fp, eps_gz_fp, png_img_fp1,
            eps_gz_fp1, overlib_fp, self.html_fp]
        self._dirs_to_clean_up = [self.output_dir]

        mkdir(self.output_dir)

        make_html_file(self.list_data_multiple_plots, self.mapping_data,
            self.html_fp, self.output_dir)

        self.assertTrue(path.exists(png_img_fp),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp),
            'The eps file was not created in the appropiate location')
        self.assertTrue(path.exists(png_img_fp1),
            'The png file was not created in the appropiate location')
        self.assertTrue(path.exists(eps_gz_fp1),
            'The eps file was not created in the appropiate location')
        self.assertTrue(path.exists(overlib_fp),
            'The overlib.js file was not copied in the appropiate location')
        self.assertTrue(path.exists(self.html_fp),
            'The html file was not created in the appropiate location')

result_all_cids = [
'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description',
'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description',
'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description',
'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description',
'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description',
'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description'
]

result_xmap = ['<AREA shape="circle" coords="354,136,15" href="#<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description\');" onmouseout="return nd();">\n',
'<AREA shape="circle" coords="466,136,15" href="#<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">\n',
'<AREA shape="circle" coords="578,136,15" href="#<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">\n', 
'<AREA shape="circle" coords="466,248,15" href="#<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">\n', 
'<AREA shape="circle" coords="578,248,15" href="#<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">\n', 
'<AREA shape="circle" coords="578,360,15" href="#<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">\n']

result_html_table_string = """<table cellpading=0 cellspacing=0 border=1>
<tr><th align=center colspan=3 border=0 class="header">Example table title</th></tr>
<tr>
<td class="normal" align=center border=0><img src="%s.png" border="0" ismap usemap="#points%s" width="800" height="800" />

<MAP name="points%s">
<AREA shape="circle" coords="354,136,15" href="#<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,136,15" href="#<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,136,15" href="#<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,248,15" href="#<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,248,15" href="#<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,360,15" href="#<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">

</MAP>
<br><a href="%s.eps.gz" >Download Figure</a></td>
</tr>
</table>
<br><br>"""

result_html_page_string_single_plot = """
<html>
<head>
<style type="text/css">
.normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
.header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
.row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
</style>
<script type="text/javascript" src="overlib.js"></script>
<title>Fastunifrac</title>
</head>
<body>
<div id="overDiv" style="position:absolute; visibility:hidden; z-index:1000;"></div>
<table cellpading=0 cellspacing=0 border=1>
<tr><th align=center colspan=3 border=0 class="header">Example table title</th></tr>
<tr>
<td class="normal" align=center border=0><img src="%s.png" border="0" ismap usemap="#points%s" width="800" height="800" />

<MAP name="points%s">
<AREA shape="circle" coords="354,136,15" href="#<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,136,15" href="#<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,136,15" href="#<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,248,15" href="#<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,248,15" href="#<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,360,15" href="#<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">

</MAP>
<br><a href="%s.eps.gz" >Download Figure</a></td>
</tr>
</table>
<br><br>
</body>
</html>
"""

result_html_page_string_multiple_plot = """
<html>
<head>
<style type="text/css">
.normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
.header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
.row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
</style>
<script type="text/javascript" src="overlib.js"></script>
<title>Fastunifrac</title>
</head>
<body>
<div id="overDiv" style="position:absolute; visibility:hidden; z-index:1000;"></div>
<table cellpading=0 cellspacing=0 border=1>
<tr><th align=center colspan=3 border=0 class="header">Example table title</th></tr>
<tr>
<td class="normal" align=center border=0><img src="%s.png" border="0" ismap usemap="#points%s" width="800" height="800" />

<MAP name="points%s">
<AREA shape="circle" coords="354,136,15" href="#<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,136,15" href="#<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,136,15" href="#<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,248,15" href="#<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,248,15" href="#<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,360,15" href="#<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">

</MAP>
<br><a href="%s.eps.gz" >Download Figure</a></td>
</tr>
</table>
<br><br><table cellpading=0 cellspacing=0 border=1>
<tr><th align=center colspan=3 border=0 class="header">Example table title</th></tr>
<tr>
<td class="normal" align=center border=0><img src="%s.png" border="0" ismap usemap="#points%s" width="800" height="800" />

<MAP name="points%s">
<AREA shape="circle" coords="354,136,15" href="#<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample2:</b> 0.1<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample2:</i> Sample2 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,136,15" href="#<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample3:</b> 0.9<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,136,15" href="#<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample1 vs Sample4:</b> 0.5<br><br><i>Sample1:</i> Sample1 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="466,248,15" href="#<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample3:</b> 0.8<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample3:</i> Sample3 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,248,15" href="#<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample2 vs Sample4:</b> 0.7<br><br><i>Sample2:</i> Sample2 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">
<AREA shape="circle" coords="578,360,15" href="#<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description"  onmouseover="return overlib(\'<b>Sample3 vs Sample4:</b> 0.4<br><br><i>Sample3:</i> Sample3 test description<br><br><i>Sample4:</i> Sample4 test description\');" onmouseout="return nd();">

</MAP>
<br><a href="%s.eps.gz" >Download Figure</a></td>
</tr>
</table>
<br><br>
</body>
</html>
"""

if __name__ == '__main__':
    main()