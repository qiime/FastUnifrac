#!/usr/bin/env python

__author__ = "Jose Antonio Navas"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Jose Antonio Navas",]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Jose Antonio Navas"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

def parse_jackknife_support_file(lines):
    """
        lines: jackknife support file lines

        Returns dict of: { 'trees_considered': int,
            'support_dict': dict of {node_name:float}}
    """
    result = {}
    dict_support = {}
    for line in lines:
        if line[0] == '#':
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
    """
        Parser for beta significance output file (e.g. p-test each_pair significance)

        According to beta significance output file format, the first row contains a comment
        which indicates the test realized, and the second row contains the headers, which
        should be 'sample 1', 'sample 2', 'p value', 'p value (Bonferroni corrected)'. Thus,
        we start parsing the values on third row.

        Returns:
            result: dict of: {(sample 1, sample 2),(p value, p value corrected)}
            test_name: string with the name of the test realized
    """
    comment = lines.next() #Get comment line
    lines.next() #Pass header line
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
    """
        Parser for beta significance output file (e.g. unifrac each_sample significance)

        According to beta significance output file format, the first row contains a comment
        which indicates the test realized, and the second row contains the headers, which
        should be 'sample', 'p value', 'p value (Bonferroni corrected)'. Thus,
        we start parsing the values on the third row.

        Returns:
            result: dict of: {sample: (p value, p value corrected)}
            test_name: string with the name of the test realized
    """
    comment = lines.next() #Get comment line
    lines.next() #Pass header line
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