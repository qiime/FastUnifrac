#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

def parse_jackknife_support_file(lines):
    """Parses the jackknife support file

    Inputs:
        lines: jackknife support open file object

    Returns dict of: { 'trees_considered': int,
                        'support_dict': dict of {node_name:float}}
    """
    result = {}
    dict_support = {}
    # Loop through all the lines in the file
    for line in lines:
        if line[0] == '#':
            # In one of the comment lines there is the number of trees used
            try:
                comment, num_trees = line.split(':')
                result['trees_considered'] = int(num_trees)
            except:
                continue
        else:
            node_name, value = line.split('\t')
            dict_support[node_name] = float(value)

    result['support_dict'] = dict_support
    return result

def parse_beta_significance_output_pairwise(lines):
    """Parses the pairwise beta significance output file

    Inputs:
        lines: beta significance open file object

    Returns:
            result: dict of: {(sample 1, sample 2),(p value, p value corrected)}
            test_name: string with the name of the test realized

    According to beta significance output file format, the first row contains a
        comment which indicates the test realized, and the second row contains
        the headers, which should be 'sample 1', 'sample 2', 'p value', 'p value
        (Bonferroni corrected)'. Thus, we start parsing the values on third row.
    """
    #Get comment line
    comment = lines.next()
    #Pass header line
    lines.next()
    result = {}
    for line in lines:
        sample1, sample2, pval, pvalcorr = line.split('\t')
        if pval[0] == '<':
            sym, pval = pval.split('=')
        if pvalcorr[0] == '<':
            sym, pvalcorr = pvalcorr.split('=')
        result[(sample1, sample2)] = (float(pval), float(pvalcorr))

    test_name = str(comment[1:])
    test_name = test_name.replace("\n", "")
    return result, test_name

def parse_beta_significance_output_each_sample(lines):
    """Parses the each sample beta significance output file

    Inputs:
        lines: beta significance open file object

    Returns:
            result: dict of: {sample: (p value, p value corrected)}
            test_name: string with the name of the test realized

    According to beta significance output file format, the first row contains a
        comment which indicates the test realized, and the second row contains
        the headers, which should be 'sample', 'p value', 'p value (Bonferroni
        corrected)'. Thus, we start parsing the values on the third row.
    """
    #Get comment line
    comment = lines.next()
    #Pass header line
    lines.next()
    result = {}
    for line in lines:
        sample, pval, pvalcorr = line.split('\t')
        if pval[0] == '<':
            sym, pval = pval.split('=')
        if pvalcorr[0] == '<':
            sym, pvalcorr = pvalcorr.split('=')
        result[sample] = (float(pval), float(pvalcorr))

    test_name = str(comment[1:])
    test_name = test_name.replace("\n", "")
    return result, test_name