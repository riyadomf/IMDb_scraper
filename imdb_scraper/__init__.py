import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np        
from time import sleep
from random import randint

def scrape_imdb(url):         
    pages = np.arange(1,1001,50)
    titles = []
    years = []
    time = []
    imdb_ratings = []
    metascores = []
    votes = []
    us_gross = []

    for page in pages:        
        '''step1: Fetch data as html string through http requests'''
        headers = {"Accept-Language": "en-US, en;q=0.5"}
        params = {"groups" : "top_1000",
                "sort"   : "user_rating",
                "start"  : page,
                "ref_"   : "adv_nxt"    
                }
        res = requests.get(url, headers = headers, params = params)

        '''step2: Parse html from html string and extract necessary information through BeautifulSoup''' 
        soup = BeautifulSoup(res.text, "html.parser")
        movie_div = soup.find_all("div", class_ = "lister-item mode-advanced")
        #sleep(randint(2,3))                #taking time for each iteration so that server can handle requests
        
        '''step3: Storing the extracted data into lists'''
        for container in movie_div:
            title = container.h3.a.text
            titles.append(title)
            year = container.h3.find("span", class_="lister-item-year").text 
            years.append(year)
            runtime = container.p.find("span", class_ = "runtime").text if container.p.find("span", class_ = "runtime") else '-'
            time.append(runtime)
            rating = float(container.strong.text)
            imdb_ratings.append(rating)
            metascore = container.find("span", class_ = "metascore").text if container.find("span", class_ = "metascore") else '-'
            metascores.append(metascore)
            vote_gross = container.find_all("span", attrs = {"name": "nv"} )
            vote = vote_gross[0].text
            votes.append(vote)
            gross = vote_gross[1].text if len(vote_gross)>1 else '-'
            us_gross.append(gross)

    '''step4: Creating a dataframe from those data'''
    movies = pd.DataFrame({
        'movie'    : titles,
        'year'     : years,
        'timeMin'  : runtime,
        'imdb'     : imdb_ratings,
        'metascore': metascores,
        'votes'    : vote,
        'us_grossMillions' : us_gross
    })
    return movies



'''
Data quality and data cleaning:
  ->Check data-type constraints, mandatory constraints and regular expression patterns.
  ->Convert each coloumn into proper data type
  ->print(movies.dtypes) : to see data types of each coloumn
'''
def data_cleaning(movies):
    movies["year"] = movies["year"].str.extract(r'(\d+)').astype(int)                                   #get rid of brackets
    movies["timeMin"] = movies["timeMin"].str.extract(r'(\d+)').astype(int)                             #get rid of 'Min'

    movies["metascore"] = movies["metascore"].str.extract(r'(\d+)')
    movies["metascore"] = pd.to_numeric(movies["metascore"], errors = "coerce")                      

    movies["votes"] = movies["votes"].str.replace(',','').astype(int)

    movies["us_grossMillions"] = movies["us_grossMillions"].map(lambda x:x.lstrip('$').rstrip('M'))     #iterable.map(lambda)     to get rid of '$' and 'M'
    movies["us_grossMillions"] = pd.to_numeric(movies["us_grossMillions"], errors = "coerce")           #pd.to_numeric() is used bcs astype() would throw error when dashes occurs in the coloumn.
                                                                                                        #    (errors = 'coerce') will transform the non-numeric values(dashes) into NaN(not a number)
    return movies




def handle_missing_values(movies):                                                                
    movies.metascore = movies.metascore.fillna("None Given")        #default value for missing data 
    movies.us_grossMillions = movies.us_grossMillions.fillna("Not calculated")    #but the data type will also be changed from int into object
    return movies