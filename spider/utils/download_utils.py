import logging
import os
import traceback
from time import sleep
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from spider.handlers.html_handler import HtmlHandler
from spider.handlers.pdf_handler import PdfHandler
from spider.handlers.zip_handler import ZipHandler

__logger = logging.getLogger(__name__)
__ct_logger = logging.getLogger("spider.content.type")
__ex_url_logger = logging.getLogger("spider.excluded.urls")
__url_logger = logging.getLogger("spider.downloaded.urls")
__err_logger = logging.getLogger("spider.errors")
__extensions = ["html", "pdf"]

__pdf_handler = PdfHandler()
__html_handler = HtmlHandler()
__zip_handler = ZipHandler(__html_handler, __pdf_handler)


def get_links(soup: BeautifulSoup, url: str, exclude_prefixes: List[str], exclude_contains: List[str],
              include_contains: List[str]) -> set:
    """
    extracts links from downloaded page
    :param url: parent url
    :param soup: beautiful soup object
    :param exclude_prefixes: some links we want to exclude
    :param exclude_contains: some links we want to exclude
    :param include_contains: urls need to contain at least one pattern from this list
    :return: links
    """
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        include = False

        # sometimes we have <a></a>, we don't need it
        if href:
            href = __build_url(domain, href)

            for contain in include_contains:
                if contain in href:
                    include = True
                    break

            for prefix in exclude_prefixes:
                if href.startswith(prefix) or href == "/":
                    __ex_url_logger.info("Prefix '{}' is excluded, drop url: {}".format(prefix, href))
                    include = False
                    break

            for contain in exclude_contains:
                if contain in href:
                    __ex_url_logger.info("Contains '{}', drop url: {}".format(contain, href))
                    include = False
                    break

            if include:
                links.add(href)
    return links


def get_page(url: str, output_dir: str,
             exclude_prefixes: List[str], exclude_contains: List[str], include_contains: List[str],
             proxies: dict = None) -> set:
    """
    get single page
    :param url: url to download
    :param output_dir: output dir
    :param exclude_prefixes: prefixes for url which should be excluded
    :param exclude_contains: phrases in url which should be excluded
    :param include_contains: url must contain
    :param proxies: proxies for connection if required
    :return: urls found on current url web page
    """
    # noinspection PyBroadException
    try:
        output_name = get_output_name(url)

        # we check if we have downloaded url (result.html exists)
        for e in __extensions:
            if os.path.isfile("{}/{}.{}".format(output_dir, output_name, e)):
                __err_logger.warning("File {} is downloaded, skip it!".format(output_name))
                return set()

        links = set()
        response = requests.get(url, proxies=proxies)
        __url_logger.info("Download page '{}' with status {}".format(url, response.status_code))
        if response.ok:
            headers = response.headers
            content_type = str(headers['content-type'])

            if "text/html" in content_type:
                soup = BeautifulSoup(response.content, "lxml")
                __html_handler.save_result(output_dir, output_name, soup)
                links |= get_links(soup, url, exclude_prefixes, exclude_contains, include_contains)

            elif "application/pdf" in content_type:
                __pdf_handler.save_result(output_dir, output_name, response.content)

            elif "application/zip" in content_type:
                __zip_handler.save_result(output_dir, output_name, response.content)

            else:
                __ct_logger.warning("ContentType {} is not implemented, url: {}".format(content_type, url))

        else:
            __err_logger.warning("Response is invalid, code: {}, url: {}".format(response.status_code, url))
        return links

    except Exception:
        # most exceptions occur because of proxy delay, we take some time and continue
        __err_logger.error("Can't download page '{}'".format(url))
        traceback.print_exc()
        sleep(2)
        return set()


def get_pages(urls: set, downloaded_urls: set, output_dir: str, depth: int,
              exclude_prefixes: List[str], exclude_contains: List[str], include_contains: List[str],
              proxies: dict = None, max_depth: int = 1000) -> None:
    """
    allows to get pages from urls defined as parameter
    :param urls: url addresses to download
    :param downloaded_urls: downloaded urls. Because of recursive calls, we don't want to download again the same
                            urls. We collect all downloaded urls and we put it into next iteration for subtraction
                            and saving time.
    :param output_dir: output dir
    :param depth: current depth
    :param exclude_prefixes: prefixes for url which should be excluded
    :param exclude_contains: phrases in url which should be excluded
    :param include_contains: url must contain
    :param proxies: proxies for connection if required
    :param max_depth: how deep we want to download pages
    :return: None
    """
    __logger.info("current depth: {}".format(depth))
    urls_list = urls - downloaded_urls
    if depth < max_depth and len(urls_list) > 0:
        child_links = set()

        for i, u in enumerate(urls_list):
            child_links |= get_page(u, output_dir, exclude_prefixes, exclude_contains, include_contains, proxies)

        get_pages(child_links, downloaded_urls | urls, output_dir, depth + 1,
                  exclude_prefixes, exclude_contains, include_contains, proxies, max_depth)


def get_output_name(url: str):
    return url.replace("://", "_").replace(".", "_").replace("/", "_").replace("#", "_").replace("?", "_") \
        .replace("=", "_").replace(":", "_").replace("%", "_").replace("&", "_").replace("-", "_")


def __build_url(domain: str, href: str) -> str:
    """
    builds url as absolute path
    :param domain: domain
    :param href: url
    :return: absolute url
    """
    href = href.strip()
    slash = "" if href.startswith("/") else "/"
    return href if href.startswith("http") else "{}{}{}".format(domain, slash, href)
