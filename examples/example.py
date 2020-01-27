# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
from aiida.common.extendeddicts import AttributeDict
from aiida.orm import Code
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run
from aiida import load_profile
load_profile()

from aiida_logger.tests import TEST_DIR  # pylint: disable=wrong-import-position

# Get code
code_string = 'dummy@localhost'
code = Code.get_from_string(code_string)

# Prepare input parameters
parameters = AttributeDict()
parameters.comment_string = '#'
parameters.labels = True

# Define input files to use
SinglefileData = DataFactory('singlefile')
datafile = SinglefileData(
    file=os.path.join(TEST_DIR, 'input_files', 'datafile'))

# Set up calculation
inputs = {
    'code': code,
    'parameters': DataFactory('dict')(dict=parameters),
    'datafiles': {
        'datafile': datafile
    },
    'metadata': {
        'description': 'Test job submission with the aiida_logger plugin'
    },
}

# Note: in order to submit your calculation to the aiida daemon, do:
# from aiida.engine import submit
# future = submit(CalculationFactory('logger'), **inputs)
result = run(CalculationFactory('logger'), **inputs)
