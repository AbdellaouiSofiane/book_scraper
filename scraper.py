import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"

def get_soup(category_url=None):
	if category_url:
		url = category_url
	else:
		url = BASE_URL
	response = requests.get(url)
	return BeautifulSoup(response.content, features="html.parser")


if __name__ == "__main__":
	soup = get_soup()
	print(soup.prettify())
