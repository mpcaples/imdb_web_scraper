import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint

headers = {'Accept-Language': 'en-US, en;q=0.5'}

titles = []
years = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

pages = np.arange(1, 1001, 50)

for page in pages: 

    page = requests.get(f'https://www.imdb.com/search/title/?groups=top_1000&start={str(page)}&ref_=adv_nxt', headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    sleep(randint(2, 10))

    # Looping over all the movies to extract data
    for container in movie_div:
        # Scraping the titles
        name = container.h3.a.text
        titles.append(name)

        # Years
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # Runtime
        runtime = container.p.find('span', class_='runtime').text
        runtimes.append(runtime)

        # imdb Ratings
        rating = float(container.strong.text)
        imdb_ratings.append(rating)

        # Metascore
        # If there is a metascore, use that, if not insert placeholder
        m_score = container.find(
            'span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        # collect both nv spans
        nv = container.find_all('span', attrs={'name': 'nv'})
        # votes
        vote = nv[0].text
        votes.append(vote)
        # grosses
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

# Initialize a data frame with pandas
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': runtimes,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})

# cleaning data
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)

movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)

movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')

movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

movies['us_grossMillions'] = movies['us_grossMillions'].map(
    lambda x: x.lstrip('$').rstrip('M'))

movies['us_grossMillions'] = pd.to_numeric(
    movies['us_grossMillions'], errors='coerce')

movies.to_csv('movies.csv')

