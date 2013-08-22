#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from numpy import flipud
from matplotlib.pylab import *
from commands import getoutput
import os

#Keywords for headers dict
HEADERS_VER = 'vertical'
HEADERS_HOR = 'horizontal'

def get_info_from_dict(trans_values):
    """Get plotting information from the translation dictionary

    Inputs:
        trans_values: dict of: {(val1, val2): (plot_value, label)}
            must have a key of form (None, None) used for asign value to None
            values. Is a dictionary which allows to transform the continue
            matrix values into a discrete values to plot.

    Returns:
        n_values: number of values in trans_values
        boundaries: list with the boundaries for the heatmap's colorbar
        ticks: list with the ticks for the heatmap's colorbar
        ticklabels: list with the ticklabels for the heatmap's colorbar
    """
    sorted_values = trans_values.values()
    sorted_values.sort()
    # We need the number of values to know hom many colors
    # we need in the colormap.
    n_values = len(sorted_values)
    # (None, None) is not a real value, so we don't take it in account
    ticks = [float(i) for i in range(1,n_values)]
    # We will get discrete values, but we want that in the colorbar, this
    # discrete values appear in the center of the range of values.
    boundaries = [i - 0.5 for i in ticks]
    boundaries.append(float(n_values - 0.5))
    #sorted_values[0] is the value for (None, None), so we discard it
    ticklabels = [label for value, label in sorted_values[1:]]

    return n_values, boundaries, ticks, ticklabels

def get_matrix_value(value, trans_values):
    """Transforms a matrix value to a plot value using the translation dict

    Inputs:
        value: value to transform using 'trans_values' dict
        trans_values: dict of: {(val1, val2): (plot_value, label)}
            must have a key of form (None, None) used for asign value to None
            values. Is a dictionary which allows to transform the continue
            matrix values into a discrete values to plot.

    Returns:
        The new value corresponding to 'value' using 'trans_values'
    """
    # None is a special case - check it first
    if value is None:
        return trans_values[(None, None)][0]
    # Check the range which value belongs
    for val1, val2 in trans_values:
        if val1 is not None or val2 is not None:
            if val1 is None and value <= val2:
                return trans_values[(val1, val2)][0]
            if val1 < value and val2 is None:
                return trans_values[(val1, val2)][0]
            if val1 < value and value <= val2:
                return trans_values[(val1, val2)][0]

def make_plot_data(matrix, trans_values):
    """Get the plot values matrix of the matrix values

    Inputs:
        matrix: list of lists containing the float values to plot
        trans_values: dict of: {(val1, val2): (plot_value, label)}
            must have a key of form (None, None) used for asign value to None
            values. Is a dictionary which allows to transform the continue
            matrix values into a discrete values to plot.

    Returns: list of lists containing the discrete values to plot after apply
        'trans_values' to 'matrix'
    """
    result = []
    # Loop through all the matrix values and construct the new matrix
    for row in matrix:
        new_row = []
        for elem in row:
            new_row.append(get_matrix_value(elem, trans_values))
        result.append(new_row)

    return result

def plot_heatmap(plot_name, headers, matrix, trans_values, output_dir):
    """Creates the heatmap figure for the values in matrix

    Inputs:
        plot_name: plot name used for name the files
        headers: dict of: {HEADERS_VER:[], HEADERS_HOR:[]}
        matrix: list of lists containing the float values to plot
        trans_values: dict of: {(val1, val2): (plot_value, label)}
            must have a key of form (None, None) used for asign value to None
            values. Is a dictionary which allows to transform the continue
            matrix values into a discrete values to plot.
        output_dir: output directory where to place the images

    Returns:
        width: figure width
        height: figure height
        headers: input headers with some modifications applied
            (Concretely: headers['HEADERS_VER'] is reversed)
        matrix: input matrix with some modifications applied
            (Concretely: matrix is fliped up to down)
        plot: heatmap plot

    Creates a heatmap and save it as plot_name.png and plot_name.eps.gz
        in the given directory 'output_dir'.
    
    Code adapted from Dan Knights' code in make_otu_heatmap.py
    """
    # Get figure size
    n_values, boundaries, ticks, ticklabels = get_info_from_dict(trans_values)
    width = (len(headers[HEADERS_HOR]) + 2) / 3 if \
                len(headers[HEADERS_HOR]) > 10 else 10
    height = (len(headers[HEADERS_VER]) + 2) / 3 if \
                len(headers[HEADERS_VER]) > 10 else 10
    fig = figure(figsize=(width, height))

    # Only want a colormap with 'n_values' values in the look up table
    my_cmap = get_cmap('spectral', n_values)
    # Get the plot values from the matrix
    plot_data = make_plot_data(matrix, trans_values)
    # Plot data
    plot = imshow(plot_data, interpolation='nearest', cmap=my_cmap)
    ax = fig.axes[0]
    # Put x tick marks on top for showing labels on top
    ax.xaxis.set_ticks_position('top')
    # Turn off tick marks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    #Add ticklabels to axes
    xticks(arange(len(headers[HEADERS_HOR])), headers[HEADERS_HOR])
    yticks(arange(len(headers[HEADERS_VER])), headers[HEADERS_VER])
    #Rotate x ticklabels
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(90)
    #grab the Colorbar instance
    cb = colorbar(boundaries=boundaries, ticks=ticks, orientation='horizontal')
    cb.set_ticklabels(ticklabels)
    #save figure as '.png' format file
    heatmap_fp = os.path.join(output_dir, plot_name + '.png')
    savefig(heatmap_fp, dpi=80, format='png')
    #save figure as '.eps.gz' format file
    eps_fp = os.path.join(output_dir, plot_name + '.eps.gz')
    savefig(eps_fp, format='eps')
    out = getoutput("gzip -f" + eps_fp)
    # Return image size and the plot object
    return width, height, plot