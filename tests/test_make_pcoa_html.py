#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from cogent.util.unit_test import TestCase, main
from qiime.util import load_qiime_config
from os import path, mkdir
from shutil import rmtree
from fastunifrac.make_pcoa_html import (get_link_indexes, get_kinemage_link, get_html_links,
                                get_raw_pcoa_download_link, get_dict_links, get_html_table_links,
                                get_html_string, make_html_file)

class MakePcoaHtmlTest(TestCase):
    def setUp(self):
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        self.pcoa_dir = path.join(self.tmp_dir, 'pcoa_output')

        self.dict_links = {0:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d continuous coloring plots</a>""",
            1:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d discrete coloring plots</a>""",
            2:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d continuous coloring plots</a>""",
            3:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d discrete coloring plots</a>""",
            4:"""<a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a>""",
            5:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a>""",
            6:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a>"""}

        self._dirs_to_clean_up = []

    def tearDown(self):
        map(rmtree, self._dirs_to_clean_up)

    def _create_2d_directory(self, output_dir, name):
        dir_path = path.join(output_dir, name)
        mkdir(dir_path)

        js_path = path.join(dir_path, 'js')
        mkdir(js_path)
        f = open(path.join(js_path, 'overlib.js'), 'w+')
        f.close()

        random_path = path.join(dir_path, 'random_name')
        mkdir(random_path)
        f = open(path.join(random_path, 'PC1vsPC2.png'), 'w+')
        f.close()

        f = open(path.join(dir_path, 'weighted_unifrac_pc_2D_PCoA_plots.html'), 'w+')
        f.close()

    def _create_3d_directory(self, output_dir, name):
        dir_path = path.join(output_dir, name)
        mkdir(dir_path)

        jar_path = path.join(dir_path, 'jar')
        mkdir(jar_path)
        f = open(path.join(jar_path, 'king.jar'), 'w+')

        kin_dir = path.join(dir_path, 'random_name')
        mkdir(kin_dir)
        f = open(path.join(kin_dir, 'weighted_unifrac_pc.txt.kin'), 'w+')
        f.close()

        f = open(path.join(dir_path, 'weighted_unifrac_pc_3D_PCoA_plots.html'), 'w+')
        f.close()

    def _create_pcoa_output_structure(self, output_dir):
        mkdir(output_dir)
        self._create_2d_directory(output_dir, 'weighted_unifrac_2d_continuous')
        self._create_2d_directory(output_dir, 'weighted_unifrac_2d_discrete')
        self._create_3d_directory(output_dir, 'weighted_unifrac_3d_continuous')
        self._create_3d_directory(output_dir, 'weighted_unifrac_3d_discrete')

        f = open(path.join(output_dir, 'log_3564.txt'), 'w+')
        f.close()
        f = open(path.join(output_dir, 'prefs.txt'), 'w+')
        f.close()
        f = open(path.join(output_dir, 'weighted_unifrac_dm.txt'), 'w+')
        f.close()
        f = open(path.join(output_dir, 'weighted_unifrac_pc.txt'), 'w+')
        f.close()

    def test_get_link_indexes(self):
        obs_a, obs_b = get_link_indexes('weighted_unifrac_2d_continuous')
        exp_a = 0
        exp_b = None
        self.assertEqual(obs_a, exp_a)
        self.assertEqual(obs_b, exp_b)

        obs_a, obs_b = get_link_indexes('weighted_unifrac_2d_discrete')
        exp_a = 1
        exp_b = None
        self.assertEqual(obs_a, exp_a)
        self.assertEqual(obs_b, exp_b)

        obs_a, obs_b = get_link_indexes('weighted_unifrac_3d_continuous')
        exp_a = 2
        exp_b = 5
        self.assertEqual(obs_a, exp_a)
        self.assertEqual(obs_b, exp_b)

        obs_a, obs_b = get_link_indexes('weighted_unifrac_3d_discrete')
        exp_a = 3
        exp_b = 6
        self.assertEqual(obs_a, exp_a)
        self.assertEqual(obs_b, exp_b)

        self.assertRaises(ValueError, get_link_indexes, 'weighted_unifrac_bad_discrete')
        self.assertRaises(ValueError, get_link_indexes, 'weighted_unifrac_3d_bad')

    def test_get_kinemage_link(self):
        mkdir(self.pcoa_dir)
        self._dirs_to_clean_up = [self.pcoa_dir]

        name = 'weighted_unifrac_3d_discrete'
        p = path.join(self.pcoa_dir, name)
        index = 6
        self._create_3d_directory(self.pcoa_dir, name)
        obs = get_kinemage_link(p, name, index)
        exp = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a>"""
        self.assertEqual(obs, exp)

        name = 'weighted_unifrac_3d_continuous'
        p = path.join(self.pcoa_dir, name)
        index = 5
        self._create_3d_directory(self.pcoa_dir, name)
        obs = get_kinemage_link(p, name, index)
        exp = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a>"""
        self.assertEqual(obs, exp)

        self.assertRaises(ValueError, get_kinemage_link, p, name, 3)

        name = 'weighted_unifrac_2d_discrete'
        p = path.join(self.pcoa_dir, name)
        self._create_2d_directory(self.pcoa_dir, name)
        self.assertRaises(ValueError, get_kinemage_link, p, name, 5)

    def test_get_html_links(self):
        mkdir(self.pcoa_dir)
        self._dirs_to_clean_up = [self.pcoa_dir]

        name = 'weighted_unifrac_3d_discrete'
        p = path.join(self.pcoa_dir, name)
        self._create_3d_directory(self.pcoa_dir, name)
        obs_vi, obs_vl, obs_di, obs_dl = get_html_links(p, name)
        exp_vi = 3
        exp_vl = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d discrete coloring plots</a>"""
        exp_di = 6
        exp_dl = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a>"""
        self.assertEqual(obs_vi, exp_vi)
        self.assertEqual(obs_vl, exp_vl)
        self.assertEqual(obs_di, exp_di)
        self.assertEqual(obs_dl, exp_dl)

        name = 'weighted_unifrac_3d_continuous'
        p = path.join(self.pcoa_dir, name)
        self._create_3d_directory(self.pcoa_dir, name)
        obs_vi, obs_vl, obs_di, obs_dl = get_html_links(p, name)
        exp_vi = 2
        exp_vl = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d continuous coloring plots</a>"""
        exp_di = 5
        exp_dl = """<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a>"""
        self.assertEqual(obs_vi, exp_vi)
        self.assertEqual(obs_vl, exp_vl)
        self.assertEqual(obs_di, exp_di)
        self.assertEqual(obs_dl, exp_dl)

        name = 'weighted_unifrac_2d_discrete'
        p = path.join(self.pcoa_dir, name)
        self._create_2d_directory(self.pcoa_dir, name)
        obs_vi, obs_vl, obs_di, obs_dl = get_html_links(p, name)
        exp_vi = 1
        exp_vl = """<a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d discrete coloring plots</a>"""
        exp_di = None
        exp_dl = None
        self.assertEqual(obs_vi, exp_vi)
        self.assertEqual(obs_vl, exp_vl)
        self.assertEqual(obs_di, exp_di)
        self.assertEqual(obs_dl, exp_dl)

        name = 'weighted_unifrac_2d_continuous'
        p = path.join(self.pcoa_dir, name)
        self._create_2d_directory(self.pcoa_dir, name)
        obs_vi, obs_vl, obs_di, obs_dl = get_html_links(p, name)
        exp_vi = 0
        exp_vl = """<a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d continuous coloring plots</a>"""
        exp_di = None
        exp_dl = None
        self.assertEqual(obs_vi, exp_vi)
        self.assertEqual(obs_vl, exp_vl)
        self.assertEqual(obs_di, exp_di)
        self.assertEqual(obs_dl, exp_dl)

    def test_get_raw_pcoa_download_link(self):
        mkdir(self.pcoa_dir)
        self._dirs_to_clean_up = [self.pcoa_dir]

        name = 'weighted_unifrac_pc.txt'
        p = path.join(self.pcoa_dir, name)
        f = open(p, 'w+')
        f.close()

        obs = get_raw_pcoa_download_link(p, name)
        exp = """<a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a>"""
        self.assertEqual(obs, exp)

    def test_get_dict_links(self):
        self._create_pcoa_output_structure(self.pcoa_dir)
        self._dirs_to_clean_up = [self.pcoa_dir]

        obs = get_dict_links(self.pcoa_dir)
        exp = {0:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d continuous coloring plots</a>""",
            1:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d discrete coloring plots</a>""",
            2:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d continuous coloring plots</a>""",
            3:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d discrete coloring plots</a>""",
            4:"""<a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a>""",
            5:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a>""",
            6:"""<a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a>"""}

        self.assertEqual(obs, exp)

    def test_get_html_table_links(self):
        obs = get_html_table_links(self.dict_links)
        self.assertEqual(obs, exp_html_table_links)

    def test_get_html_string(self):
        self._create_pcoa_output_structure(self.pcoa_dir)
        self._dirs_to_clean_up = [self.pcoa_dir]
        
        obs = get_html_string(self.pcoa_dir)
        self.assertEqual(obs, exp_html_string)

exp_html_table_links = """<table cellpadding=1 cellspacing=1 border=1>
    <tr>
        <td class="header">PCoA</td>
    </tr>
    <tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a></td>
    </tr>

</table>
"""

exp_html_string = """<html>
    <head>
        <style type="text/css">
            .normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
            .header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
            .table_cell { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal; background-color:#EBD9B2;}
            .container { overflow: hidden;}
        </style>
        <title>Fastunifrac</title>
    </head>
    <body>
        <div>
            <table cellpadding=1 cellspacing=1 border=1>
    <tr>
        <td class="header">PCoA</td>
    </tr>
    <tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View weighted unifrac 2d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/weighted_unifrac_pc_3D_PCoA_plots.html">View weighted unifrac 3d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_continuous/random_name/weighted_unifrac_pc.txt.kin">Download kinemage continuous coloring file (Right click - Save as)</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_3d_discrete/random_name/weighted_unifrac_pc.txt.kin">Download kinemage discrete coloring file (Right click - Save as)</a></td>
    </tr>

</table>

        </div>
    </body>
</html>
"""

if __name__ == '__main__':
    main()
