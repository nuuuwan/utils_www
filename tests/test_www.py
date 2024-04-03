import os
import unittest

from utils_base import File

from utils_www import WWW

DIR_TESTS = 'tests'


URL_BASE = '/'.join(
    [
        'https://raw.githubusercontent.com',
        'nuuuwan/utils_www',
        'main/tests',
    ]
)

URL_HTML = 'https://nuuuwan.github.io/utils_www/index.html'


def get_test_file(ext: str) -> str:
    return os.path.join(DIR_TESTS, f'data.{ext}')


def strip_html(html):
    return html.replace('\t', '').replace('\n', '').replace(' ', '')


def get_test_url(ext: str) -> str:
    if ext == 'html':
        return URL_HTML
    return f'{URL_BASE}/data.{ext}'


def cleanup_local_files():
    pass


class TestWWW(unittest.TestCase):
    def test_read(self):
        cleanup_local_files()
        self.assertEqual(
            File(get_test_file('txt')).read(),
            WWW(get_test_url('txt')).read(),
        )

    def test_exists(self):
        cleanup_local_files()
        url = get_test_url('png')
        self.assertTrue(WWW(url).exists)
        self.assertFalse(WWW(url + '.1234').exists)

    def test_children(self):
        cleanup_local_files()
        url = 'https://www.python.org/'
        children = WWW(url).children
        self.assertGreater(len(children), 0)
        print(children[0].url)
        self.assertIn(children[0].url, '#')
