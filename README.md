# imdb_scraper
A simple scraper that scrapes IMDb website.
* Uses requests module to fetch data as html string from the website.
* Parses html from html string and extracts necessary information through BeautifulSoup
* Creates a dataframe from those data, processes those data and handles missing value using pandas.
* Saves the pandas dataframe as csv.
