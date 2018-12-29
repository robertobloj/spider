import logging
import shutil
import sys
from typing import List, Optional

from spider.utils import file_utils
from spider.utils.download_utils import get_pages
from spider.utils.logging_utils import configure_logging
from spider.utils.zip_utils import zip_dir

sys.setrecursionlimit(100000)


class App(object):
    def __init__(self, url: str,
                 proxy_host: Optional[str] = None,
                 proxy_user: Optional[str] = None,
                 proxy_password: Optional[str] = None,
                 output_dir: str = "output",
                 max_depth: int = 1000,
                 exclude_prefixes: List[str] = None,
                 exclude_contains: List[str] = None,
                 include_contains: List[str] = None):

        self.__max_depth = max_depth
        self.__setup(max_depth, output_dir)

        self.__logger = logging.getLogger(__name__)
        self.__url = url
        self.__exclude_prefixes = exclude_prefixes if exclude_prefixes else []
        self.__exclude_contains = exclude_contains if exclude_contains else []
        self.__include_contains = include_contains if include_contains else []
        self.__output_dir = output_dir
        if proxy_host:
            self.__proxies = {
                'http': 'http://{}:{}@{}'.format(proxy_user, proxy_password, proxy_host),
                'https': 'http://{}:{}@{}'.format(proxy_user, proxy_password, proxy_host),
            }
        else:
            self.__proxies = None

    def main(self):
        get_pages({self.__url}, set(),
                  self.__output_dir, 0,
                  self.__exclude_prefixes,
                  self.__exclude_contains,
                  self.__include_contains,
                  self.__proxies,
                  self.__max_depth)

        # at the end we zip all downloaded files
        zip_dir(self.__output_dir, 'output.zip')

    def __setup(self, max_depth: int, output_dir: str):
        if sys.getrecursionlimit() < max_depth:
            self.__logger.warning("Decrease max depth to: {}".format(sys.getrecursionlimit()))
            self.__max_depth = sys.getrecursionlimit()

        configure_logging()

        # init output dir
        shutil.rmtree(output_dir, ignore_errors=True)
        # html
        file_utils.create_dir_if_not_exist("{}/html".format(output_dir))
        file_utils.create_dir_if_not_exist("{}/txt".format(output_dir))
        # pdf
        file_utils.create_dir_if_not_exist("{}/pdf".format(output_dir))
        file_utils.create_dir_if_not_exist("{}/pdf2txt".format(output_dir))
        # zip
        file_utils.create_dir_if_not_exist("{}/zip".format(output_dir))
        file_utils.create_dir_if_not_exist("{}/unzipped".format(output_dir))


if __name__ == "__main__":

    App(
        url="https://www.somewebpage.com",
        exclude_prefixes=["https://www.youtube.com",
                          "https://www.linkedin.com",
                          "https://trustsealinfo.verisign.com"],
        exclude_contains=["login", "javascript:void(0)", "#", "phone:", "mailto"],
        include_contains=["somewebpage.com"],
        max_depth=1000
    ).main()
