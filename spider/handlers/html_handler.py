from bs4 import BeautifulSoup

from spider.handlers.content_type_handler import ContentTypeHandler


class HtmlHandler(ContentTypeHandler):

    def save_result(self, output_dir: str, output_name: str, soup: BeautifulSoup) -> None:
        """
        save spider result as html file (for debug purpose) and as txt file with words (for word2vec)
        :param soup: beautiful soup object
        :param output_dir: output dir
        :param output_name: output file name
        :return: None
        """
        with open("{}/html/{}.html".format(output_dir, output_name), "w", encoding="UTF-8") as f:
            # noinspection PyTypeChecker
            f.write(str(soup))
        with open("{}/txt/{}.txt".format(output_dir, output_name), "w", encoding="UTF-8") as f:
            f.write("\n".join(self.__extract_text(soup)))

    def __extract_text(self, soup: BeautifulSoup) -> set:
        """
        extract every text tag as <p>, <div>, etc. into single line. As result we return multiple lines string
        :param soup: soup
        :return: multiple lines string
        """
        # at the beginning we clean html from <script>, <style> tags, etc.
        soup = self.__remove_tags(soup)
        text_set = set()
        for s in soup.strings:
            stripped = s.strip()
            # min len must be 2 and we want to get unique values
            if len(stripped) > 1 and stripped not in text_set:
                text_set.add(stripped)
        return text_set

    @classmethod
    def __remove_tags(cls, soup: BeautifulSoup, tags=None) -> BeautifulSoup:
        """
        removes unnecessary tags from html, by default <script> and <style> is removed
        :param soup: soup object
        :param tags: tags to remove
        :return: soup object without unnecessary tags
        """
        for script in soup(tags if tags else ['script', 'style']):
            script.extract()
        return soup

    def __clean_html(self, soup: BeautifulSoup, separator: str = ' '):
        """
        clean html and put all text in one line
        :param soup: beautiful soup object
        :param separator: how to replace all unnecessary gaps
        :return: cleaned html
        """
        soup = self.__remove_tags(soup)
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = separator.join(chunk for chunk in chunks if chunk)
        return text
