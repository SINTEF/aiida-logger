"""
Calculations provided by aiida_logger.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
from __future__ import absolute_import

import six

from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import SinglefileData
from aiida.plugins import DataFactory


class LoggerCalculation(CalcJob):
    """
    AiiDA calculation plugin to fetch files from datafiles.

    Currently relies on a dummy calculation where the input files are retrieved as output files.
    In the future the extraction of data from various loggers and data sources might be possible
    using this calculation framework.
    """
    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super(LoggerCalculation, cls).define(spec)
        spec.input('metadata.options.resources', valid_type=dict, default={'num_machines': 1, 'num_mpiprocs_per_machine': 1})
        spec.input('metadata.options.parser_name', valid_type=six.string_types, default='logger')
        spec.input('metadata.options.withmpi', valid_type=bool, default=False)
        spec.input('metadata.options.output_filename', valid_type=Str, default='logger.out')
        spec.input('parameters', valid_type=Dict, help='Parameters to use for the processing of datafiles.')
        spec.input_namespace('datafiles', valid_type=SinglefileData, dynamic=True, help='A dictionary of datafiles to be analyzed.')

        spec.exit_code(100, 'ERROR_MISSING_DATA_FILE', message='Could not locate the data file.')

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = []
        calcinfo.retrieve_list = []
        # Define which datafiles to analyze
        for item in self.inputs.filenames.items():
            calcinfo.retrieve_list.append(item)

        return calcinfo
