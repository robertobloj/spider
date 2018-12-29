from unittest import TestCase, mock

from bs4 import BeautifulSoup

from spider.handlers.html_handler import HtmlHandler
from spider.handlers.pdf_handler import PdfHandler
from spider.handlers.zip_handler import ZipHandler
from spider.utils.download_utils import get_output_name, get_links, get_page


class Object(object):
    pass


# noinspection PyUnusedLocal
def mock_get_invalid_code(url, data=None, **kwargs):
    assert kwargs is not None
    response = Object()
    response.ok = False
    response.status_code = 404
    return response


# noinspection PyUnusedLocal
def mock_get_txt(url, data=None, **kwargs):
    assert kwargs is not None
    response = Object()
    response.ok = True
    response.text = 'OK'
    response.headers = {
        'content-type': 'text/plain'
    }
    return response


# noinspection PyUnusedLocal
def mock_get_zip(url, data=None, **kwargs):
    assert kwargs is not None
    response = Object()
    response.ok = True
    response.content = 'some binary content'
    response.headers = {
        'content-type': 'application/zip'
    }
    return response


# noinspection PyUnusedLocal
def mock_get_pdf(url, data=None, **kwargs):
    assert kwargs is not None
    response = Object()
    response.ok = True
    response.content = 'some binary content'
    response.headers = {
        'content-type': 'application/pdf'
    }
    return response


# noinspection PyUnusedLocal
def mock_get_html(url, data=None, **kwargs):
    assert kwargs is not None
    response = Object()
    response.ok = True
    response.content = "<html>" \
                       "   <head></head>" \
                       "   <body>" \
                       "       <div>Go to <a href='/'>root page</a></div>" \
                       "       <div>bla bla bla <a>no href</a></div>" \
                       "       <div>next article <a href='http://fake.url.com'>link</a></div>" \
                       "       <div><a href='page/article/download/example.html'>example</a></div>" \
                       "   </body>" \
                       "</html>"
    response.headers = {
        'content-type': 'text/html'
    }
    return response


class TestDownloadUtils(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = 'spider/utils/test/outdir'
        self.output_name = 'get_page'
        self.url = 'http://some.url/page#section?param=value&param2=weird-value:value'
        self.urls = ['http://fake.url.com', 'http://some.url/page/article/download/example.html']
        self.html = "<html>" \
                    "   <head><script>alert('test')</script></head>" \
                    "   <body>" \
                    "       <div>some text</div>" \
                    "       <div>bla bla bla <a>no href</a></div>" \
                    "       <div>next article <a href='http://fake.url.com'>link</a></div>" \
                    "       <div><a href='page/article/download/example.html'>example</a></div>" \
                    "   </body>" \
                    "</html>"

    def test_get_output_name(self):
        result = get_output_name(self.url)
        self.assertEqual(result, 'http_some_url_page_section_param_value_param2_weird_value_value')

    def test_get_all_links(self):
        soup = BeautifulSoup(self.html, "lxml")

        links = get_links(soup, self.url, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(2, len(links))
        self.assertTrue(links.pop() in self.urls)
        self.assertTrue(links.pop() in self.urls)

    def test_some_links(self):
        soup = BeautifulSoup(self.html, "lxml")

        links = get_links(soup, self.url, [], [], ['http'])
        self.assertIsNotNone(links)
        self.assertEqual(1, len(links))
        self.assertEqual('http://fake.url.com', links.pop())

    def test_exclude_prefix(self):
        soup = BeautifulSoup(self.html, "lxml")

        links = get_links(soup, self.url, ['http://fake'], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(1, len(links))
        self.assertEqual('http://some.url/page/article/download/example.html', links.pop())

    def test_exclude_contains(self):
        soup = BeautifulSoup(self.html, "lxml")

        links = get_links(soup, self.url, [], ['fake'], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(1, len(links))
        self.assertEqual('http://some.url/page/article/download/example.html', links.pop())

    # noinspection PyUnusedLocal
    @mock.patch('requests.get', side_effect=mock_get_txt)
    def test_get_txt_page(self, mock_req_get):
        links = get_page(self.url, self.output_dir, 0, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(0, len(links))

    # noinspection PyUnusedLocal
    @mock.patch('requests.get', side_effect=mock_get_invalid_code)
    def test_get_invalid_code(self, mock_req_get):
        links = get_page(self.url, self.output_dir, 0, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(0, len(links))

    # noinspection PyUnusedLocal
    @mock.patch.object(PdfHandler, "save_result")
    @mock.patch('requests.get', side_effect=mock_get_pdf)
    def test_get_pdf_page(self, mock_req_get, mock_pdf_handler):
        mock_pdf_handler.return_value = None

        links = get_page(self.url, self.output_dir, 0, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(0, len(links))

    # noinspection PyUnusedLocal
    @mock.patch.object(ZipHandler, "save_result")
    @mock.patch('requests.get', side_effect=mock_get_zip)
    def test_get_zip(self, mock_req_get, mock_zip_handler):
        mock_zip_handler.return_value = None

        links = get_page(self.url, self.output_dir, 0, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(0, len(links))

    # noinspection PyUnusedLocal
    @mock.patch.object(HtmlHandler, "save_result")
    @mock.patch('requests.get', side_effect=mock_get_html)
    def test_get_html_page(self, mock_req_get, mock_html_handler):
        mock_html_handler.return_value = None

        links = get_page(self.url, self.output_dir, 0, [], [], ['http', 'page'])
        self.assertIsNotNone(links)
        self.assertEqual(2, len(links))
        self.assertTrue(links.pop() in self.urls)
        self.assertTrue(links.pop() in self.urls)

    # noinspection PyUnusedLocal
    @mock.patch('requests.get', side_effect=Exception("Boom!"))
    def test_exception(self, mock_req_get):
        self.assertRaises(Exception, get_page(self.url, self.output_dir, 0, [], [], ['http', 'page']))
