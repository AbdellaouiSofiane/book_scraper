# book_scraper
> Demo scraping from https://books.toscrape.com/. Get and store book's data into csv files for each category in the website.

## Requirements

* python3

## Installation

Navigate to the desired folder using your command prompt and type:

`git clone https://github.com/AbdellaouiSofiane/book_scraper.git`

Create your virtual enviroment (replace \<PATH\> with the desired location):

`python -m venv <PATH>`

Activate your virtual enviroment (see [python documentation](https://docs.python.org/fr/3/library/venv.html#creating-virtual-environments) for any trouble):

* POSIX: `source <PATH>/bin/activate`

* Windows: `C:\<PATH>\Scripts\activate.bat`

Navigate to the project directory and type :

`pip install -r requirements.txt`

## Usage

To launch the scraping process, type:

`python scraper.py`

Your command prompt should now show you which file is being written to your system.

In your project root, you should also see two new folders:
* `data/`: contains a csv file for each category.
* `images/`: contains every book' cover picture.

## Authors

Sofiane Abdellaoui - abdellaoui.sofiane.esb@gmail.com