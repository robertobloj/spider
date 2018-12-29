import os
import shutil
from unittest import TestCase

from bs4 import BeautifulSoup

from spider.handlers.html_handler import HtmlHandler
from spider.utils import file_utils


class TestHtmlHandler(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = 'spider/handlers/test/outdir'
        self.output_name = 'html_handler'
        self.html = "<html>" \
                    "   <head></head>" \
                    "   <body>" \
                    "       <div>some text</div>" \
                    "       <div>bla bla bla</div>" \
                    "       <div>next article</div>" \
                    "   </body>" \
                    "</html>"

    def setUp(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        file_utils.create_dir_if_not_exist('{}/html'.format(self.output_dir))
        file_utils.create_dir_if_not_exist('{}/txt'.format(self.output_dir))
        file_utils.create_dir_if_not_exist('{}/all'.format(self.output_dir))

    def test_save_html_result(self):
        html_file = "{}/html/{}.html".format(self.output_dir, self.output_name)
        txt_file = "{}/txt/{}.txt".format(self.output_dir, self.output_name)

        # check if we start with empty dirs
        self.assertFalse(os.path.exists(html_file))
        self.assertFalse(os.path.exists(txt_file))

        handler = HtmlHandler()
        soup = BeautifulSoup(self.html, "lxml")
        handler.save_result(self.output_dir, self.output_name, soup)

        # check if files are saved correctly
        self.assertTrue(os.path.isdir(self.output_dir))
        self.assertTrue(os.path.isdir("{}/html".format(self.output_dir)))
        self.assertTrue(os.path.exists(html_file))

        self.assertTrue(os.path.isdir("{}/txt".format(self.output_dir)))
        self.assertTrue(os.path.exists(txt_file))

        strings = ['bla bla bla', 'some text', 'next article']
        with open(txt_file, 'r') as fh:
            content = fh.readlines()
            # TODO why script tag is not ignored?
            self.assertEqual(3, len(content))
            for line in content:
                # order does not matter, so we check only whether we found all texts
                found = False
                for s in strings:
                    if s.strip() in line.strip():
                        found = True
                        break
                self.assertTrue(found)
