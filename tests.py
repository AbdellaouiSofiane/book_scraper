import unittest
import requests
import re
from bs4 import BeautifulSoup
from slugify import slugify

from scraper import *


class SoupTestCase(unittest.TestCase):

	def setUp(self):
		self.base_url = "http://books.toscrape.com/"

	def build_category_url_regex(self, category, index):
		category_slug = slugify(category)
		return re.compile(
			rf'^{self.base_url}catalogue/category/books/{category_slug}_{index}/index.html$'
		)

	def test_response_from_base_url(self):
		response = requests.get(self.base_url)
		self.assertTrue(response.ok)
		self.assertIsNotNone(response.content)

	def test_get_soup_with_no_url(self):
		self.assertIsInstance(get_soup(), BeautifulSoup)

	def test_get_category_list(self):
		soup = get_soup()
		category_list = get_category_list(soup)
		self.assertIsInstance(category_list, list)
		self.assertEqual(len(category_list), 50)

	def test_get_category_url(self):
		soup = get_soup()
		category_list = get_category_list(soup)
		index = 2
		for category in category_list:
			category_url = get_category_url(soup, category)
			self.assertRegex(
				category_url,
				self.build_category_url_regex(category, index)
			)
			index += 1


if __name__ == '__main__':
    unittest.main()
