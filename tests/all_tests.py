#!/usr/bin/env python
from os import walk, environ
from subprocess import Popen, PIPE, STDOUT
from os.path import join, abspath, dirname, split
from glob import glob
from qiime.util import get_qiime_scripts_dir
import re

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The FastUniFrac Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiime.util import make_option
from qiime.util import parse_command_line_parameters, get_options_lookup

options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = []
script_info['optional_options'] = []
script_info['version'] = __version__
script_info['help_on_no_arguments'] = False

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile('OK\s*$')
    application_not_found_pattern = re.compile('ApplicationNotFoundError')
    python_name = 'python'
    bad_tests = []
    missing_application_tests = []

    # Run through all of FastUnifrac's unit tests, and keep track of any files
    # which fail unit tests.
    unittest_names = []

    for root, dirs, files in walk(test_dir):
        for name in files:
            if name.startswith('test_') and name.endswith('.py'):
                unittest_names.append(join(root,name))

    unittest_names.sort()

    for unittest_name in unittest_names:
        print "Testing %s:\n" % unittest_name
        command = '%s %s -v' % (python_name, unittest_name)
        result = Popen(command,shell=True,universal_newlines=True,\
                       stdout=PIPE,stderr=STDOUT).stdout.read()
        print result
        if not unittest_good_pattern.search(result):
            if application_not_found_pattern.search(result):
                missing_application_tests.append(unittest_name)
            else:
                bad_tests.append(unittest_name)


    if bad_tests:
        print "\nFailed the following unit tests.\n%s" % '\n'.join(bad_tests)
            
if __name__ == "__main__":
    main()
