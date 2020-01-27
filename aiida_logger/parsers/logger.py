# -*- coding: utf-8 -*-
"""
Parsers provided by aiida_logger.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from __future__ import absolute_import

from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

from aiida_logger.parsers.file_parsers.datafile import DatafileParser


class LoggerParser(Parser):
    """
    Parser class for parsing output of calculation.
    """
    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a LoggerCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.ProcessNode`
        """
        super(LoggerParser, self).__init__(node)
        if not issubclass(node.process_class, CalculationFactory('logger')):
            raise exceptions.ParsingError("Can only parse LoggerCalculation")

    def parse(self, **kwargs):  # pylint: disable=too-many-locals
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        import fleep
        from aiida.common.links import LinkType

        # Check if retrieved folder is present
        try:
            output_folder = self.retrieved
        except exceptions.NotExistent:
            return self.exit_codes.ERROR_NO_RETRIEVED_FOLDER

        # Check that folder content is as expected
        files_retrieved = output_folder.list_object_names()
        inputs = self.node.get_incoming(link_type=LinkType.INPUT_CALC).nested()
        files_expected = inputs['datafiles']
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error("Found files '{}', expected to find '{}'".format(
                files_retrieved, files_expected))
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # Detect file types
        parameters = inputs['parameters']
        filetypes = {}
        for filename in files_expected:
            info = None
            try:
                with output_folder.open(filename, 'rb') as handle:
                    info = fleep.get(handle.read(128))
            except (OSError, IOError):
                return self.exit_codes.ERROR_READING_DATA_FILE
            filetypes[filename] = info
            if not info.type and not info.extension and not info.mime:
                # Call the generic datafile parser as we did not detect any particular
                # file type
                datafile_parser = DatafileParser(output_folder,
                                                 self.exit_codes, parameters)
                data, metadata = datafile_parser.parse()
                self.out('data', data)
                self.out('metadata', metadata)

        return ExitCode(0)
