import unittest
import requests
from bs4 import BeautifulSoup

from scraper import *


class SoupTestCase(unittest.TestCase):

	def setUp(self):
		self.base_url = "http://books.toscrape.com/"

	def test_response_from_base_url(self):
		response = requests.get(self.base_url)
		self.assertTrue(response.ok)
		self.assertIsNotNone(response.content)

	def test_get_soup_with_no_url(self):
		self.assertIsInstance(get_soup(), BeautifulSoup)


if __name__ == '__main__':
    unittest.main()
