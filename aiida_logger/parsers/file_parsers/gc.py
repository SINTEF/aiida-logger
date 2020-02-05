from __future__ import absolute_import

from __future__ import print_function
from aiida.plugins import DataFactory
from dateutil import parser
import numpy as np

from aiida_logger.parsers.file_parsers.base import BaseFileParser
from six.moves import range


class GCParser(BaseFileParser):  # pylint: disable=too-many-locals
    """Parser class for parsing data from gas chromatographs."""
    def __init__(self, *args, **kwargs):
        super(GCParser, self).__init__(*args, **kwargs)

    def _parse(self, file_handle):  # pylint: disable=too-many-locals
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

        # Read content
        content = file_handle.readlines()
        comments = None
        labels = None
        separator = self.parameters['separator']

        # Fetch data layout
        data_layout = self.parameters['data_layout']

        # Fetch comments if specified
        shift_index = 0
        if comment_range:
            if '-' not in comment_range and ',' not in comment_range:
                # Only comments on one line
                comments = content[int(self.parameters['comment_range'])]
                shift_index = shift_index + 1
            else:
                raise NotImplementedError

        date_time = []
        labels = []
        data = []
        time_index = []
        num_channels = len(data_layout)
        num_fields = []
        for channel in range(num_channels):
            data.append([])
            # Fetch location of the time steps
            time_index.append([
                index for index, item in enumerate(data_layout[channel])
                if 'time' in item
            ])
            num_fields.append(len(data_layout[channel]))
            # Build labels
            labels.append(
                [list(item.keys())[0] for item in data_layout[channel]])

        # Check that only one time index is given
        if True in [len(item) > 1 for item in time_index]:
            raise ValueError(
                'More than one time entry per channel. Please correct the configuration.'
            )
        # Make sure we only have integers in the list (find a more clever way to do this)
        time_index = [item[0] for item in time_index]

        # Start extracting the actual data
        for line in content[self.parameters['data_start_line']:]:
            line = line.split(separator)
            # Replace all empty strings with a zero (later converted to float)
            line = ['0.0' if item == '' else item for item in line]
            start_channel_index = 0
            for channel in range(num_channels):
                if channel == 0:
                    # Fetch and remove time entries (assumed the same between channels)
                    date_time.append(
                        parser.parse(line.pop(time_index[channel]).strip(),
                                     fuzzy=True))
                else:
                    # For the other channels, remove time data
                    line.pop(start_channel_index + time_index[channel])
                # Convert from string to target data for each channel
                data[channel].append([
                    float(item) for index, item in enumerate(
                        line[start_channel_index:start_channel_index +
                             num_fields[channel]])
                ])
                start_channel_index = start_channel_index + num_fields[channel]

        # Calculate time difference for each step and store that instead of absolute times
        reference_time = date_time[0]
        date_time = [(time - reference_time).total_seconds()
                     for time in date_time]
        # Compose data, time and metadata nodes
        array = DataFactory('array')()
        for channel in range(num_channels):
            array.set_array('channel_' + str(channel + 1),
                            np.array(data[channel]))
        array.set_array('time', np.array(date_time))
        meta = DataFactory('dict')(dict={
            'start_time': reference_time.utcnow(),
            'comments': comments,
            'labels': labels
        })

        return {'data': array, 'metadata': meta}
