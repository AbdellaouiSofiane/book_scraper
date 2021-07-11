import requests
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path


BASE_URL = "http://books.toscrape.com/"
FIELDNAMES = [
	'product_page_url',
	'universal_ product_code (upc)',
	'title',
	'price_including_tax',
	'price_excluding_tax',
	'product_description',
	'number_available',
	'category',
	'review_rating',
	'image_url'
]

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
	return {
		'product_page_url': url,
		'universal_ product_code (upc)': get_UPC(soup),
		'title': get_title(soup),
		'price_including_tax': get_price_incl_tax(soup),
		'price_excluding_tax': get_price_excl_tax(soup),
		'number_available': get_availability(soup),
		'product_description': get_description(soup),
		'review_rating': get_rating(soup),
		'image_url': get_image_url(soup, url)
	}


if __name__ == "__main__":
	soup = get_soup_from_url()
	category_list = get_category_list(soup)
	Path("data/").mkdir(parents=True, exist_ok=True)
	for category in category_list:
		print(f'Writing csv file for category: {category}')
		with open(f'data/{category}.csv', 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
			writer.writeheader()
			for book_url in get_books_urls_by_category(soup, category):
				data = get_book_data(book_url)
				data['category'] = category
				writer.writerow(data)
