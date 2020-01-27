""" Tests to check parsing of generic datafiles

"""
# pylint: disable=unused-import
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from aiida.plugins import CalculationFactory, DataFactory

from aiida_logger.parsers.file_parsers.datafile import DatafileParser
from aiida_logger.utils.fixtures.data import fixture_retrieved  # noqa: F401


def test_generic_datafile_parsing(fixture_retrieved):  # noqa: F811
    """Test a datafile with a comment section, labels and integer and floats."""

    dummy_calculation = CalculationFactory('arithmetic.add')
    exit_codes = dummy_calculation.exit_codes

    parameters = DataFactory('dict')(dict={
        'comment_string': '#',
        'labels': True
    })

    datafile_parser = DatafileParser(fixture_retrieved, exit_codes, parameters)
    data, metadata = datafile_parser.parse()
    metadata = metadata.get_dict()

    assert 'labels' in metadata
    assert 'comments' in metadata
    assert metadata['labels'] == 'time param1 param2 param3'
    assert metadata['comments'][0] == '# This is an example file'
    test_array = np.array([[1.0e+00, 3.0e+00, 4.0e+00, 5.0e+00],
                           [2.0e+00, 4.0e+00, 5.7e+00, -1.0e-01],
                           [3.0e+00, 1.0e-03, 1.0e+03, 8.0e-01]])
    np.testing.assert_allclose(data.get_array('content'), test_array)
