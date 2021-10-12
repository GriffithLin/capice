import argparse
import logging

from src.args_handler_predict import ArgsHandlerPredict
from src.args_handler_train import ArgsHandlerTrain


class ArgsHandler:
    """
    Command-line argument handler for all sub-commands (e.g. predict, train).
    Parses, validates and executes functions for sub-commands.
    """

    __version__ = '3.0.0-SNAPSHOT'
    __description__ = """CAPICE, a machine-learning-based method for prioritizing pathogenic variants
    https://doi.org/10.1186/s13073-020-00775-w"""

    def __init__(self, parser):
        self.parser = parser

    def handle(self):
        args = self.parser.parse_args()
        self._handle_args(args)
        if 'func' in args:
            args.func(args)
        else:
            self.parser.print_help()
            self.parser.exit(2)

    @staticmethod
    def create():
        parser = argparse.ArgumentParser(description=ArgsHandler.__description__)
        ArgsHandler._add_arguments(parser)

        subparsers = parser.add_subparsers()
        ArgsHandlerPredict.create(subparsers.add_parser('predict'))
        ArgsHandlerTrain.create(subparsers.add_parser('train'))

        return ArgsHandler(parser)

    @staticmethod
    def _add_arguments(parser):
        parser.add_argument(
            '-v',
            '--verbose',
            action='count',
            default=0,
            help='verbose mode. multiple -v options increase the verbosity')

        parser.add_argument('--version', action='version', version=f'%(prog)s {ArgsHandler.__version__}')

    @staticmethod
    def _handle_args(args):
        if args.verbose == 0:
            level = logging.WARN
        elif args.verbose == 1:
            level = logging.INFO
        elif args.verbose == 2:
            level = logging.DEBUG
        else:
            level = logging.DEBUG
        logging.basicConfig(level=level)
