#!/usr/bin/env python

"""
    NOTE: The html file generated in optimized for its usage on Galaxy. It will 
        NOT work in a browser by itself unless the html file (html_fp) is placed
        in the output_dir directory.
"""

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from make_heatmap import plot_heatmap, HEADERS_VER, HEADERS_HOR
from shutil import copyfile
from os.path import join, dirname

# overlib.js path
OVERLIB_JS = "support_files/overlib.js"

# Keywords for dicts in 'list_data'
LD_NAME = 'name'
LD_HEADERS = 'headers'
LD_HEADERS_VER = HEADERS_VER
LD_HEADERS_HOR = HEADERS_HOR
LD_MATRIX = 'matrix'
LD_TRANSFORM_VALUES = 'transform_values'
LD_TABLE_TITLE = 'table_title'

# HTML strings
# (adapted from Jesse Stombaugh and Micah Hamady's code in make_2d_plots.py)
AREA_SRC = """<AREA shape="circle" coords="%d,%d,%d" href="#%s"  \
onmouseover="return overlib('%s');" onmouseout="return nd();">\n"""

IMG_MAP_SRC = """<img src="%s" border="0" ismap usemap="#points%s" width="%d" \
height="%d" />\n"""

MAP_SRC = """
<MAP name="points%s">
%s
</MAP>
"""

DOWNLOAD_LINK = """<a href="%s" >%s</a>"""

TABLE_HTML = """<table cellpading=0 cellspacing=0 border=1>
<tr><th align=center colspan=3 border=0 class="header">%s</th></tr>
<tr>
<td class="normal" align=center border=0>%s</td>
</tr>
</table>
<br><br>"""

PAGE_HTML = """
<html>
<head>
<style type="text/css">
.normal { color: black; font-family:Arial,Verdana; font-size:12; font-weight:normal;}
.header { color: white; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#2C3143;}
.row_header { color: black; font-family:Arial,Verdana; font-size:12; font-weight:bold; background-color:#C1C9E5;}
</style>
<script type="text/javascript" src="overlib.js"></script>
<title>Fastunifrac</title>
</head>
<body>
<div id="overDiv" style="position:absolute; visibility:hidden; z-index:1000;"></div>
%s
</body>
</html>
"""

def get_coords(headers, matrix, plot, mapping_data):
    """
    Inputs:
        headers: {LD_HEADERS_VER:[], LD_HEADERS_HOR:[]}
            used to generate the map label
        matrix: list of lists containing the float values plotted
            used to generate the map label
        plot: heatmap source. Used to get the html coordinates of the map

    Returns:
        all_cids: orderd list with all the map labels
        all_xcoords: ordered list with all the map x coordinates
        all_ycoords: ordered list with all the map y coordinates

    Adapted from Jesse Stombaugh and Micah Hamady's code in make_2d_plots.py
    """
    all_cids = []
    all_xcoords = []
    all_ycoords = []
    plot.set_transform(plot.axes.transData)
    trans = plot.get_transform()

    for j in range(len(headers[LD_HEADERS_VER])):
        for i in range(len(headers[LD_HEADERS_HOR])):
            if matrix[j][i] is not None:
                # Matplotlib interprets rows as columns, so we flip i, j
                icoord = trans.transform((i,j))
                xcoord, ycoord = icoord

                # Build the string with the descriptions of the samples
                sampleID_1 = headers[LD_HEADERS_VER][j]
                sampleID_2 = headers[LD_HEADERS_HOR][i]
                str_desc = "<b>" + sampleID_1 + " vs " + sampleID_2 + \
                    ":</b> " + str(matrix[j][i])
                str_desc += "<br><br><i>" + sampleID_1 + ":</i> " + \
                    mapping_data[0][sampleID_1]['Description']
                str_desc += "<br><br><i>" + sampleID_2 + ":</i> " + \
                    mapping_data[0][sampleID_2]['Description']
                
                all_cids.append(str_desc)
                all_xcoords.append(xcoord)
                all_ycoords.append(ycoord)

    return all_cids, all_xcoords, all_ycoords

def generate_xmap(x_len, y_len, headers, matrix, plot, mapping_data):
    """
    Inputs:
        x_len: number of x samples in the plot (width)
        y_len: number of y samples in the plot (height)
        headers: {LD_HEADERS_VER:[], LD_HEADERS_HOR:[]}
            used to generate the map label
        matrix: list of lists containing the float values plotted
            used to generate the map label
        plot: heatmap source. Used to get the html coordinates of the map

    Returns:
        xmap: list with AREA html string for the map
        img_height: image height
        img_width: image width

    Adapted from Jesse Stombaugh and Micah Hamady's code in make_2d_plots.py
    """
    all_cids, all_xcoords, all_ycoords = get_coords(headers, matrix, plot,
        mapping_data)

    # Although x_len is width and y_len is height, we flip them
    # due to Matplotlib interprets rows as columns
    img_height = x_len * 80
    img_width = y_len * 80

    xmap = []
    z = 6 if len(headers[HEADERS_HOR]) > 10 else 15
    # Since all_cids, all_xcoords, all_ycoords are ordered lists we can zip them
    for cid, x, y in zip(all_cids, all_xcoords, all_ycoords):
        xmap.append(AREA_SRC % (x, img_height - y, z, cid, cid))

    return xmap, img_height, img_width

def get_html_table_string(data, mapping_data, output_dir):
    """
    Inputs:
        data: dict of:
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
        output_dir: output directory where the images and scripts will be saved

    Returns a string with an HTML table with the heatmap

    Based in Jesse Stombaugh and Micah Hamady's code in make_2d_plots.py
    """
    # Create the heatmap
    width, height, plot = plot_heatmap(data[LD_NAME], data[LD_HEADERS],
        data[LD_MATRIX], data[LD_TRANSFORM_VALUES], output_dir)

    # Create the map for the heatmap image
    xmap, img_height, img_width = generate_xmap(height, width, data[LD_HEADERS],
        data[LD_MATRIX], plot, mapping_data)

    # Create the html string with the heatmap image source information
    img_src = IMG_MAP_SRC % (data[LD_NAME] + '.png', data[LD_NAME], img_width,
        img_height)

    # Create the html string with the map information
    img_map = MAP_SRC % (data[LD_NAME], ''.join(xmap))

    # Create the html download link for the image in '.eps.tgz' format
    eps_link = DOWNLOAD_LINK % (data[LD_NAME] + '.eps.gz', "Download Figure")

    # Create the html table with the heatmap image and its map and add it to
    # the string with previous tables
    return TABLE_HTML % (data[LD_TABLE_TITLE], "<br>".join((img_src + img_map,
        eps_link)))

def get_html_page_string(list_data, mapping_data, output_dir):
    """
    Inputs:
        list_data: list of dicts of:
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
            Every dict contains the necessary information for plotting
            the heatmap
        output_dir: output directory where the images and scripts will be saved

    Returns a string with all the HTML page.

    Based in Jesse Stombaugh and Micah Hamady's code in make_2d_plots.py
    """
    out_table = ''
    for item in list_data:
        out_table += get_html_table_string(item, mapping_data, output_dir)

    # Create the complete html string
    return PAGE_HTML % (out_table)

def make_html_file(list_data, mapping_data, html_fp, output_dir):
    """
    Inputs:
        list_data: list of dicts of:
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
            Every dict contains the necessary information for plotting
                the heatmap
        html_fp: file path where the html file will be created
        output_dir: output directory where the images and scripts will be saved

        Generates an html file with all the heatmaps listed in 'list_data'.
        The generated html file will be saved as 'html_fp' and the images and
        the scripts will be saved in 'output_dir'
    """
    page_html_string = get_html_page_string(list_data, mapping_data, output_dir)

    overlib_js_fp = join(dirname(__file__), OVERLIB_JS)

    # Move 'overlib.js' to the output_dir
    copyfile(overlib_js_fp, join(output_dir, "overlib.js"))

    # Save the html file
    out = open(html_fp, "w+")
    out.write(page_html_string)
    out.close()