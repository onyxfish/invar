#!/usr/bin/env python

import argparse
import sys

import mapnik

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

        if hasattr(self.args, 'font_paths'):
            for font_path in self.args.font_paths:
                mapnik.register_fonts(font_path)

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
        self.argparser.add_argument('-p', '--process_count', help="Number of rendering processes to create.", type=int, default=constants.DEFAULT_PROCESS_COUNT)
        self.argparser.add_argument('-w', '--width', help="Width of images to render.", type=int, default=constants.DEFAULT_WIDTH)
        self.argparser.add_argument('-t', '--height', help="Height of images to render.", type=int, default=constants.DEFAULT_HEIGHT)
        self.argparser.add_argument('-b', '--buffer', type=int, help="The buffer drawn around the image during rendering. Defaults to the width or height, whichever is greater, however, it may not be increased when rendering large elements at small zoom levels.")
        self.argparser.add_argument('--font-path', help='Add a directory to the paths which Mapnik will search by fonts.', dest='font_paths', action='append', default=['/Library/Fonts/', '/usr/share/fonts'])
        self.argparser.add_argument('-s', '--skip-existing', dest='skip_existing', action='store_true', help='Skip rendering tiles which already exist.')
        self.argparser.add_argument('-v', '--verbose', action='store_true', help='Display detailed error messages.')

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

