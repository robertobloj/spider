import shutil
from shutil import copyfile

from bs4 import BeautifulSoup

from spider.handlers.content_type_handler import ContentTypeHandler
from spider.handlers.html_handler import HtmlHandler
from spider.handlers.pdf_handler import PdfHandler
from spider.utils.zip_utils import unzip_file


class ZipHandler(ContentTypeHandler):

    def __init__(self, html_handler: HtmlHandler, pdf_handler: PdfHandler):
        super().__init__()
        self._ext_txt = '.txt'
        self._ext_html = '.html'
        self._ext_pdf = '.pdf'
        self.__extensions = (self._ext_txt, self._ext_html, self._ext_pdf)

        # inside zip we have to have reference to more specific handlers
        self.__html_handler = html_handler
        self.__pdf_handler = pdf_handler

    def save_result(self, output_dir: str, output_name: str, content: bytes) -> None:
        """
        save spider result as zip file (for debug purpose) and as txt file with words (for word2vec)
        :param content: pdf response
        :param output_dir: output dir
        :param output_name: output file name
        :return: None
        """
        structure = self.__save_and_unzip(output_dir, output_name, content)
        self.__extract_text_from_files(output_dir, output_name, structure)

    def __extract_text_from_files(self, output_dir: str, output_name: str, structure: dict) -> None:
        """
        extracts text from each file extracted from zip file
        :param output_dir: output directory
        :param output_name: output name
        :param structure: unzipped structure
        :return: None
        """
        # and iterate over unzipped files recursively
        files = [f for f in structure['files'] if f.endswith(self.__extensions)]
        for file in files:
            file_name = "{}/{}".format(structure['root'], file)
            if file_name.endswith(self._ext_html):
                self.__extract_html(file_name, output_dir, file)

            elif file_name.endswith(self._ext_pdf):
                self.__extract_pdf(file_name, output_dir, file)

            elif file_name.endswith(self._ext_txt):
                self.__extract_txt(file_name, output_dir, file)

            else:
                self._err_logger.error("Weird extension for file: {}".format(file_name))

        # clean unzipped dir for next zip files
        shutil.rmtree(structure['root'])

    @classmethod
    def __extract_txt(cls, file_name, output_dir, r):
        # TODO create txt handler
        copyfile(file_name, "{}/txt/{}".format(output_dir, r))

    def __extract_pdf(self, file_name, output_dir, output_name):
        with open(file_name, "rb") as f:
            content = f.read()
            self.__pdf_handler.save_result(output_dir, output_name, content)

    def __extract_html(self, file_name, output_dir, output_name):
        with open(file_name, "r") as f:
            content = f.read()
            self.__html_handler.save_result(output_dir, output_name, BeautifulSoup(content, "lxml"))
            # we do not go deeper even if html contain links

    @classmethod
    def __save_and_unzip(cls, output_dir: str, output_name: str, content: bytes) -> dict:
        """
        we save zip file and unzip its content
        :param content: zip file binary content
        :param output_dir: output directory
        :param output_name: output file name
        :return: unzipped structure
        """
        # we save zip file
        zip_file = "{}/zip/{}.zip".format(output_dir, output_name)
        with open(zip_file, "wb") as f:
            f.write(content)

        # we extract zip file
        zip_output_dir = "{}/unzipped".format(output_dir)
        structure = unzip_file(zip_file, zip_output_dir)
        return structure
