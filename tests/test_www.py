import os
import unittest

from utils_www import WWW


class TestCase(unittest.TestCase):
    TEST_URL_HTML = (
        "https://raw.githubusercontent.com"
        + "/nuuuwan/utils_www/refs/heads/main/tests/_input/data.html"
    )
    TEST_URL_PNG = (
        "https://raw.githubusercontent.com"
        + "/nuuuwan/utils_www/refs/heads/main/tests/_input/data.png"
    )
    TEST_URL_PYTHON_ORG = "https://www.python.org/"
    DIR_OUTPUT = os.path.join("tests", "_output")

    def test_init_and_basic_methods(self):
        www = WWW(self.TEST_URL_HTML)
        self.assertEqual(
            str(www),
            "🌐https://raw.githubusercontent.com"
            + "/nuuuwan/utils_www/refs/heads/main/tests/_input/data.html",
        )

        self.assertEqual(
            www.ext,
            "html",
        )
        self.assertEqual(
            www.url_md5,
            "0edf940553728e4c1efcdc20fa7810c5",
        )
        self.assertEqual(
            www.temp_local_path,
            "/tmp/www/www.0edf940553728e4c1efcdc20fa7810c5.html",
        )

    def test_read(self):
        www = WWW(self.TEST_URL_HTML)
        if os.path.exists(www.temp_local_path):
            os.remove(www.temp_local_path)
        content = www.read()
        self.assertEqual(len(content), 196)
        self.assertEqual(content[:12], "<html><head>")
        content2 = www.read()
        self.assertEqual(content, content2)

    def test_read_with_selenium(self):
        www = WWW(self.TEST_URL_PYTHON_ORG)
        content = www.read_with_selenium()
        self.assertGreater(len(content), 30_000)

    def test_download_binary(self):
        www = WWW(self.TEST_URL_PNG)
        os.makedirs(self.DIR_OUTPUT, exist_ok=True)
        download_path = os.path.join(self.DIR_OUTPUT, "data.png")
        if os.path.exists(download_path):
            os.remove(download_path)
        www.download_binary(download_path)
        self.assertTrue(os.path.exists(download_path))

    def test_soup(self):
        www = WWW(self.TEST_URL_HTML)
        soup = www.soup
        h1 = soup.find("h1")
        self.assertEqual(h1.text, "Heading 1")
