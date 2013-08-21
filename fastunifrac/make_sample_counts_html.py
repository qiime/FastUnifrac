#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.parse import parse_mapping_file_to_dict

ROW_TABLE_HTML = """<tr>
    <td class="row_header">%s</td>
    <td class="table_cell">%s</td>
    <td class="table_cell">%s</td>
</tr>
"""

TABLE_HTML = """<table cellpadding=3 cellspacing=3 border=1>
<tr><td colspan=3 class="header">Sample counts</td></tr>
<tr>
    <td class="header">Sample ID</td>
    <td class="header">Count</td>
    <td class="header">Description</td>
</tr>
%s
</table>
<br>
"""

PAGE_HTML = """
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
%s
    </body>
</html>
"""

def get_html_table(map_dict):
    table_rows = ""
    total = 0.0
    for key in map_dict.keys():
        table_rows += ROW_TABLE_HTML % (key, map_dict[key]['NumIndividuals'], map_dict[key]['Description'])
        total += float(map_dict[key]['NumIndividuals'])
    table_rows += ROW_TABLE_HTML % ('Total', int(total), '')
    return TABLE_HTML % table_rows

def get_html_page_string(map_dict):
    """
        map_dict: 
    """
    table_html = get_html_table(map_dict)

    return PAGE_HTML % table_html

def make_html_file(lines, html_fp):
    """
        lines:
        html_fp:
    """
    # Parse the mapping file
    (map_dict, list_c) = parse_mapping_file_to_dict(lines)

    # Generate the string containing the html code
    page_html_string = get_html_page_string(map_dict)

    #Save the html file
    out = open(html_fp, 'w')
    out.write(page_html_string)
    out.close()