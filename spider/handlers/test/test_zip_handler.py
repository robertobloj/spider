import os
import shutil
from unittest import TestCase, mock

from spider.handlers.html_handler import HtmlHandler
from spider.handlers.pdf_handler import PdfHandler
from spider.handlers.zip_handler import ZipHandler
from spider.utils import file_utils


class TestZipHandler(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = 'spider/handlers/test/outdir'
        self.output_name = 'zip_handler'
        self.zip_file = 'spider/handlers/test/test.zip'

    def setUp(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        file_utils.create_dir_if_not_exist('{}/zip'.format(self.output_dir))
        file_utils.create_dir_if_not_exist('{}/txt'.format(self.output_dir))
        file_utils.create_dir_if_not_exist('{}/unzipped'.format(self.output_dir))

    @mock.patch.object(PdfHandler, "save_result")
    @mock.patch.object(HtmlHandler, "save_result")
    def test_zip_handler(self, mock_html_handler, mock_pdf_handler):
        mock_html_handler.return_value = None
        mock_pdf_handler.return_value = None

        zip_file = "{}/zip/{}.zip".format(self.output_dir, self.output_name)
        img_file = "{}/unzipped/image.png".format(self.output_dir)
        pdf_file = "{}/unzipped/test2.pdf".format(self.output_dir)
        txt_file1 = "{}/txt/file1.txt".format(self.output_dir)
        txt_file2 = "{}/txt/file2.txt".format(self.output_dir)
        zip_in_zip_file = "{}/unzipped/child.zip".format(self.output_dir)

        # check if we start with empty dirs
        self.assertFalse(os.path.exists(zip_file))
        self.assertFalse(os.path.exists(img_file))
        self.assertFalse(os.path.exists(pdf_file))
        self.assertFalse(os.path.exists(txt_file1))
        self.assertFalse(os.path.exists(txt_file2))
        self.assertFalse(os.path.exists(zip_in_zip_file))

        with open(self.zip_file, "rb") as f:
            handler = ZipHandler(mock_html_handler, mock_pdf_handler)
            handler.save_result(self.output_dir, self.output_name, f.read())

        # unzipped dir must be cleaned at the end
        self.assertTrue(os.path.exists(zip_file))
        self.assertTrue(os.path.exists(txt_file1))
        self.assertTrue(os.path.exists(txt_file2))

        # we also do not check result for pdf_handler and html_handler, because there are tests for it
