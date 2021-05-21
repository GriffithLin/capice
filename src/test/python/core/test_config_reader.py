import unittest
from src.main.python.core.config_reader import ConfigReader
from src.main.python.resources.enums.sections import Sections


class TestConfigReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up.')
        cls.config = ConfigReader()
        cls.config.parse()

    def setUp(self):
        print('Testing case:')

    def test_section_defaults_present(self):
        print('Section defaults present')
        self.assertTrue(Sections.DEFAULTS.value in self.config.config.sections())

    def test_section_defaults(self):
        print('Section defaults')
        required_arguments = ['logfilelocation', 'genomebuild', 'caddversion']
        for argument in required_arguments:
            self.assertTrue(argument in self.config.defaults)

    def test_section_overwrites_present(self):
        print('Section overwrites present')
        self.assertTrue(Sections.OVERWRITES.value in self.config.config.sections())

    def test_section_overwrites(self):
        print('Section overwrites')
        required_arguments = ['imputefile', 'modelfile']
        for argument in required_arguments:
            self.assertTrue(argument in self.config.overwrites)

    def test_section_misc_present(self):
        print('Section misc present')
        self.assertTrue(Sections.MISC.value in self.config.config.sections())

    def test_section_misc(self):
        print('Section misc')
        required_arguments = ['disablelogfile']
        for argument in required_arguments:
            self.assertTrue(argument in self.config.misc)

    def test_section_training_present(self):
        print('Section training present')
        self.assertTrue(Sections.TRAINING.value in self.config.config.sections())

    def test_section_training(self):
        print('Section training')
        required_argument = ['makebalanced', 'default', 'specifieddefaults', 'split', 'traintestsize', 'earlyexit']
        for argument in required_argument:
            self.assertTrue(argument in self.config.train)

    def test_get_default_key(self):
        print('Get default key')
        value = self.config.get_default_value(key='logfilelocation')
        self.assertIsNone(value)

    def test_get_overwrite_key(self):
        print('Get overwrite key')
        value = self.config.get_overwrite_value(key='imputefile')
        self.assertFalse(value)

    def test_get_misc_key(self):
        print('Get misc key')
        value = self.config.get_misc_value(key='disablelogfile')
        self.assertFalse(value)

    def test_get_training_key(self):
        print('Get training key')
        value = self.config.get_train_value(key='traintestsize')
        self.assertEqual(value, 0.2)


if __name__ == '__main__':
    unittest.main()
