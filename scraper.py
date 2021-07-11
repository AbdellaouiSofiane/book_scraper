import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

def get_soup_from_url(url=BASE_URL):
	response = requests.get(url)
	return BeautifulSoup(response.content, features="html.parser")

def get_category_list(soup):
	ul = soup.find('ul', class_='nav nav-list').find('ul')
	return [category for category in ul.stripped_strings]

def get_category_base_url(soup, category):
	regex = re.compile(rf'^\s*{category}\s*$')
	link = soup.find('a', string=regex).get('href')
	return urljoin(BASE_URL, link)

def get_next_page_url(soup, base_url):
	next_page = soup.find('li', class_="next")
	if next_page:
		return urljoin(base_url, next_page.a.get("href"))
	else:
		return

def get_books_urls_by_category(soup, category):
	book_list = []
	category_base_url = get_category_base_url(soup, category)
	page = category_base_url
	while page:
		soup = get_soup_from_url(url=page)
		books = soup.find_all('article', class_='product_pod')
		for book in books:
			book_list.append(
				urljoin(category_base_url, book.a.get('href'))
			)
		page = get_next_page_url(soup, category_base_url)
	return book_list


if __name__ == "__main__":
	soup = get_soup_from_url()
	category_list = get_category_list(soup)
	for category in category_list:
		print('in category', category)
		for book_url in get_books_urls_by_category(soup, category):
			print(book_url)
