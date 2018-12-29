import logging
from abc import ABCMeta, abstractmethod


class ContentTypeHandler(metaclass=ABCMeta):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._err_logger = logging.getLogger("spider.errors")

    @abstractmethod
    def save_result(self, output_dir: str, output_name: str, obj) -> None:
        """
        save result into file(s)
        :param obj: object to save
        :param output_dir: output dir
        :param output_name: output name (for file)
        :return: none
        """
        pass
