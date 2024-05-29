import datetime
import os
from io import StringIO
import gzip
import shutil
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_film_data():
    if not os.path.exists('netflix_films.csv'):
        netflix_films = get_wiki_films()
        netflix_films.to_csv("netflix_films.csv", index=False)
    else:
        netflix_films = pd.read_csv("netflix_films.csv")
        netflix_films['Release date'] = pd.to_datetime(netflix_films['Release date'], format='%Y-%m-%d')

    return netflix_films


def get_film_ratings():
    if not os.path.exists('title.basics.tsv.gz'):
        response = requests.get('https://datasets.imdbws.com/title.basics.tsv.gz', stream=True)
        with open('title.basics.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.basics.tsv.gz', 'rb') as f_in:
            with open('title.basics.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    if not os.path.exists('title.ratings.tsv.gz'):
        response = requests.get('https://datasets.imdbws.com/title.ratings.tsv.gz', stream=True)
        with open('title.ratings.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.ratings.tsv.gz', 'rb') as f_in:
            with open('title.ratings.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    titles = pd.read_csv('title.basics.tsv', sep='\t')
    ratings = pd.read_csv('title.ratings.tsv', sep='\t')

    films_ratings = pd.merge(titles, ratings, how='inner')

    films_ratings.to_csv('films_ratings.csv', index=False)

def get_wiki_films():
    urls = ["https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2015–2017)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2018)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2019)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2020)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2021)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2022)",
            "https://en.wikipedia.org/wiki/List_of_Netflix_original_films_(2023)"]

    dataframes = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("table", {"class": "wikitable"})

        for table in tables:
            df = pd.read_html(StringIO(str(table)))[0]

            movie_type = table.find_previous('h2').find('span', class_='mw-headline').text
            df['Type'] = movie_type
            if movie_type == "Documentaries":
                df['Genre'] = 'Documentary'

            dataframes.append(df)

    netflix_films = pd.concat(dataframes, ignore_index=True)

    netflix_films['Release date'] = pd.to_datetime(netflix_films['Release date'], format='%B %d, %Y')

    print(netflix_films.info())
    print(netflix_films.head(10))

    return netflix_films


if __name__ == "__main__":
    get_film_ratings()