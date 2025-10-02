import os
import ssl
import tempfile
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils_base import File, Hash, Log

log = Log("WWW")


# pylint: disable=W0212
ssl._create_default_https_context = ssl._create_unverified_context


class WWW:
    class DEFAULT_PARAMS:
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            + " AppleWebKit/537.36 "
        }
        T_TIMEOUT = 120
        T_SELENIUM_WAIT = 1

    def __init__(
        self, url: str, headers=None, t_timeout=None, t_selenium_wait=None
    ):
        self.url = url
        self.headers = headers or self.DEFAULT_PARAMS.HEADERS
        self.t_timeout = t_timeout or self.DEFAULT_PARAMS.T_TIMEOUT
        self.t_selenium_wait = (
            t_selenium_wait or self.DEFAULT_PARAMS.T_SELENIUM_WAIT
        )

    def __str__(self) -> str:
        return f"🌐{self.url}"

    @property
    def ext(self) -> str:
        return os.path.splitext(self.url)[1].lower().strip(".")

    @property
    def url_md5(self) -> str:
        return Hash.md5(self.url)

    @property
    def temp_local_path(self):
        dir_www = os.path.join(tempfile.gettempdir(), "www")
        os.makedirs(dir_www, exist_ok=True)
        return os.path.join(dir_www, f"www.{self.url_md5}.{self.ext}")

    def get_response(self):
        response = requests.get(
            self.url,
            headers=self.headers,
            timeout=self.t_timeout,
            verify=False,
        )
        response.raise_for_status()
        return response

    def __read_hot__(self) -> str:
        response = self.get_response()
        return response.content.decode("utf-8")

    def read(self):
        temp_file = File(self.temp_local_path)
        if temp_file.exists:
            return temp_file.read()
        content = self.__read_hot__()
        temp_file.write(content)
        return content

    def read_with_selenium(self):
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        time.sleep(self.t_selenium_wait)
        content = driver.page_source
        driver.quit()
        return content

    def download_binary(self, file_path) -> str:
        CHUNK_SIZE = 1024
        response = self.get_response()
        with open(file_path, "wb") as fd:
            for chunk in response.iter_content(CHUNK_SIZE):
                fd.write(chunk)
        return file_path

    @property
    def soup(self):
        return BeautifulSoup(self.read(), "html.parser")
