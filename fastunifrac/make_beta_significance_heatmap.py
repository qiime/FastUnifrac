#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.parse import parse_mapping_file_to_dict
from fastunifrac.parse import parse_beta_significance_output_pairwise
from fastunifrac.make_html_heatmap import (make_html_file, LD_NAME, LD_HEADERS,
                                           LD_HEADERS_VER, LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES,
                                           LD_TABLE_TITLE)

DICT_TRANS_VALUES = {(None, None): (0, ""),
                     (None, 0.001): (1, "(<0.001)\nHighly\nsignificant"),
                     (0.001, 0.01): (2, "(0.001-0.01)\nSignificant"),
                     (0.01, 0.05): (3, "(0.01-0.05)\nMarginally\nsignificant"),
                     (0.05, 0.1): (4, "(0.05-0.1)\nSuggestive"),
                     (0.1, None): (5, "(>0.1)\nNot\nsignificant")}


def generate_headers_and_matrix(d_data, index):
    """Generates the headers and the matrix values for plotting

    Inputs:
        d_data: dict of: {(sample 1, sample 2),(p value, p value corrected)}
        index: 0 indicates p value and 1 indicates p value corrected

        Returns:
            headers: dict of: {HEADERS_VER:[], HEADERS_HOR:[]}
            result: list of lists containing the float values to plot
    """
    # Check that index is one of the supported values
    if index != 0 and index != 1:
        raise ValueError, "Index must be 0 or 1!"

    sorted_keys = d_data.keys()
    sorted_keys.sort()

    headers = {LD_HEADERS_VER: [], LD_HEADERS_HOR: []}
    headers[LD_HEADERS_VER].append(sorted_keys[0][0])
    headers[LD_HEADERS_HOR].append(sorted_keys[0][0])
    result = []
    row = []
    row.append(None)
    none_ct = 1
    for key in sorted_keys:
        s1, s2 = key
        value = d_data[key][index]
        if headers[LD_HEADERS_VER][none_ct - 1] != s1:
            result.append(row)
            none_ct += 1
            headers[LD_HEADERS_VER].append(s1)
            row = [None for i in range(none_ct)]
        if s2 not in headers[LD_HEADERS_HOR]:
            headers[LD_HEADERS_HOR].append(s2)
        row.append(value)
    result.append(row)

    return headers, result


def generate_dict_data(name, headers, matrix, test_name):
    """Generates a dict with the info needed for the plots

    Inputs:
        name: str with the title of the plot
        headers: dict of: {HEADERS_VER:[], HEADERS_HOR:[]}
        matrix: list of lists containing the float values to plot
        test_name: str with the conducted test name

    Return dict of:
        {
            LD_NAME: plot_name,
            LD_HEADERS: {LD_HEADERS_VER:[], LD_HEADERS_HOR:[]},
            LD_MATRIX : list of lists containing the float values to plot
            LD_TRANSFORM_VALUES: {(val1, val2) : (plot_value, label)}
                must have a key of form (None, None)
                Is a dictionary which allows to transform the continue
                matrix values into a discrete values to plot.
            LD_TABLE_TITLE: table_title
        }
        Contains all the needed information to generate the html file.
    """
    result = {}
    result[LD_NAME] = name
    result[LD_HEADERS] = headers
    result[LD_MATRIX] = matrix
    result[LD_TRANSFORM_VALUES] = DICT_TRANS_VALUES
    result[LD_TABLE_TITLE] = test_name + ": " + name

    return result


def generate_data_make_html(bs_lines):
    """Parses the beta significance file and returns the info in a list of dicts

    Inputs:
        bs_lines: beta significance results open file object

    Returns list of dicts of:
        {
            LD_NAME: plot_name,
            LD_HEADERS: {LD_HEADERS_VER:[], LD_HEADERS_HOR:[]},
            LD_MATRIX : list of lists containing the float values to plot
            LD_TRANSFORM_VALUES: {(val1, val2) : (plot_value, label)}
                must have a key of form (None, None)
                Is a dictionary which allows to transform the continue
                matrix values into a discrete values to plot.
            LD_TABLE_TITLE: table_title
        }
        Contains all the needed information to generate the html file.
    """
    result = []

    dict_data, test_name = parse_beta_significance_output_pairwise(bs_lines)

    raw_headers, raw_matrix = generate_headers_and_matrix(dict_data, 0)
    corr_headers, corr_matrix = generate_headers_and_matrix(dict_data, 1)

    result.append(generate_dict_data("Raw values", raw_headers, raw_matrix,
                                     test_name))
    result.append(generate_dict_data("Corrected values", corr_headers,
                                     corr_matrix, test_name))

    return result


def make_beta_significance_heatmap(beta_significance_fp, mapping_fp, html_fp,
                                   output_dir):
    """Creates an html file with the heatmaps of beta significance analysis

    Inputs:
        beta_significance_fp: beta significance results filepath
        mapping_fp: mapping filepath
        html_fp: output html filepath
        output_dir: output directory where the aux html files will be stored
    """
    bs_lines = open(beta_significance_fp, 'U')

    l_data = generate_data_make_html(bs_lines)

    mapping_data = parse_mapping_file_to_dict(open(mapping_fp, 'U'))

    make_html_file(l_data, mapping_data, html_fp, output_dir)
