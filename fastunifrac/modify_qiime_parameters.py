#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

def create_dict_of_changes(params, values):
    """
        params: string which contains a comma separated list with script:parameter_to_change
        values: string which contains a comma separated list with new values. Must be in order with respect to 'params'

        Returns dict of: {parameter:value}
    """
    list_params = params.split(',')
    list_values = values.split(',')

    if len(list_params) != len(list_values):
        raise ValueError, "Options --parameters and --new_values must have same length."

    changes = {}
    for idx, param in enumerate(list_params):
        changes[param] = list_values[idx]
    return changes

def replace_value(lines, param, value):
    """
        lines: list of parameter file string lines
        param: parameter to change
        value: new value to assign to 'param'

        Return the list 'lines' with the parameter 'param' changed
            to the new value 'value'
    """
    new_lines = []
    finded = False
    for line in lines:
        if (len(line) != 0) and (line[0] != '#') and (param in line):
            line=line.replace(line, param + "\t" + value.replace('-',',') + "\n")
            finded = True
        new_lines.append(line)
    if not finded:
        new_lines.append(param + "\t" + value.replace('-', ',') + "\n")
    return new_lines

def modify_qiime_parameters(param_fp, output_fp, parameters, new_values):
    """
        param_fp: parameter filepath
        output_fp: output filepath
        parameters: string which contains a comma separated list with script:parameter_to_change
        new_values: string which contains a comma separated list with new values.
            Must be in order with respect to 'parameters'

        Creates a new parameter file stored at 'output_fp' with the params listed 'parameters'
            assigned to the new values listed at 'new_values'
    """
    changes = create_dict_of_changes(parameters, new_values)

    input_file = open(param_fp, 'r')
    new_lines = list(input_file)
    input_file.close()

    for key in changes.keys():
        new_lines = replace_value(new_lines, key, changes[key])

    output_file = open(output_fp, 'w')
    output_file.writelines(new_lines)