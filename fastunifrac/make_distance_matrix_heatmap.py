#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.parse import parse_distmat, parse_mapping_file_to_dict
from numpy import median
from fastunifrac.make_html_heatmap import (make_html_file, LD_NAME, LD_HEADERS,
    LD_HEADERS_VER, LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES,
    LD_TABLE_TITLE)

def get_upper_triangle(matrix):
    """
        Returns a matrix with the upper triangle (without diagonal) values
        of the input matrix and None in the rest of matrix.
    """
    result = []

    for i in range(len(matrix)):
        row = []
        for j in range(i+1):
            row.append(None)
        for j in range(i+1, len(matrix[i])):
            row.append(matrix[i][j])
        result.append(row)

    return result

def compute_quartiles(data):
    """
        Compute quartiles

        Uses method described by Moore and McCabe
    """
    if len(data) < 4:
        raise ValueError, "Not enough values to compute quartiles!"

    data.sort()
    q_median = median(data)
    len_data = len(data)
    m_ix = len_data / 2
    if len_data % 2 == 0:
        lq = median(data[0:m_ix])
        uq = median(data[m_ix:])
    else:
        lq = median(data[0:m_ix])
        uq = median(data[m_ix+1:])

    return lq, q_median, uq

def make_quartiles(dist_mat):
    """
        (Code adapted from Micah Hamady's code)

        Returns dict of: {(value1, value2),(plot_value, label)}
            where:
                (value1, value2) is the quartile interval
                plot_value is the value to use instead of any value in the interval
                label is the label to use in the heatmap plot for this interval
    """
    data = []
    for row in dist_mat:
        for item in row:
            if item is not None:
                data.append(item)

    min_val = min(data)
    max_val = max(data)
    try:
        lq, mq, uq = compute_quartiles(data)
    except ValueError, e:
        lq = mq = uq = 0

    return {(min_val - .01, lq):(1, "(0-25%)\nLower\nquartile"),
            (lq, mq):(2.0, "(25-50%)"),
            (mq, uq):(3.0, "(50-75%)"),
            (uq, max_val + .01):(4.0,"(75-100%)\nUpper\nquartile")}


def generate_trans_values_dict(dist_mat):
    """
        Returns dict of: {(value1, value2),(plot_value, label)}
            Is a dictionary which allows to transform the continue matrix 
            values into a discrete values to plot.
            Have a key of form (None, None) used for asign value to None values
    """
    trans_values = make_quartiles(dist_mat)
    trans_values[(None, None)] = (0, "")
    return trans_values

def generate_data_make_html(dm_lines):
    """
        Return dict of:
            {
                LD_NAME: plot_name,
                LD_HEADERS: {LD_HEADERS_VER:[], LD_HEADERS_HOR:[]},
                LD_MATRIX : list of lists containing the float values to plot
                LD_TRANSFORM_VALUES: {(val1, val2) : (plot_value, label)}
                    must have a key of form (None, None)
                    Is a dictionary which allows to transform the continue matrix 
                    values into a discrete values to plot.
                LD_TABLE_TITLE: table_title
            }
            Contains all the needed information to generate the html file.
    """
    header, dist_mat = parse_distmat(dm_lines)

    dist_mat = get_upper_triangle(dist_mat)

    result = {}
    result[LD_NAME] = "Distance matrix"

    headers = {}
    headers[LD_HEADERS_HOR] = header
    headers[LD_HEADERS_VER] = header

    result[LD_HEADERS] = headers
    result[LD_MATRIX] = dist_mat
    result[LD_TRANSFORM_VALUES] = generate_trans_values_dict(dist_mat)
    result[LD_TABLE_TITLE] = "Distance matrix"

    return result

def make_distance_matrix_heatmap(distance_matrix_lines, mapping_lines, html_fp, output_dir):
    data = generate_data_make_html(distance_matrix_lines)

    mapping_data = parse_mapping_file_to_dict(mapping_lines)

    make_html_file([data], mapping_data, html_fp, output_dir)