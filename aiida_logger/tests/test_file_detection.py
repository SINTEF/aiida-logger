""" Tests to check that fleep detects the right filetypes we encounter

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import fleep

from aiida_logger.tests import TEST_DIR


def test_no_extension():
    """Test a datafile with a comment section, labels and integer and floats."""

    test_file = os.path.join(TEST_DIR, 'input_files', 'datafile')
    with open(test_file, "rb") as file:
        info = fleep.get(file.read(128))

    assert not info.type
    assert not info.extension
    assert not info.mime


def test_xlsx_extension_libre():
    """
    Test a xlsx datafile with a comment section, labels, dates, time and floats.
    
    Saved with LibreOffice.
    """

    test_file = os.path.join(TEST_DIR, 'input_files', 'data.xlsx')
    with open(test_file, "rb") as file:
        info = fleep.get(file.read(128))

    assert info.type == ['document', 'archive', 'executable']
    assert info.extension == ['pages', 'key', 'numbers', 'epub', 'zip', 'jar']
    assert info.mime == [
        'application/zip', 'application/epub+zip', 'application/java-archive'
    ]


def test_xlsx_extension_ms():
    """
    Test a xlsx datafile with a comment section, labels, dates, time and floats.

    Saved with MS.
    """

    test_file = os.path.join(TEST_DIR, 'input_files', 'data_ms.xlsx')
    with open(test_file, "rb") as file:
        info = fleep.get(file.read(128))

    assert info.type == ['document', 'archive', 'executable']
    assert info.extension == [
        'doc', 'pps', 'ppt', 'xls', 'docx', 'pptx', 'xlsx', 'pages', 'key',
        'numbers', 'epub', 'zip', 'jar'
    ]
    assert info.mime == [
        'application/vnd.ms-excel', 'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/zip', 'application/epub+zip', 'application/java-archive'
    ]
