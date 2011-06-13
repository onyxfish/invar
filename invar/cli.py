#!/usr/bin/env python

import argparse
import sys

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
        If you want to constrain which common args are present, you can pass a string for 'omitflags'. Any argument
        whose single-letter form is contained in 'omitflags' will be left out of the configured parser. Use 'f' for 
        file.
        """
        self.argparser = argparse.ArgumentParser(description=self.description, epilog=self.epilog)

        pass

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

