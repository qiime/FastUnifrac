#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from fastunifrac.make_heatmap import get_matrix_value

""" Html code adapted from Micah Hamady's Fastunifrac code """

DICT_TRANS_VALUES = {(None, None): ("#FFFFFF", ""),
                     (None, 0.001): ("#FF8582", "(<0.001) Highly significant"),
                     (0.001, 0.01): ("#F8FE83", "(0.001-0.01) Significant"),
                     (0.01, 0.05): ("#82FF8B", "(0.01-0.05) Marginally significant"),
                     (0.05, 0.1): ("#99CCFF", "(0.05-0.1) Suggestive"),
                     (0.1, None): ("#dddddd", "(>0.1) Not significant")}

ROW_TABLE_HTML = """<tr>
<td class="row_header">%s</td>
<td class="normal" bgcolor="%s" nowrap>%s</td>
</tr>
"""

TABLE_HTML = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">%s</td></tr>
<tr>
    <td class="header">Sample</td>
    <td class="header" nowrap>P Value</td>
</tr>
%s
</table>
<br>
"""

ROW_TABLE_LEGEND_HTML = """<tr>
<td class="normal" bgcolor="%s" nowrap>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td class="row_header">%s</td>
</tr>
"""

TABLE_LEGEND_HTML = """<table cellpadding=2 cellspacing=2 border=1>
<tr> <td colspan=2 class="header">Color description</td></tr>
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
            .float_left { width: 33%%; float: left;}
            .container { overflow: hidden;}
        </style>
    <title>Fastunifrac</title>
    </head>
    <body>
        <div class="container">
            <div class="float_left">
            %s
            </div>
            <div class="float_left">
            %s
            </div>
            <div class="float_left">
            %s
            </div>
        </div>
    </body>
</html>
"""


def get_html_table(d_data, title, index):
    """Get the HTML table with the p values colored by significance

    Inputs:
        d_data: dict of: {sample: (p value, p value corrected)}
        title: string which contains the table title
        index: 0 indicates p value and 1 indicates p value corrected

    Returns a string which contains the html code of a table where the p values
        are colored by significance.
    """
    # Check the index is in the expected range
    if index != 0 and index != 1:
        raise ValueError, "Index must be 0 or 1!"
    # Sort the sample names
    sorted_samples = d_data.keys()
    sorted_samples.sort()
    # Generate the HTML string with the rows code
    rows = ''
    for sample in sorted_samples:
        v = d_data[sample][index]
        c = get_matrix_value(v, DICT_TRANS_VALUES)
        rows += ROW_TABLE_HTML % (sample, c, v)
    # Generate the HTML string with the table code
    return TABLE_HTML % (title, rows)


def get_html_legend_table():
    """Get the HTML table with the color legend"""
    # Sort the ranges
    sorted_keys = DICT_TRANS_VALUES.keys()
    sorted_keys.sort()
    # Generate the HTML string with the rows code
    rows = ''
    for key in sorted_keys[1:]:
        color = DICT_TRANS_VALUES[key][0]
        desc = DICT_TRANS_VALUES[key][1]
        rows += ROW_TABLE_LEGEND_HTML % (color, desc)
    # Generate the HTML string with the table code
    return TABLE_LEGEND_HTML % (rows)


def get_html_page_string(d_data, test_name):
    """Creates the full HTML string of the page

    Inputs:
        d_data: dict of: {sample: (p value, p value corrected)}
        test_name: string which contains the name of the test realized

    Returns a string which contains the full page html code.
    """
    # Get the table with the raw values
    raw_table = get_html_table(d_data, test_name + ": Raw values", 0)
    # Get the table with the corrected values
    corrected_table = get_html_table(
        d_data, test_name + ": Corrected values", 1)
    # Get the table with the color legend
    leg_table = get_html_legend_table()
    # Return the string with the full page html code
    return PAGE_HTML % (raw_table, corrected_table, leg_table)


def make_html_file(d_data, test_name, html_fp):
    """Creates the HTML file with the unifrac significance results

    Inputs:
        d_data: dict of: {sample: (p value, p value corrected)}
        test_name: string which contains the name of the test realized
        html_fp: file path where the html file will be created

    Generates the html file with the unifrac results colored by significance
    """
    # Generate the html string
    page_html_string = get_html_page_string(d_data, test_name)
    # Save the html file
    out = open(html_fp, 'w')
    out.write(page_html_string)
    out.close()
