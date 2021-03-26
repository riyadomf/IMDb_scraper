from imdb_scraper import scrape_imdb, data_cleaning, handle_missing_values

url = "https://www.imdb.com/search/title/"      #?groups=top_1000&ref_=adv_prv
movies = scrape_imdb(url)
movies = data_cleaning(movies)
movies = handle_missing_values(movies)
movies.to_csv('imdb_top100_movies.csv')