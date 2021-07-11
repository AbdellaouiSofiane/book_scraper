import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pprint

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
		return None

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

def get_UPC(soup):
	return soup.find('th', string="UPC").find_next_sibling().string

def get_title(soup):
	return soup.find('h1').string

def get_price_incl_tax(soup):
	return soup.find('th', string="Price (incl. tax)") \
		.find_next_sibling().string

def get_price_excl_tax(soup):
	return soup.find('th', string="Price (excl. tax)") \
		.find_next_sibling().string

def get_description(soup):
	description = soup.find('div', id="product_description")
	if description:
		return description.find_next_sibling().string
	else:
		return ""

def get_availability(soup):
	availability = soup.find('th', string="Availability") \
		.find_next_sibling().string
	return re.compile(r"\d+").search(availability).group()

def get_image_url(soup, url):
	return urljoin(
		url,
		soup.find('div', class_="item active").find('img').get('src')
	)

def get_rating(soup):
	return soup.find('p', class_="star-rating").get('class')[1]

def get_book_data(url):
	soup = get_soup_from_url(url)
	data = {
		'url': url,
		'UPC': get_UPC(soup),
		'title': get_title(soup),
		'price_incl_tax': get_price_incl_tax(soup),
		'price_excl_tax': get_price_excl_tax(soup),
		'description': get_description(soup),
		'availability': get_availability(soup),
		'image_url': get_image_url(soup, url),
		'rating': get_rating(soup)
	}
	return data


if __name__ == "__main__":
	soup = get_soup_from_url()
	category_list = get_category_list(soup)
	for category in category_list:
		print('in category', category)
		for book_url in get_books_urls_by_category(soup, category):
			pprint.pprint(get_book_data(book_url))
