#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from make_heatmap import get_matrix_value
from shutil import copyfile
import os
from os.path import join, dirname

# overlib.js path
OVERLIB_JS = "support_files/overlib.js"

"""Html code adapted from Micah Hamady's code at Fastunifrac website"""

INTERACTIVE_ID_HTML = """<a href="#" onmouseover="return overlib('<b>Sample ID:</b> %s<br><b>Description:</b> %s');" onmouseout="return nd();">%s</a>"""

FORMATED_HTML = """<a href="#" onmouseover="return overlib('<b>Jackknife Count:</b> %.3f<br><b>Jackknife Fraction:</b> %.3f');" onmouseout="return nd();"><font style="BACKGROUND-COLOR:%s">%s</font></a>"""

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
<title>Fastunifrac</title>
<script type="text/javascript" src="overlib.js"></script>
<style type="text/css">
.normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
.header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
.row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
</style>
</head>
<body>
%s
</body>
</html>
"""

def asciiArt_length(tree, char1='-'):
    """
        tree: cluster samples tree
        char1: first char to use in the current branch

        Returns:
            result: list containing the strings which represents the tree rooted
                at 'tree'
            mid: integer which means the middle line of 'result'
    """
    LEN = tree.Length or 2
    if tree.Children:
        result = []
        mids = []
        for child in tree.Children:
            if child is tree.Children[0]:
                char2 = '/'
            elif child is tree.Children[-1]:
                char2 = '\\'
            else:
                char2 = '-'
            (child_lines, child_mid) = asciiArt_length(child, char2)
            mids.append(len(result) + child_mid)
            result.extend(child_lines)
        low_mid = mids[0]
        high_mid = mids[-1]
        mid = (high_mid + low_mid) / 2
        space_str = ' ' * LEN
        space_pipe_str = ' ' * (LEN - 1) + '|'
        prefixes = [space_str] * (low_mid + 1) + [space_pipe_str] * (high_mid - 
            low_mid - 1) + [space_str] * (len(result) - high_mid)
        if LEN < 2:
            prefixes[mid] = char1
        else:
            prefixes[mid] = char1 + '-' * (LEN - 2) + prefixes[mid][-1]
        result = [ p + l for (p, l) in zip(prefixes, result)]
        return (result, mid)
    else:
        return ([char1 + '-' * (LEN - 1) + '>' + tree.Name], 0)

def get_tree_by_length_string(tree):
    """
        tree: cluster samples tree

        Returns a string wich contains a representation of the cluster samples
        tree.
    """
    unscaled_max_length = max([node.Length for node in tree.tips()])
    tree.scaleBranchLengths(max_length=100, ultrametric=True)
    scaled_max_length = max([node.Length for node in tree.tips()])
    branch_scale = float(unscaled_max_length) / scaled_max_length

    (lines, mid) = asciiArt_length(tree)
    output = []
    output.append("Scale: 1 dash, slash, backslash ~ %.4f branch length units" %
        branch_scale)
    output.extend(lines)
    return output

def add_interactive_sample_id(line, mapping_data, separator):
    before, sep, after = line.partition(separator)
    return before + "&#62;" + INTERACTIVE_ID_HTML % (after,
        mapping_data[0][after]['Description'], after)

def make_interactive_sample_id_tree_file(tree, mapping_data, html_fp,
    output_dir):
    tree_lines = get_tree_by_length_string(tree)
    tree_html_lines = [tree_lines[0] + "<br>"]
    tree_html_lines.extend([add_interactive_sample_id(line, mapping_data, '>')
        for line in tree_lines[1:]])

    html_lines = ["<pre>"]
    html_lines.extend(tree_html_lines)
    html_lines.append("</pre>")

    tree_text_html = PAGE_HTML % "\n".join(html_lines)

    # Move 'overlib.js' to the output_dir
    overlib_js_fp = join(dirname(__file__), OVERLIB_JS)
    copyfile(overlib_js_fp, os.path.join(output_dir, "overlib.js"))

    # Save the html file
    outf = open(html_fp, 'w')
    outf.write(tree_text_html)
    outf.close()

#####################################################################
#  Functions to get a html file with a representation of Jackknifed #
#  tree colored by Jackknife fraction                               #
#####################################################################

def get_formated_char_html(char, num_trees_considered, fraction, trans_values):
    """
        char: character to format
        num_trees_considered: number of trees used for the jackknife
        fraction: jackknife fraction of the node that represented by 'char'
        trans_values: dict of: {(val1, val2): (html_color, label)}

        Returns an html string which applies background color to the
            char and add a message showing the jackknife count and fraction
            when the mouse is over the char.
    """
    fraction = float(fraction)
    count = num_trees_considered * fraction
    color = get_matrix_value(fraction, trans_values)
    return FORMATED_HTML % (count, fraction, color, char)

def get_last_char_of_html_string(html_string):
    """
        html_string: string which contains the html code to modify

        Returns the last char of 'html_string' but taking in account
        the html tags
    """
    if len(html_string) == 0:
        return ""
    if html_string[-1] == ">":
        left, sep, right = html_string.rpartition("<a")
        return sep + right
    return html_string[-1]

def remove_first_chars_of_html_string(html_string, num_chars):
    """
        html_string: string which contains the html code to modify
        num_chars: number of chars to remove

        Returns the 'html_string' string but removing the 'num_chars' first
        chars taking in account the html tags
    """
    if len(html_string) == 0:
        return ""
    if num_chars == 0:
        return html_string
    if html_string[0] == "<":
        left, sep, right = html_string.partition("</a>")
        return remove_first_chars_of_html_string(right, num_chars-1)
    return remove_first_chars_of_html_string(html_string[1:], num_chars-1)

def asciiArt_length_html(tree, num_trees_considered, trans_values, char1="-"):
    """
        tree: jackknife cluster samples tree
        num_trees_considered: number of trees used for the jackknife
        trans_values: dict of: {(val1, val2): (html_color, label)}
        char1: first char to use in the current branch

        Returns:
            result: list containing the strings which represents the tree rooted
                at 'tree'
            mid: integer which means the middle line of 'result'
    """
    LEN = tree.Length or 2
    if tree.Children:
        result = []
        mids = []
        for child in tree.Children:
            if child is tree.Children[0]:
                char2 = get_formated_char_html("/", num_trees_considered,
                    tree.Name, trans_values)
            elif child is tree.Children[-1]:
                char2 = get_formated_char_html("\\", num_trees_considered,
                    tree.Name, trans_values)
            else:
                char2 = '-'
            (child_lines, child_mid) = asciiArt_length_html(child,
                num_trees_considered, trans_values, char2)
            mids.append(len(result) + child_mid)
            result.extend(child_lines)
        low_mid = mids[0]
        high_mid = mids[-1]
        mid = (high_mid + low_mid) / 2
        space_str = ' ' * LEN
        space_pipe_str = ' ' * (LEN - 1) + get_formated_char_html("|",
            num_trees_considered, tree.Name, trans_values)
        prefixes = [space_str] * (low_mid + 1) + [space_pipe_str] * (high_mid -
            low_mid - 1) + [space_str] * (len(result) - high_mid)
        if LEN < 2:
            prefixes[mid] = char1
        else:
            prefixes[mid] = char1 + '-' * (LEN - 2) + \
                get_last_char_of_html_string(prefixes[mid])
        result = [ p + l for (p, l) in zip(prefixes, result)]
        return (result, mid)
    else:
        return ([char1 + '-' * (LEN-1) + '+' + tree.Name], 0)

def draw_jackknife_tree_html(tree, num_trees_considered, trans_values,
    mapping_data):
    """
        tree: jackknife cluster samples tree
        num_trees_considered: number of trees used for the jackknife
        trans_values: dict of: {(val1, val2): (html_color, label)}

        Returns a string wich contains the html code which
        shows the jackknife cluster samples tree colored by jackknife
        fraction.
    """
    unscaled_max_length = max([node.Length for node in tree.tips()])
    tree.scaleBranchLengths(max_length=100, ultrametric=True)
    scaled_max_length = max([node.Length for node in tree.tips()])
    branch_scale = float(unscaled_max_length) / scaled_max_length

    (lines, mid) = asciiArt_length_html(tree, num_trees_considered,
        trans_values)
    new_lines = [add_interactive_sample_id(line, mapping_data, '+')
        for line in lines]
    output = []
    output.append("<pre>Scale: 1 dash, slash, backslash ~ " + 
        "%.4f branch length units<br>" % branch_scale)
    output.extend(new_lines)
    output.append("</pre>")
    return "\n".join(output)

def get_legend_table_html(trans_values):
    """
        trans_values: dict of: {(val1, val2): (html_color, label)}

        Returns a string which contains the html code of a table containing the
        color legend.
    """
    rows = ''

    sorted_keys = trans_values.keys()
    sorted_keys.sort()

    for key in sorted_keys[1:]:
        color = trans_values[key][0]
        desc = trans_values[key][1].replace(">", "&#62;").replace("<", "&#60;")
        rows += ROW_TABLE_LEGEND_HTML % (color, desc)

    return TABLE_LEGEND_HTML % (rows)

def get_jackknife_tree_html_string(tree, num_trees_considered, trans_values,
    mapping_data):
    """
        tree: jackknife cluster samples tree
        num_trees_considered: number of trees used for the jackknife
        trans_values: dict of: {(val1, val2): (html_color, label)}

        Returns a string wich contains the full html page code which
        shows the jackknife cluster samples tree colored by jackknife
        fraction.
    """
    html_string = draw_jackknife_tree_html(tree, num_trees_considered,
        trans_values, mapping_data)
    html_string += get_legend_table_html(trans_values)
    return PAGE_HTML % html_string

def make_jackknife_tree_html_file(tree, support, trans_values, mapping_data,
    html_fp, output_dir):
    """
        tree_fp: jackknife named nodes tree
        support: dict of: { 'trees_considered': int,
            'support_dict': dict of {node_name:float}}
        trans_values: dict of: {(val1, val2): (html_color, label)}
        html_fp: output html filepath
        output_dir: output directory which will contains scripts and images

        Generates a html file stored at 'html_fp' with the tree stored at
        'tree_fp' and colored by jackknife fraction (stored at support_fp).
    """

    # Generate the string which contains the full page html code
    tree_text_html = get_jackknife_tree_html_string(tree,
        support['trees_considered'], trans_values, mapping_data)

    # Move 'overlib.js' to the output_dir
    overlib_js_fp = join(dirname(__file__), OVERLIB_JS)
    copyfile(overlib_js_fp, os.path.join(output_dir, "overlib.js"))

    # Save the html file
    outf = open(html_fp, 'w')
    outf.write(tree_text_html)
    outf.close()