import os
from datetime import datetime
from src.main_capice import Main
from src.main.python.core.config_reader import ConfigReader
from src.main.python.core.global_manager import CapiceManager
from src.main.python.resources.utilities.utilities import get_project_root_dir


def set_up_manager_and_loc():
    """
    Function to set up the CapiceManager and testing output location
    :return: manager instance, output_directory
    """
    manager = CapiceManager()
    manager.now = datetime.now()
    manager.disable_logfile = True
    manager.critical_logging_only = True
    manager.verbose = False
    root_dir = get_project_root_dir()
    output_directory = os.path.join(root_dir, '.test_output')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return manager, output_directory


def teardown():
    """
    Function to remove any and all files from the '.test_output' folder and remove the folder itself too.
    """
    test_folder = os.path.join(get_project_root_dir(), '.test_output')
    if len(os.listdir(test_folder)) > 0:
        for file in os.listdir(test_folder):
            os.remove(os.path.join(test_folder, file))
    os.rmdir(test_folder)


def set_up_main():
    ConfigReader().parse()
    main = Main(__program__='testing',
                __author__='R.J. Sietma',
                __version__='Testing',
                input_loc=None,
                output_loc=None)
    return main
