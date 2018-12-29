import os
import shutil
from unittest import TestCase

from spider.handlers.pdf_handler import PdfHandler
from spider.utils import file_utils


class TestPdfHandler(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = 'spider/handlers/test/outdir'
        self.output_name = 'pdf_handler'
        self.test_file = 'spider/handlers/test/test.pdf'
        self.test_file2 = 'spider/handlers/test/test2.pdf'

    def setUp(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        file_utils.create_dir_if_not_exist('{}/pdf'.format(self.output_dir))
        file_utils.create_dir_if_not_exist('{}/pdf2txt'.format(self.output_dir))

    def test_text_extraction_is_not_allowed(self):
        pdf_file = "{}/pdf/{}.pdf".format(self.output_dir, self.output_name)
        txt_file = "{}/pdf2txt/{}.txt".format(self.output_dir, self.output_name)

        # check if we start with empty dirs
        self.assertFalse(os.path.exists(pdf_file))
        self.assertFalse(os.path.exists(txt_file))

        with open(self.test_file, "rb") as f:
            handler = PdfHandler()
            handler.save_result(self.output_dir, self.output_name, f.read())

        self.assertTrue(os.path.isdir(self.output_dir))
        self.assertTrue(os.path.isdir("{}/pdf".format(self.output_dir)))
        self.assertTrue(os.path.exists(pdf_file))
        self.assertFalse(os.path.exists(txt_file))

    def test_save_pdf_result(self):
        pdf_file = "{}/pdf/{}.pdf".format(self.output_dir, self.output_name)
        txt_file = "{}/pdf2txt/{}.txt".format(self.output_dir, self.output_name)

        # check if we start with empty dirs
        self.assertFalse(os.path.exists(pdf_file))
        self.assertFalse(os.path.exists(txt_file))

        with open(self.test_file2, "rb") as f:
            array = f.read()

            handler = PdfHandler()
            handler.save_result(self.output_dir, self.output_name, array)

        self.assertTrue(os.path.isdir(self.output_dir))
        self.assertTrue(os.path.isdir("{}/pdf".format(self.output_dir)))
        self.assertTrue(os.path.exists(pdf_file))

        self.assertTrue(os.path.isdir("{}/pdf2txt".format(self.output_dir)))
        self.assertTrue(os.path.exists(txt_file))

        with open(txt_file, "r") as f:
            content = f.read()
            self.assertTrue("Adobe PDF is an ideal format for electronic document distribution as " in content)
            self.assertTrue("Reader. Recipients of other file formats sometimes can't open files " in content)
            self.assertTrue("PDF files always print correctly on any printing device." in content)
            self.assertTrue("Compact  PDF  files  are  smaller  than  their  source  files  and  download" in content)
            self.assertFalse("any printing device. PDF  files  always" in content)
