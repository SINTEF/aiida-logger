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
