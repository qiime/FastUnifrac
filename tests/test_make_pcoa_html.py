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
from os import mkdir
from os.path import join, exists
from shutil import rmtree
from fastunifrac.make_pcoa_html import (get_dict_links, get_html_table_links,
    get_html_string, make_html_file)

class MakePcoaHtmlTest(TestCase):
    def setUp(self):
        """Set up some test variables"""
        # Get the temp folder
        self.qiime_config = load_qiime_config()
        self.tmp_dir = self.qiime_config['temp_dir'] or '/tmp/'
        # Initialize some variables
        self.dict_links = {
            0:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d continuous coloring plots</a>""",
            1:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d discrete coloring plots</a>""",
            2:"""<a class="table_cell" target="_blank" href="index.html">View 3d plots</a>""",
            3:"""<a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a>"""
        }
        self._dirs_to_clean_up = []

    def tearDown(self):
        """Cleans up the environment once the tests finish"""
        map(rmtree, self._dirs_to_clean_up)

    def _create_2d_directory(self, output_dir, name):
        """Creates the directory structure of the 2d plots"""
        # Create base dir
        dir_path = join(output_dir, name)
        mkdir(dir_path)
        # Add the overlib.js file
        js_path = join(dir_path, 'js')
        mkdir(js_path)
        f = open(join(js_path, 'overlib.js'), 'w')
        f.close()
        # Add the directory with the plot images
        random_path = get_tmp_filename(tmp_dir=dir_path, suffix='')
        mkdir(random_path)
        f = open(join(random_path, 'PC1vsPC2.png'), 'w')
        f.close()
        # Add the html file
        f = open(join(dir_path, 'weighted_unifrac_pc_2D_PCoA_plots.html'), 'w')
        f.close()

    def _create_pcoa_output_structure(self, output_dir):
        """Creates the directory structure of the PCoA analysis"""
        # Create base dir
        mkdir(output_dir)
        # Create 2d plots structure for continuous and discrete coloring 
        self._create_2d_directory(output_dir, 'weighted_unifrac_2d_continuous')
        self._create_2d_directory(output_dir, 'weighted_unifrac_2d_discrete')
        # Create the log file
        f = open(get_tmp_filename(tmp_dir=output_dir, prefix='log_',
            suffix='.txt'), 'w')
        f.close()
        # Create the prefs.txt file
        f = open(join(output_dir, 'prefs.txt'), 'w')
        f.close()
        # Create the distance matrix file
        f = open(join(output_dir, 'weighted_unifrac_dm.txt'), 'w')
        f.close()
        # Create the principal coordinate file
        f = open(join(output_dir, 'weighted_unifrac_pc.txt'), 'w')
        f.close()
        # Create the index.html file from Emperor
        f = open(join(output_dir, 'index.html'), 'w')
        f.close()
        # Create the 'emperor_required_resources' folder
        mkdir(join(output_dir, 'emperor_required_resources'))

    def test_get_dict_links(self):
        """The links dict is retrieved correctly"""
        # Generate the PCoA output directory structure
        pcoa_dir = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='')
        self._create_pcoa_output_structure(pcoa_dir)
        # Add the PCoA output to the cleaning paths
        self._dirs_to_clean_up = [pcoa_dir]
        # Perform the test 
        obs_links, obs_title = get_dict_links(pcoa_dir)
        exp_links = {
            0:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d continuous coloring plots</a>""",
            1:"""<a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d discrete coloring plots</a>""",
            2:"""<a class="table_cell" target="_blank" href="index.html">View 3d plots</a>""",
            3:"""<a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a>"""
        }
        self.assertEqual(obs_links, exp_links)
        self.assertEqual(obs_title, "weighted unifrac")

    def test_get_html_table_links(self):
        """The HTML table string is generated correctly"""
        obs = get_html_table_links(self.dict_links, "weighted unifrac")
        self.assertEqual(obs, exp_html_table_links)

    def test_get_html_string(self):
        """The HTML string is generated correctly"""
        # Generate the PCoA output directory
        pcoa_dir = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='')
        self._create_pcoa_output_structure(pcoa_dir)
        # Add the PCoA output to the cleaning paths
        self._dirs_to_clean_up = [pcoa_dir]
        # Perform the test
        obs = get_html_string(pcoa_dir)
        self.assertEqual(obs, exp_html_string)

    def test_make_html_file(self):
        """The HTML file is stored in the correct location"""
        # Generate the PCoA output directory
        pcoa_dir = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='')
        self._create_pcoa_output_structure(pcoa_dir)
        # Add the PCoA output to the cleaning paths
        self._dirs_to_clean_up = [pcoa_dir]
        # Perform the test
        html_fp = get_tmp_filename(tmp_dir=self.tmp_dir, suffix='.html')
        make_html_file(pcoa_dir, html_fp)
        self.assertTrue(exists(html_fp))

exp_html_table_links = """<table cellpadding=1 cellspacing=1 border=1>
    <tr>
        <td class="header">PCoA - weighted unifrac</td>
    </tr>
    <tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="index.html">View 3d plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a></td>
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
        <td class="header">PCoA - weighted unifrac</td>
    </tr>
    <tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_continuous/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d continuous coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_2d_discrete/weighted_unifrac_pc_2D_PCoA_plots.html">View 2d discrete coloring plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="index.html">View 3d plots</a></td>
    </tr>
<tr>
        <td class="table_cell"><a class="table_cell" target="_blank" href="weighted_unifrac_pc.txt">Download raw PCoA data (Right click - Save as)</a></td>
    </tr>

</table>

        </div>
    </body>
</html>
"""

if __name__ == '__main__':
    main()
