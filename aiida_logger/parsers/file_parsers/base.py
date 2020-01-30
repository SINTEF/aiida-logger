from __future__ import absolute_import

from __future__ import print_function
from os import path

from aiida.plugins import DataFactory
from aiida_logger.utils.array import string_to_float


class BaseFileParser():
    """Base file parser class."""
    def __init__(self, folder, filename, exit_codes, parameters=None):
        self.folder = folder
        self.filename = filename
        self.exit_codes = exit_codes
        print(exit_codes)
        self.parameters = None
        if parameters:
            self.parameters = parameters.get_dict()
        self.binary = False

    def parse(self):
        """Parse the quantity of interest."""
        try:
            if self.binary:
                with self.folder.open(self.filename, 'rb') as file_handle:
                    result = self._parse(file_handle)
            else:
                with self.folder.open(self.filename, 'r') as file_handle:
                    result = self._parse(file_handle)
        except (OSError, IOError):
            return self.exit_codes.ERROR_READING_OUTPUT_FILE
        if result is None:
            return self.exit_codes.ERROR_INVALID_OUTPUT

        return result

    def _parse(self):
        """The function that takes care of the actual parsing."""

        raise NotImplemented
