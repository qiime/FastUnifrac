#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.parse import parse_distmat, parse_mapping_file_to_dict
from numpy import median
from fastunifrac.make_html_heatmap import (make_html_file, LD_NAME, LD_HEADERS,
    LD_HEADERS_VER, LD_HEADERS_HOR, LD_MATRIX, LD_TRANSFORM_VALUES,
    LD_TABLE_TITLE)

def get_upper_triangle(matrix):
    """Sets the lower triangle and the diagonal of 'matrix' to None

    Inputs:
        matrix: list of lists representing a matrix

    Returns the list of lists representing a matrix with the upper triangle
        (without diagonal) values of the input matrix and None in the rest of 
        the matrix.
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
    """Compute the quartiles of data

    Input:
        data: array

    Returns:
        lq: lower quartile
        q_median: median quartile
        uq: upper quartile

    Note: Uses method described by Moore and McCabe
    Note: raises a ValueError if data have less than 4 elements
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
    """Creates a dictionary with the quartile ranges and its label in the plot

    Inputs:
        dist_mat: distance matrix values (list of lists)

    Returns dict of: {(value1, value2),(plot_value, label)}
        where:
            (value1, value2) is the quartile interval
            plot_value is the value to use instead of any value in the interval
            label is the label to use in the heatmap plot for this interval
    """
    # Create a 1D array with the non-None data
    data = []
    for row in dist_mat:
        for item in row:
            if item is not None:
                data.append(item)
    # Compute quartiles
    min_val = min(data)
    max_val = max(data)
    try:
        lq, mq, uq = compute_quartiles(data)
    except ValueError, e:
        lq = mq = uq = 0
    # Crate and return the dictionary with the quartiles ranges
    return {(min_val - .01, lq):(1, "(0-25%)\nLower\nquartile"),
            (lq, mq):(2.0, "(25-50%)"),
            (mq, uq):(3.0, "(50-75%)"),
            (uq, max_val + .01):(4.0,"(75-100%)\nUpper\nquartile")}


def generate_trans_values_dict(dist_mat):
    """Generates a dictionary for translate the matrix values to plot values

    Inputs:
        dist_mat: distance matrix values (list of lists)

    Returns dict of: {(value1, value2),(plot_value, label)}
        Is a dictionary which allows to transform the continue matrix 
        values into a discrete values to plot.
        Have a key of form (None, None) used for assign value to None values
    """
    trans_values = make_quartiles(dist_mat)
    trans_values[(None, None)] = (0, "")
    return trans_values

def generate_data_make_html(dm_lines):
    """Generates a dictionary from the distance matrix with the plot info

    Inputs:
        dm_lines: distance matrix open file object

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
    # Distance matrix are symmetric, get only the upper triangle
    dist_mat = get_upper_triangle(dist_mat)
    # Generate the dictionary
    result = {}
    result[LD_NAME] = "Distance matrix"
    # In this case, the headers are symmetric
    headers = {}
    headers[LD_HEADERS_HOR] = header
    headers[LD_HEADERS_VER] = header

    result[LD_HEADERS] = headers
    result[LD_MATRIX] = dist_mat
    result[LD_TRANSFORM_VALUES] = generate_trans_values_dict(dist_mat)
    result[LD_TABLE_TITLE] = "Distance matrix"

    return result

def make_distance_matrix_heatmap(dm_lines, mapping_lines, html_fp, output_dir):
    """Create an html with a heatmap of the distance matrix

    Inputs:
        dm_lines: distance matrix open file object
        mapping_lines: mapping open file object
        html_fp: filepath of the output html file
        output_dir: path of the output directory which will contain the aux
            html files
    """
    # Parse input files
    data = generate_data_make_html(dm_lines)
    mapping_data = parse_mapping_file_to_dict(mapping_lines)
    # Create the html file
    make_html_file([data], mapping_data, html_fp, output_dir)