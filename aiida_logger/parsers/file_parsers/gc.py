from __future__ import absolute_import

from __future__ import print_function
from aiida.plugins import DataFactory
from dateutil import parser

from aiida_logger.parsers.file_parsers.base import BaseFileParser
from aiida_logger.utils.array import string_to_float
from six.moves import range


class GCParser(BaseFileParser):
    """Parser class for parsing data from gas chromatographs."""
    def __init__(self, *args, **kwargs):
        super(GCParser, self).__init__(*args, **kwargs)

    def _parse(self, file_handle):
        """Parse the content of GC file as a NumPy array."""

        # Set the separator
        try:
            separator = self.config['separator']
        except KeyError:
            separator = ' '

        # Fetch comment and label ranges
        try:
            comment_range = self.config['comment_range']
        except KeyError:
            comment_range = None
        try:
            label_range = self.config['label_range']
        except KeyError:
            label_range = None

        # Read content
        content = file_handle.readlines()
        comments = None
        labels = None

        # Fetch comments if specified
        shift_index = 0
        if comment_range:
            if '-' not in comment_range and ',' not in comment_range:
                # Only comments on one line
                comments = content[int(self.config['comment_range'])]
                shift_index = shift_index + 1
            else:
                raise NotImplemented

        # Fetch labels if specified
        if label_range:
            if '-' not in label_range and ',' not in label_range:
                # Only labels on one line
                labels = content[int(self.config['label_range'])]
                shift_index = shift_index + 1
            else:
                raise NotImplemented

        date_time = []
        data = []
        num_fields = self.config['num_fields_per_channel']
        if self.config['evolution'] == 'time':
            # Start extracting the actual data
            for line in content[shift_index:]:
                line = line.split(self.config['separator'])
                print(line)
                # First entry should be data and time
                date_time.append(parser.parse(line[0].strip()))
                for channel in range(self.config['channels']):
                    print(channel)
                    print([
                        item
                        for item in line[1 +
                                         channel * num_fields:(channel + 1) *
                                         num_fields]
                    ])
                    data.append([
                        float(item)
                        for item in line[1 +
                                         channel * num_fields:(channel + 1) *
                                         num_fields]
                    ])
        else:
            raise NotImplemented

        print(date_time)
        print(data)

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
