from io import StringIO
from typing import Optional

from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfpage import PDFPage

from spider.handlers.content_type_handler import ContentTypeHandler


class PdfHandler(ContentTypeHandler):

    def __init__(self):
        super().__init__()

    def save_result(self, output_dir: str, output_name: str, content: bytes) -> None:
        """
        save spider result as pdf file (for debug purpose) and as txt file with words (for word2vec)
        :param content: pdf response
        :param output_dir: output dir
        :param output_name: output file name
        :return: None
        """
        pdf_file = "{}/pdf/{}.pdf".format(output_dir, output_name)
        with open(pdf_file, "wb") as f:
            f.write(content)

        text = self.__read_pdf(pdf_file)
        if text:
            with open("{}/pdf2txt/{}.txt".format(output_dir, output_name), "w") as f:
                try:
                    f.write(text)
                except UnicodeEncodeError:
                    self._err_logger.error("Encoding problem for file {}".format(pdf_file))

    def __read_pdf(self, pdf_file: str, password: str="", encoding: str='utf-8', la_params=LAParams()) -> Optional[str]:
        """
        read pdf content from bytes stream. If you want to
        :param pdf_file: path to pdf file
        :param password: password if pdf is encrypted
        :param encoding: pdf encoding
        :param la_params: parameters for converter
        :return: text
        """
        with StringIO() as return_string:
            resource_mgr = PDFResourceManager()
            with TextConverter(resource_mgr, return_string, codec=encoding, laparams=la_params) as device:
                interpreter = PDFPageInterpreter(resource_mgr, device)
                try:
                    with open(pdf_file, 'rb') as fp:
                        i = 1
                        pages = [p for p in self.__get_pages(fp, password=password)]
                        for page in pages:
                            self._logger.info("Processing {} pdf page from {}".format(i, len(pages)))
                            interpreter.process_page(page)
                            i += 1
                        return return_string.getvalue()
                except PDFTextExtractionNotAllowed:
                    self._err_logger.error("Text extraction is not allowed for: {}".format(pdf_file))
                    return None

    @classmethod
    def __get_pages(cls, fp, maxpages=0, password='', caching=True, check_extractable=True):
        """
        get pages from pdf
        :param fp: file handler
        :param maxpages: max returned pages
        :param password: password if pdf is encrypted
        :param caching: whether we cache or not
        :param check_extractable: check extractable
        :return: pages
        """
        return PDFPage.get_pages(fp, set(),
                                 maxpages=maxpages,
                                 password=password,
                                 caching=caching,
                                 check_extractable=check_extractable)
