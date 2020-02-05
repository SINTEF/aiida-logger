""" Tests to check parsing of generic datafiles

"""
# pylint: disable=unused-import
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from aiida.plugins import CalculationFactory, DataFactory

from aiida_logger.utils.fixtures.data import fixture_retrieved  # noqa: F401


def test_generic_datafile_parsing(fixture_retrieved):  # noqa: F811
    """Test a datafile with a comment section, labels and integer and floats."""
    from aiida_logger.parsers.file_parsers.datafile import DatafileParser

    dummy_calculation = CalculationFactory('arithmetic.add')
    exit_codes = dummy_calculation.exit_codes

    parameters = DataFactory('dict')(dict={
        'comment_string': '#',
        'labels': True
    })

    datafile_parser = DatafileParser(fixture_retrieved, 'datafile', exit_codes,
                                     parameters)
    result = datafile_parser.parse()
    data = result['data']
    metadata = result['metadata'].get_dict()

    assert 'labels' in metadata
    assert 'comments' in metadata
    assert metadata['labels'] == ['time', 'param1', 'param2', 'param3']
    assert metadata['comments'][0] == '# This is an example file'
    test_array = np.array([[1.0e+00, 3.0e+00, 4.0e+00, 5.0e+00],
                           [2.0e+00, 4.0e+00, 5.7e+00, -1.0e-01],
                           [3.0e+00, 1.0e-03, 1.0e+03, 8.0e-01]])
    np.testing.assert_allclose(data.get_array('content'), test_array)


def test_generic_spreadsheet_parsing(fixture_retrieved):  # noqa: F811
    """Test a datafile with a comment section, labels and integer and floats."""
    from aiida_logger.parsers.file_parsers.spreadsheet import SpreadsheetParser

    dummy_calculation = CalculationFactory('arithmetic.add')
    exit_codes = dummy_calculation.exit_codes

    parameters = DataFactory('dict')(dict={
        'type': 'spreadsheet',
        'evolution': 'time',
        'time_range': 'A6:A8',
        'data_range': 'B6:AQ8',
        'label_range': 'B4:AQ4',
        'comment_range': 'A1:F2',
        'manual_label': {
            0: 'Time'
        },
        'open_end': False,
    })

    spreadsheet_parser = SpreadsheetParser(fixture_retrieved, 'data_ms.xlsx',
                                           exit_codes, parameters)
    result = spreadsheet_parser.parse()
    data = result['data']
    metadata = result['metadata'].get_dict()

    assert 'labels' in metadata
    assert 'comments' in metadata
    assert 'start_time' in metadata
    assert metadata['labels'] == [
        'Time', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5',
        'Sensor 6', 'Sensor 7', 'Sensor 8', 'Sensor 9', 'Sensor 10',
        'Sensor 11', 'Sensor 12', 'Sensor 13', 'Sensor 14', 'Sensor 15',
        'Sensor 16', 'Sensor 17', 'Sensor 18', 'Sensor 19', 'Sensor 20',
        'Sensor 21', 'Sensor 22', 'Sensor 23', 'Sensor 24', 'Sensor 25',
        'Sensor 26', 'Sensor 27', 'Sensor 28', 'Sensor 29', 'Sensor 30',
        'Sensor 31', 'Sensor 32', 'Sensor 33', 'Sensor 34', 'Sensor 35',
        'Sensor 36', 'Sensor 37', 'Sensor 38', 'Sensor 39', 'Sensor 40',
        'Sensor 41', 'Sensor 42'
    ]
    test_array = np.array(
        [[
            0.00000000e+00, -3.40709948e+02, 7.47658860e+02, 9.18733878e+02,
            -7.99093966e+01, 2.45069498e+01, -3.63283978e+01, 9.37928230e+02,
            -4.16957562e+02, 6.93798701e+02, -3.52544446e+02, 8.52946845e+02,
            5.60229149e+02, 2.87366919e+02, -2.69403676e+02, -9.23615100e+02,
            9.68144497e+02, 3.68706033e+02, 7.47278329e+02, -7.47373679e+02,
            4.10574083e+02, -6.31391750e+02, -3.09559120e+02, -7.44718630e+02,
            9.63757742e+02, 4.21721005e+02, -3.33192348e+02, 8.45939222e+02,
            1.24894193e+02, 6.91578314e+02, 3.87962363e+02, 2.27979320e+02,
            -2.50019573e+02, -9.60876606e+02, -8.33308278e+02, 1.56349529e+02,
            7.50691757e+02, 2.35018136e+02, -9.14626100e+02, 6.76976612e+02,
            -3.25222313e+02, 1.38691004e+00, 5.02350466e+02
        ],
         [
             2.20838405e+08, -6.18474215e+02, 6.00631086e+02, -6.43737563e+02,
             7.76594460e+01, -9.22237390e+02, -7.15655510e+01, 9.67789699e+02,
             1.92673128e+02, -5.52394154e+02, 2.81543496e+02, -6.37092365e+01,
             -5.91547184e+02, -5.44977791e+02, -7.67420882e+02,
             -1.62916665e+02, 3.70539399e+02, 1.26995927e+01, -2.68029199e+02,
             6.31882474e+01, 9.76864697e+02, -3.83129487e+02, 1.95210420e+02,
             -2.60162172e+02, -9.86353346e+02, -8.26376630e+02, 1.25272824e+02,
             8.52728373e+02, -7.25402623e+02, -3.01577924e+01, 7.22989853e+02,
             2.26073742e+02, 2.12257008e+02, 7.58457989e+02, -4.97815936e+01,
             5.42971039e+02, 8.16722573e+01, -1.96706989e+02, -2.77223235e+02,
             1.21237190e+02, 5.61942217e+02, -2.43545319e+02, -3.54513781e+00
         ],
         [
             2.20838410e+08, 8.99351867e+02, 6.28300967e+02, 7.28590937e+02,
             5.83291581e+02, 1.85083319e+02, -4.73680591e+01, -3.75341647e+02,
             -7.36851942e+02, -1.82213856e+02, -9.74887341e+02,
             -2.91766140e+02, 7.40829890e+02, 1.26657932e+02, -3.67166167e+02,
             8.34278850e+02, 3.70328554e+02, -6.00622246e+02, 2.47063320e+02,
             6.08178645e+02, 2.70132541e+02, 2.07916205e+02, -3.17457313e+02,
             7.59102669e+02, 1.92718361e+02, 9.28023871e+02, 1.53027429e+02,
             -4.49037090e+02, -9.07665680e+02, 3.50276322e+02, -1.80396333e+02,
             -1.52448548e+02, -9.85388418e+02, 4.67614377e+01, 7.97604734e+02,
             3.49960646e+02, -4.97232975e+02, -4.16892376e+02, 7.18324767e+02,
             6.79491634e+01, -6.50685078e+02, 1.25396740e+02, -9.33237582e+02
         ]])
    np.testing.assert_allclose(data.get_array('content'), test_array)


def test_generic_gc_parsing(fixture_retrieved):  # noqa: F811
    """Test a gc datafile with a comment section, labels, time and floats."""
    from aiida_logger.parsers.file_parsers.gc import GCParser

    dummy_calculation = CalculationFactory('arithmetic.add')
    exit_codes = dummy_calculation.exit_codes

    parameters = DataFactory('dict')(dict={
        'type':
        'gc',
        'comment_line':
        0,
        'data_start_line':
        2,
        'data_layout': [[{
            'time': '%m/%d/%y %H:%M:%S'
        }, {
            'id': int
        }, {
            'He concentration': float
        }, {
            'H2 concentration': float
        }, {
            'O2 concentration': float
        }, {
            'N2 concentration': float
        }, {
            'CH4 concentration': float
        }, {
            'CO concentration': float
        }, {
            'He area': float
        }, {
            'H2 area': float
        }, {
            'O2 area': float
        }, {
            'N2 area': float
        }, {
            'CH4 area': float
        }, {
            'CO area': float
        }],
                        [{
                            'time': '%m/%d/%y %H:%M:%S'
                        }, {
                            'id': int
                        }, {
                            'CO2 concentration': float
                        }, {
                            'H2O concentration': float
                        }, {
                            'CO2 area': float
                        }, {
                            'H2O area': float
                        }]],
        'separator':
        '\t',
    })

    gc_parser = GCParser(fixture_retrieved, 'gc_example.txt', exit_codes,
                         parameters)
    result = gc_parser.parse()
    data = result['data']
    metadata = result['metadata'].get_dict()

    assert 'start_time' in metadata
    assert 'labels' in metadata
    assert 'comments' in metadata
    assert metadata['labels'] == [[
        'time', 'id', 'He concentration', 'H2 concentration',
        'O2 concentration', 'N2 concentration', 'CH4 concentration',
        'CO concentration', 'He area', 'H2 area', 'O2 area', 'N2 area',
        'CH4 area', 'CO area'
    ],
                                  [
                                      'time', 'id', 'CO2 concentration',
                                      'H2O concentration', 'CO2 area',
                                      'H2O area'
                                  ]]
    test_array = np.array(
        [[
            0.00000000e+00, 6.79400000e-01, 5.04992000e+01, 1.36000000e-02,
            1.27000000e-02, 7.92900000e-01, 4.31270000e+00, 0.00000000e+00,
            8.61157000e+05, 8.96377480e+07, 2.34600000e+03, 3.81400000e+03,
            4.41225000e+05, 8.86470000e+05
        ],
         [
             0.00000000e+00, 3.48000000e-02, 6.88570000e+00, 6.76100000e-01,
             0.00000000e+00, 3.79000000e-02, 0.00000000e+00, 0.00000000e+00,
             4.42050000e+04, 1.22223080e+07, 1.16494000e+05, 0.00000000e+00,
             2.11070000e+04, 0.00000000e+00
         ],
         [
             0.00000000e+00, 9.56900000e-01, 6.11289000e+01, 0.00000000e+00,
             0.00000000e+00, 1.64040000e+00, 8.09260000e+00, 0.00000000e+00,
             1.21295000e+06, 1.08505819e+08, 0.00000000e+00, 0.00000000e+00,
             9.12864000e+05, 1.66342600e+06
         ],
         [
             0.00000000e+00, 4.32000000e-02, 7.24410000e+00, 6.84600000e-01,
             0.00000000e+00, 5.93000000e-02, 2.50000000e-03, 0.00000000e+00,
             5.48310000e+04, 1.28584960e+07, 1.17953000e+05, 0.00000000e+00,
             3.30150000e+04, 5.14000000e+02
         ],
         [
             0.00000000e+00, 9.86400000e-01, 6.14073000e+01, 1.04000000e-01,
             0.00000000e+00, 1.85040000e+00, 7.88030000e+00, 0.00000000e+00,
             1.25032800e+06, 1.09000015e+08, 1.79270000e+04, 0.00000000e+00,
             1.02969900e+06, 1.61979900e+06
         ],
         [
             0.00000000e+00, 4.56000000e-02, 7.22490000e+00, 0.00000000e+00,
             0.00000000e+00, 6.70000000e-02, 3.25000000e-02, 0.00000000e+00,
             5.78050000e+04, 1.28244070e+07, 0.00000000e+00, 0.00000000e+00,
             3.72850000e+04, 6.67500000e+03
         ],
         [
             0.00000000e+00, 9.89700000e-01, 6.10085000e+01, 0.00000000e+00,
             0.00000000e+00, 2.31780000e+00, 7.71760000e+00, 0.00000000e+00,
             1.25453200e+06, 1.08292087e+08, 0.00000000e+00, 0.00000000e+00,
             1.28981500e+06, 1.58635400e+06
         ]])
    np.testing.assert_allclose(data.get_array('channel_1'), test_array)
    test_array = np.array([[
        0.000000e+00, 5.635900e+00, 2.672400e+00, 0.000000e+00, 2.956906e+06,
        5.135330e+05
    ],
                           [
                               0.000000e+00, 5.400000e-02, 1.536100e+00,
                               0.000000e+00, 2.834000e+04, 2.951810e+05
                           ],
                           [
                               0.000000e+00, 5.647100e+00, 2.900900e+00,
                               0.000000e+00, 2.962776e+06, 5.574380e+05
                           ],
                           [
                               0.000000e+00, 6.130000e-02, 1.528800e+00,
                               0.000000e+00, 3.216600e+04, 2.937810e+05
                           ],
                           [
                               0.000000e+00, 5.631200e+00, 2.886800e+00,
                               0.000000e+00, 2.954457e+06, 5.547210e+05
                           ],
                           [
                               0.000000e+00, 6.460000e-02, 1.518600e+00,
                               0.000000e+00, 3.390600e+04, 2.918070e+05
                           ],
                           [
                               0.000000e+00, 5.746800e+00, 2.891000e+00,
                               0.000000e+00, 3.015136e+06, 5.555380e+05
                           ]])
    np.testing.assert_allclose(data.get_array('channel_2'), test_array)
