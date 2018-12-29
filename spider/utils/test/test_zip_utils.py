import os
from unittest import TestCase

from spider.utils.zip_utils import zip_dir, unzip_file


class TestZipUtils(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_dir = 'spider/utils/test/indir'
        self.output_zip_dir = 'spider/utils/test/outzipdir'
        self.output_zip_file1 = "{}/file1.txt".format(self.output_zip_dir)
        self.output_zip_file2 = "{}/file2.txt".format(self.output_zip_dir)
        self.output_zip = 'spider/utils/test/outdir/output.zip'
        self.zip_file = 'spider/utils/test/test.zip'

    def setUp(self):
        if os.path.exists(self.output_zip):
            os.remove(self.output_zip)

        if os.path.isfile(self.output_zip_file1):
            os.remove(self.output_zip_file1)
        if os.path.isfile(self.output_zip_file2):
            os.remove(self.output_zip_file2)

    def test_zip_dir(self):
        self.assertFalse(os.path.isfile(self.output_zip))
        zip_dir(self.input_dir, self.output_zip)
        self.assertTrue(os.path.isfile(self.output_zip))

    def test_unzip_file(self):
        self.assertFalse(os.path.isfile(self.output_zip_file1))
        self.assertFalse(os.path.isfile(self.output_zip_file2))
        result = unzip_file(self.zip_file, self.output_zip_dir)
        self.assertTrue(os.path.exists(self.output_zip_dir))
        self.assertIsInstance(result, dict)
        self.assertTrue('root' in result)
        self.assertTrue('dirs' in result)
        self.assertTrue('files' in result)
        self.assertEqual(self.output_zip_dir, result['root'])
        self.assertEqual(0, len(result['dirs']))
        self.assertEqual(2, len(result['files']))

        files = os.listdir(self.output_zip_dir)
        self.assertIsNotNone(files)
        self.assertEqual(2, len(files))
