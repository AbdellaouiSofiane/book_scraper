import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

def get_soup(category_url=None):
	if category_url:
		url = category_url
	else:
		url = BASE_URL
	response = requests.get(url)
	return BeautifulSoup(response.content, features="html.parser")

def get_category_list(soup):
	ul = soup.find('ul', {'class': 'nav nav-list'}).find('ul')
	return [category for category in ul.stripped_strings]

def get_category_url(soup, category):
	link = soup.find(
		'a',
		string=re.compile(rf'^\s*{category}\s*$')
	)
	return urljoin(BASE_URL, link.get('href'))

def get_category_books_urls(soup, category):
	category_url = get_category_url(soup, category)
	category_soup = get_soup(
		category_url=get_category_url(soup, category)
	)
	books = category_soup.find_all('article', {'class': 'product_pod'})
	return [
		urljoin(category_url, book.a.get('href')) for book in books
	]


if __name__ == "__main__":
	soup = get_soup()
	category_list = get_category_list(soup)
	for category in category_list:
		for book_url in get_category_books_urls(soup, category):
			print(book_url)
