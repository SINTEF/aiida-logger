""" 
Tests for calculations.

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import numpy as np


def test_process(logger_code):
    """
    Test running a calculation.

    Also checks its outputs.
    """
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run
    from aiida.common.extendeddicts import AttributeDict

    from aiida_logger.tests import TEST_DIR  # pylint: disable=wrong-import-position

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
        'code': logger_code,
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

    assert 'data' in result
    assert 'metadata' in result

    data = result['data']
    metadata = result['metadata']
    metadata = metadata.get_dict()

    assert 'labels' in metadata
    assert 'comments' in metadata
    assert metadata['labels'] == 'time param1 param2 param3'
    assert metadata['comments'][0] == '# This is an example file'
    test_array = np.array([[1.0e+00, 3.0e+00, 4.0e+00, 5.0e+00],
                           [2.0e+00, 4.0e+00, 5.7e+00, -1.0e-01],
                           [3.0e+00, 1.0e-03, 1.0e+03, 8.0e-01]])
    np.testing.assert_allclose(data.get_array('content'), test_array)
