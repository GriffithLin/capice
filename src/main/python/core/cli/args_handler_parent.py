from pathlib import Path
from abc import ABCMeta, abstractmethod
from src.main.python.resources.Validators import InputValidator
from src.main.python.resources.processors.input_processor import InputProcessor


class ArgsHandlerParent(metaclass=ABCMeta):
    """
    Parent class of all module specific argument parsers / handlers.
    """
    def __init__(self, parser):
        self._call_loc = str(Path('.').absolute())
        self.parser = parser

    @property
    @abstractmethod
    def _extension(self):
        """
        Method to define what extension(s) are required for an input file for
        each module parser.
        """
        return ()

    @abstractmethod
    def create(self):
        """
        Method to define what parser options should be available for the module.
        Use self.parser.add_argument() to add an argument to the subparser.
        """
        pass

    def handle(self):
        """
        Superclass handler to set the arguments set in create(). Also calls the
        parser to proceed with parsing the module specific arguments, validate
        them and run  the CAPICE code.
        """
        self.parser.set_defaults(func=self._handle_args)

    def _handle_args(self, args):
        """
        Superclass handle args to parse and validate the input and output
        arguments. Also parses the output filename.
        """
        validator = InputValidator(self.parser)
        input_loc = args.input[0]
        validator.validate_input_loc(
            input_loc,
            extension=self._extension
        )
        output_path = None
        if args.output is not None:
            output_path = args.output[0]
        processor = InputProcessor(
            call_dir=self._call_loc,
            input_path=input_loc,
            output_path=output_path,
            force=args.force
        )
        output_loc = processor.get_output_directory()
        validator.validate_output_loc(output_loc)
        output_filename = processor.get_output_filename()
        self._handle_module_specific_args(
            input_loc, output_loc, output_filename, args
        )

    @abstractmethod
    def _handle_module_specific_args(self,
                                     input_loc,
                                     output_loc,
                                     output_filename,
                                     args):
        """
        Method to be filled in by the module specific parsers. Should perform
        additional validation over args specific to the parser. Should then call
        the module to continue the module.
        """
        pass
