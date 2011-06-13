#!/usr/bin/env python

import argparse
import sys

import constants

class InvarUtility(object):
    description = ''
    epilog = ''
    override_flags = ''

    def __init__(self):
        """
        Perform argument processing and other setup for a InvarUtility.
        """
        self._init_common_parser()
        self.add_arguments()
        self.args = self.argparser.parse_args()
        self._install_exception_handler()

    def add_arguments(self):
        """
        Called upon initialization once the parser for common arguments has been constructed.

        Should be overriden by individual utilities.
        """
        raise NotImplementedError('add_arguments must be provided by each subclass of InvarUtility.')

    def main(self):
        """
        Main loop of the utility.

        Should be overriden by individual utilities and explicitly called by the executing script.
        """
        raise NotImplementedError(' must be provided by each subclass of InvarUtility.')

    def _init_common_parser(self):
        """
        Prepare a base argparse argument parser so that flags are consistent across different shell command tools.
        """
        self.argparser = argparse.ArgumentParser(description=self.description, epilog=self.epilog)

        self.argparser.add_argument('config', help="Mapnik2 XML configuration file.")
        self.argparser.add_argument('output_dir', help="Destination directory for output.")
        self.argparser.add_argument('-p', '--processes', help="Number of rendering processes to create", type=int, default=constants.DEFAULT_PROCESS_COUNT)

    def _install_exception_handler(self):
        """
        Installs a replacement for sys.excepthook, which handles pretty-printing uncaught exceptions.
        """
        def handler(t, value, traceback):
            if self.args.verbose:
                sys.__excepthook__(t, value, traceback)
            else:
                print value

        sys.excepthook = handler

