import os
from logging.config import DictConfigurator

import yaml

from spider.utils import file_utils


class Configurator(object):

    def __init__(self, config):
        """
        Configurator for loggers
        """
        super(Configurator, self).__init__()
        self.__configurator = DictConfigurator(config)

    def configure(self):
        self.__configurator.configure()


dictConfigClass = Configurator


def dict_config(config):
    """Configure logging using a dictionary."""
    dictConfigClass(config).configure()


def configure_logging():
    logs_dir = os.path.join(os.getcwd(), "logs")
    file_utils.create_dir_if_not_exist(logs_dir)
    logging_path = os.path.normpath(os.path.join(os.getcwd(), "logging.yaml"))
    if os.path.isfile(logging_path):
        with open(logging_path) as logging_config_file:
            config = yaml.safe_load(logging_config_file.read())
        dict_config(config)
