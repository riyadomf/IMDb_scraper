# IMDb_scraper
A simple scraper that scrapes IMDb website.
* Uses requests module to fetch data as html string from the website.
* Parses html from html string and extracts necessary information through BeautifulSoup
* Creates a dataframe from those data, processes those data and handles missing value using pandas.
* Saves the pandas dataframe as csv.

# Installation
* git clone https://github.com/riyadomf/IMDb_scraper
* pip install -r requirements.txt
* run main.py
