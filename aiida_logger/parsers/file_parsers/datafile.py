from __future__ import absolute_import

from aiida.plugins import DataFactory
from aiida_logger.utils.array import string_to_float


class DatafileParser():
    """Parser class for parsing the the datafile."""
    def __init__(self, folder, exit_codes, parameters):
        self.folder = folder
        self.exit_codes = exit_codes
        self.parameters = parameters.get_dict()

    def parse(self):
        """Parse the datafile."""

        try:
            with self.folder.open('datafile', 'r') as file_handle:
                data, metadata = self._parse_datafile(file_handle)
        except (OSError, IOError):
            return self.exit_codes.ERROR_READING_DATA_FILE
        if data is None:
            return self.exit_codes.ERROR_INVALID_DATA_OUTPUT

        return data, metadata

    def _parse_datafile(self, file_handle):
        """Parse the content of the data file as a NumPy array."""
        data = file_handle.readlines()
        data_no_comments = []
        comments = []
        labels = None
        for line in data:
            line = line.strip()
            if not line.startswith(self.parameters['comment_string']):
                data_no_comments.append(line)
            else:
                comments.append(line)

        if self.parameters.get('labels'):
            labels = data_no_comments[0]

        # Convert to array
        array = string_to_float(data_no_comments[1:], ' ')

        # Compose data and metadata nodes
        data = DataFactory('array')()
        data.set_array('content', array)
        metadata = DataFactory('dict')(dict={
            'comments': comments,
            'labels': labels
        })

        return data, metadata
