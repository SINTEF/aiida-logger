from __future__ import absolute_import

from __future__ import print_function
from aiida.plugins import DataFactory
from dateutil import parser
import numpy as np

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
            separator = self.parameters['separator']
        except KeyError:
            separator = ' '

        # Fetch comment and label ranges
        try:
            comment_range = self.parameters['comment_range']
        except KeyError:
            comment_range = None
        try:
            label_range = self.parameters['label_range']
        except KeyError:
            label_range = None

        # Read content
        content = file_handle.readlines()
        comments = None
        labels = None

        time_index = self.parameters['time_field_index']
        # Fetch comments if specified
        shift_index = 0
        if comment_range:
            if '-' not in comment_range and ',' not in comment_range:
                # Only comments on one line
                comments = content[int(self.parameters['comment_range'])]
                shift_index = shift_index + 1
            else:
                raise NotImplemented

        num_channels = self.parameters['channels']
        num_fields_per_channel = self.parameters['num_fields_per_channel']
        separator = self.parameters['separator']
        # Fetch labels if specified
        if label_range:
            if '-' not in label_range and ',' not in label_range:
                # Only labels on one line
                labels_raw = content[int(
                    self.parameters['label_range'])].strip().split(separator)
                # Split labels according to number of channels
                labels = []
                start_channel_index = 0
                for channel in range(num_channels):
                    num_fields = num_fields_per_channel[channel] + 1
                    labels.append(
                        labels_raw[start_channel_index:start_channel_index +
                                   num_fields])
                    start_channel_index = start_channel_index + num_fields
                shift_index = shift_index + 1
            else:
                raise NotImplemented

        if self.parameters['evolution'] == 'time':
            date_time = []
            data = []
            for channel in range(num_channels):
                data.append([])
            # Start extracting the actual data
            for line in content[shift_index:]:
                line = line.split(separator)
                # Replace all empty strings with a zero (later converted to float)
                line = ['0.0' if item == '' else item for item in line]
                start_channel_index = 0
                for channel in range(num_channels):
                    if channel == 0:
                        # Fetch and remove time entries (assumed the same between channels)
                        date_time.append(
                            parser.parse(line.pop(time_index).strip(),
                                         fuzzy=True))
                    else:
                        # For the other channels, remove time data
                        line.pop(start_channel_index + time_index)
                    num_fields = num_fields_per_channel[channel]
                    data[channel].append([
                        float(item) for item in
                        line[start_channel_index:start_channel_index +
                             num_fields]
                    ])
                    start_channel_index = start_channel_index + num_fields
        else:
            raise NotImplemented

        # Calculate time difference for each step and store that instead of absolute times
        reference_time = date_time[0]
        date_time = [(time - reference_time).total_seconds()
                     for time in date_time]

        # Compose data and metadata nodes
        array = DataFactory('array')()
        for channel in range(num_channels):
            array.set_array('channel_' + str(channel + 1),
                            np.array(data[channel]))
        meta = DataFactory('dict')(dict={
            'start_time': reference_time.utcnow(),
            'comments': comments,
            'labels': labels
        })

        return {'data': array, 'metadata': meta}
