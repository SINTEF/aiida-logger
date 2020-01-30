from __future__ import absolute_import

from aiida.plugins import DataFactory
from aiida_logger.parsers.file_parsers.base import BaseFileParser
from aiida_logger.utils.array import string_to_float


class DatafileParser(BaseFileParser):
    """Parser class for parsing the the datafile."""
    def __init__(self, *args, **kwargs):
        super(DatafileParser, self).__init__(*args, **kwargs)

    def _parse(self, file_handle):
        """Parse the content of the data file as a NumPy array."""
        data = file_handle.readlines()
        data_no_comments = []
        comments = []
        labels = None

        try:
            separator = self.parameters['separator']
        except KeyError:
            separator = ' '

        try:
            comment_string = self.parameters['comment_string']
        except KeyError:
            comment_string = '#'

        for line in data:
            line = line.strip()
            if not line.startswith(comment_string):
                data_no_comments.append(line)
            else:
                comments.append(line)

        if self.parameters.get('labels'):
            labels = data_no_comments[0].split(separator)
        # Convert to array
        array = string_to_float(data_no_comments[1:], separator)

        # Compose data and metadata nodes
        data = DataFactory('array')()
        data.set_array('content', array)
        metadata = DataFactory('dict')(dict={
            'comments': comments,
            'labels': labels
        })

        return data, metadata
