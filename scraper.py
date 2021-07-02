import requests
import re
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
	return BASE_URL + link.get('href')


if __name__ == "__main__":
	soup = get_soup()
	category_list = get_category_list(soup)
	for category in category_list:
		print(get_category_url(soup, category))
