# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Submit a test calculation on localhost.

Usage: verdi run submit.py
"""
from __future__ import absolute_import
from __future__ import print_function
import os
from aiida_logger import tests, helpers
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run

# Get code
code_string = 'dummy@localhost'

# Prepare input parameters
DiffParameters = DataFactory('logger')
parameters = DiffParameters({'ignore-case': True})

# Define input files to use
SinglefileData = DataFactory('singlefile')
datafile = SinglefileData(
    file=os.path.join(tests.TEST_DIR, "input_files", 'datafile'))

# Set up calculation
inputs = {
    'code': code,
    'parameters': parameters,
    'datafile': datafile,
    'metadata': {
        'description': "Test job submission with the aiida_logger plugin"
    },
}

# Note: in order to submit your calculation to the aiida daemon, do:
# from aiida.engine import submit
# future = submit(CalculationFactory('logger'), **inputs)
result = run(CalculationFactory('logger'), **inputs)
