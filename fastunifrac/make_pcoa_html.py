#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from os.path import join, isdir, isfile
from os import listdir

PCOA_2D_CONTINUOUS_INDEX = 0
PCOA_2D_DISCRETE_INDEX = 1
PCOA_3D_INDEX = 2
RAW_DATA_INDEX = 3

PCOA_STRING = "View %s coloring plots"
RAW_DATA_STRING = "Download raw PCoA data (Right click - Save as)"

LINK_HTML = """<a class="table_cell" target="_blank" href="%s">%s</a>"""

ROW_TABLE_HTML = """<tr>
        <td class="table_cell">%s</td>
    </tr>
"""

TABLE_HTML = """<table cellpadding=1 cellspacing=1 border=1>
    <tr>
        <td class="header">PCoA</td>
    </tr>
    %s
</table>
"""

PAGE_HTML = """<html>
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
            %s
        </div>
    </body>
</html>
"""

def get_dict_links(pcoa_dir):
    """
        pcoa_dir: PCoA output directory

        Returns dict of: {index: html_link}
            where:
                index: sets the index order to show the link
                html_link: string which contains the html link
    """
    # Get a list of (path, name) with the PCoA directory content
    dir_content = [(join(pcoa_dir, content), content) for content in listdir(pcoa_dir)]

    links = {}
    for path, name in dir_content:
        if isdir(path):
            if name != 'emperor_required_resources':
                # It is one of the folders containing the 2d plots
                split_name = name.split('_')
                if split_name[-1] == 'discrete':
                    index = PCOA_2D_DISCRETE_INDEX
                elif split_name[-1] == 'continuous':
                    index = PCOA_2D_CONTINUOUS_INDEX
                else:
                    raise ValueError, 'Wrong PCoA directory structure'
                # Search for the html file with the 2d plots
                for content in listdir(path):
                    f = join(path, content)
                    if isfile(f):
                        # This is the html file
                        str_link = PCOA_STRING % (' '.join(split_name))
                        link = LINK_HTML % (join(name, content), str_link)
                        break
                links[index] = link
        else:
            if name == "index.html":
                # This is the Emperor html file - 3d plots
                str_link = PCOA_STRING % 'unifrac 3d'
                links[PCOA_3D_INDEX] = LINK_HTML % (name, str_link)
            else:
                # Check if it is the principal coordinates file
                if name.split('_')[-1] == 'pc.txt':
                    links[RAW_DATA_INDEX] = LINK_HTML % (name, RAW_DATA_STRING)
    return links

def get_html_table_links(links_dict):
    """
        links_dict: dict of: {index: html_link}
            where:
                index: sets the index order to show the link
                html_link: string which contains the html link

        Returns a string which contains all the html links in links_dict
            orderer by their indexes.
    """
    sorted_keys = links_dict.keys()
    sorted_keys.sort()

    html_rows_string = ""
    for key in sorted_keys:
        html_rows_string += ROW_TABLE_HTML % links_dict[key]

    return TABLE_HTML % html_rows_string

def get_html_string(pcoa_dir):
    """
        pcoa_dir: PCoA output directory

        Returns a string which contains the full page html code.
    """
    # Get a dict of {index, link} with the html links
    links = get_dict_links(pcoa_dir)

    # Get the html string with all the links ordered by index
    html_table_links_string = get_html_table_links(links)

    # Return the string with the full page html code
    return PAGE_HTML % (html_table_links_string)

def make_html_file(pcoa_dir, html_fp):
    """
        pcoa_dir: PCoA output directory
        html_fp: file path to store the output html page

        Generates the html file.
    """ 
    # Get the html string
    html_string = get_html_string(pcoa_dir)

    # Save the html file
    out = open(html_fp, 'w')
    out.write(html_string)
    out.close()