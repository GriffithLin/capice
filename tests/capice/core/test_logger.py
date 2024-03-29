import io
import sys
import logging
import unittest

from molgenis.capice.core.logger import Logger
from tests.capice.test_templates import teardown
from molgenis.capice.core.capice_manager import CapiceManager


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.manager = CapiceManager()
        cls.manager.critical_logging_only = False
        cls.not_present_string = 'Not present string'

    @classmethod
    def tearDownClass(cls):
        print('Tearing down.')
        teardown()

    def capture_stdout_call(self):
        old_stdout = sys.stdout
        listener = io.StringIO()
        sys.stdout = listener
        log = Logger().logger
        log.info('SomeString')
        log.debug('SomeString')
        out = listener.getvalue()
        sys.stdout = old_stdout
        self.assertGreater(len(out), 0)
        return out

    def capture_stderr_call(self):
        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener
        log = Logger().logger
        log.critical('SomeString')
        log.error('SomeString')
        out = listener.getvalue()
        sys.stderr = old_stderr
        self.assertGreater(len(out), 0)
        return out

    def setUp(self):
        print('Testing case:')

    def tearDown(self) -> None:
        print('Resetting arguments.')
        Logger.instance = None
        self.manager.critical_logging_only = False
        self.manager.loglevel = None
        print('Arguments reset.')

    def test_isenbaled_false_debug(self):
        print('isEnabledFor(logging.DEBUG) is False')
        self.manager.loglevel = 20
        log = Logger().logger
        self.assertFalse(log.isEnabledFor(logging.DEBUG))

    def test_isenabled_true_debug(self):
        print('isEnabledFor(logging.DEBUG) is True')
        self.manager.loglevel = 10
        log = Logger().logger
        self.assertTrue(log.isEnabledFor(logging.DEBUG))

    def test_isenabled_false_warning(self):
        print('isEnabledFor(logging.WARNING) is False')
        self.manager.critical_logging_only = True
        log = Logger().logger
        self.assertFalse(log.isEnabledFor(logging.WARNING))

    def test_isenabled_true_warning(self):
        print('isEnabledFor(logging.WARNING) is True')
        log = Logger().logger
        self.assertTrue(log.isEnabledFor(logging.WARNING))
        self.assertFalse(log.isEnabledFor(logging.INFO))

    def test_set_multiple_loglevels(self):
        print('isEnabledFor(logging.DEBUG) is False with '
              'CapiceManager().critical_logging_only set to True')
        self.manager.critical_logging_only = True
        self.manager.loglevel = 10
        log = Logger().logger
        self.assertFalse(log.isEnabledFor(logging.DEBUG))

    def test_loglevel_nonverbose(self):
        """
        Testing Info messages just became a lot harder since the logger is set
        to logging.NOTSET by default, with it's StreamHandlers taking care of
        the messages itself, specially the stdout StreamHandler.
        """
        print('Loglevel info')
        self.manager.loglevel = 20
        out = self.capture_stdout_call()
        self.assertIn('INFO', out)
        self.assertNotIn('DEBUG', out)

    def test_loglevel_verbose(self):
        print('Loglevel verbose')
        self.manager.loglevel = 10
        out = self.capture_stdout_call()
        self.assertIn('INFO', out)
        self.assertIn('DEBUG', out)

    def test_loglevel_critical_logging_only(self):
        print('Critical logging only')
        self.manager.critical_logging_only = True
        out = self.capture_stderr_call()
        self.assertIn('CRITICAL', out)
        self.assertNotIn('ERROR', out)

    def test_stderr(self):
        print('Levels INFO and DEBUG not present in stderr')
        self.manager.loglevel = 10

        old_stderr = sys.stderr
        listener = io.StringIO()
        sys.stderr = listener

        log = Logger().logger
        log.info(self.not_present_string)
        log.debug(self.not_present_string)

        out = listener.getvalue()
        sys.stderr = old_stderr
        self.assertNotIn(self.not_present_string, out)

    def test_stdout(self):
        print('Levels WARNING, ERROR and CRITICAL not present in stdout')
        old_stdout = sys.stdout
        listener = io.StringIO()
        sys.stdout = listener

        log = Logger().logger
        log.warning(self.not_present_string)
        log.error(self.not_present_string)
        log.critical(self.not_present_string)

        out = listener.getvalue()
        sys.stdout = old_stdout

        self.assertNotIn(self.not_present_string, out)

    def test_logger_class(self):
        print('Logger class')
        self.assertEqual(str(Logger().logger.__class__), "<class 'logging.RootLogger'>")


if __name__ == '__main__':
    unittest.main()
