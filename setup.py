#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) 2013, The FastUnifrac Development Team.
#
# Distributed under the terms of the GPLv2 License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from setuptools import setup
from glob import glob

__version__ = "1.9.1-dev"


classes = """
    Development Status :: 3 - Alpha
    License :: OSI Approved :: BSD License
    Topic :: Scientific/Engineering :: Bio-Informatics
    Topic :: Software Development :: Libraries :: Application Frameworks
    Topic :: Software Development :: Libraries :: Python Modules
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: POSIX :: Linux
    Operating System :: MacOS :: MacOS X
"""

with open('README.rst') as f:
    long_description = f.read()

classifiers = [s.strip() for s in classes.split('\n') if s]

setup(name='fastunifrac',
      version=__version__,
      long_description=long_description,
      license="BSD",
      description='FastUnifrac Galaxy interface',
      author="FastUnifrac development team",
      author_email="josenavasmolina@gmail.com",
      url='https://github.com/biocore/fastunifrac',
      test_suite='nose.collector',
      packages=['fastunifrac'],
      include_package_data=True,
      package_data={'fastunifrac': ['support_files/*']},
      scripts=glob('scripts/*'),
      extras_require={'test': ["nose >= 0.10.1", "pep8"]},
      install_requires=['qiime == 1.9.1', 'click'],
      classifiers=classifiers)
