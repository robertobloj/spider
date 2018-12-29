from typing import List
from unittest import TestCase, mock

from spider.app import App


# noinspection PyUnusedLocal
def get_pages(urls: set, downloaded_urls: set, output_dir: str, depth: int,
              exclude_prefixes: List[str], exclude_contains: List[str], include_contains: List[str],
              proxies: dict = None, max_depth: int=1000):
    pass


# noinspection PyUnusedLocal
def zip_dir(path: str, output_file: str) -> None:
    pass


class TestApp(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://some.url/page#section?param=value&param2=weird-value:value'

    # noinspection PyUnusedLocal
    @mock.patch('spider.app.get_pages', side_effect=get_pages)
    @mock.patch('spider.app.zip_dir', side_effect=zip_dir)
    def test_run_app(self, mock_zip_dir, mock_get_pages):
        app = App(url=self.url,
                  proxy_host=None,
                  proxy_user=None,
                  proxy_password=None,
                  max_depth=20000,
                  exclude_prefixes=[],
                  exclude_contains=[],
                  include_contains=['http'])
        self.assertIsNotNone(app)
        app.main()

    # noinspection PyUnusedLocal
    @mock.patch('spider.app.get_pages', side_effect=get_pages)
    @mock.patch('spider.app.zip_dir', side_effect=zip_dir)
    def test_run_app_with_proxy(self, mock_zip_dir, mock_get_pages):
        app = App(url=self.url,
                  proxy_host='http://some.proxy.com:8080',
                  proxy_user='someCorpoKey',
                  proxy_password='somePass',
                  max_depth=2,
                  exclude_prefixes=[],
                  exclude_contains=[],
                  include_contains=['http'])
        self.assertIsNotNone(app)
        app.main()
