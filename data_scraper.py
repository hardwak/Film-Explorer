import os
from io import StringIO
import gzip
import shutil
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import timedelta


def get_film_data():
    if not os.path.exists("data_scraper/full_film_data.csv"):
        ratings = get_film_ratings()
        wiki_films = get_wiki_films()

        print('Merging film data...')

        wiki_films['Year'] = wiki_films['Release date'].dt.year.astype(str)

        ratings = ratings[['primaryTitle', 'startYear', 'averageRating', 'numVotes']]

        films_data = pd.merge(wiki_films, ratings, how='left', left_on=['Title', 'Year'],
                              right_on=['primaryTitle', 'startYear'])
        films_data.drop(columns=['primaryTitle', 'startYear', 'Year'], inplace=True)

        films_data['weighted_rating'] = films_data['averageRating'] * films_data['numVotes']

        films_data_avg_rate = films_data.groupby(['Release date', 'Title', 'Genre', 'Runtime', 'Language', 'Type']).agg(
            {
                'Release date': 'first',
                'Title': 'first',
                'Genre': 'first',
                'Runtime': 'first',
                'Language': 'first',
                'Type': 'first',
                'numVotes': 'sum',
                'weighted_rating': 'sum'
            })

        print(films_data_avg_rate.info())
        films_data_avg_rate['Rating'] = films_data_avg_rate['weighted_rating'] / films_data_avg_rate['numVotes']

        films_data_avg_rate.drop(columns=['numVotes', 'weighted_rating'], inplace=True)
        films_data_avg_rate['Rating'] = films_data_avg_rate['Rating'].round(decimals=1)

        films_data_avg_rate['Runtime'] = films_data_avg_rate['Runtime'].apply(convert_runtime)

        films_data_avg_rate.to_csv('data_scraper/full_film_data.csv', index=False)

        return films_data_avg_rate
    else:
        print("Reading films data...")
        film_data = pd.read_csv('data_scraper/full_film_data.csv')
        film_data['Release date'] = pd.to_datetime(film_data['Release date'], format='%Y-%m-%d')
        film_data['Runtime'] = film_data['Runtime'].apply(convert_runtime)
        return film_data


def convert_runtime(runtime_str: str):
    pattern = r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*min)?"
    match = re.match(pattern, runtime_str.strip())

    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0

        return timedelta(hours=hours, minutes=minutes)
    else:
        raise ValueError(f"Time format is incorrect: {runtime_str}")


def get_film_ratings():
    if not os.path.exists('data_scraper/title.basics.tsv'):
        print('Downloading and unpacking title.basics.tsv...')

        response = requests.get('https://datasets.imdbws.com/title.basics.tsv.gz', stream=True)
        with open('title.basics.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.basics.tsv.gz', 'rb') as f_in:
            with open('data_scraper/title.basics.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove('title.basics.tsv.gz')

    if not os.path.exists('data_scraper/title.ratings.tsv'):
        print('Downloading and unpacking title.ratings.tsv...')

        response = requests.get('https://datasets.imdbws.com/title.ratings.tsv.gz', stream=True)
        with open('title.ratings.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.ratings.tsv.gz', 'rb') as f_in:
            with open('data_scraper/title.ratings.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove('title.ratings.tsv.gz')

    if not os.path.exists('data_scraper/films_ratings.csv'):
        print('Merging IMDB data...')
        titles = pd.read_csv('data_scraper/title.basics.tsv', sep='\t')
        ratings = pd.read_csv('data_scraper/title.ratings.tsv', sep='\t')

        films_ratings = pd.merge(titles, ratings, how='inner')
        films_ratings.to_csv('data_scraper/films_ratings.csv', index=False)

        return films_ratings
    else:
        print('Loading IMDB data...')
        return pd.read_csv('data_scraper/films_ratings.csv')


def get_wiki_films():
    if not os.path.exists('data_scraper/netflix_wiki.csv'):
        print('Scraping Wikipedia...')

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

        netflix_wiki = pd.concat(dataframes, ignore_index=True)

        netflix_wiki['Release date'] = pd.to_datetime(netflix_wiki['Release date'], format='%B %d, %Y')

        netflix_wiki.to_csv("data_scraper/netflix_wiki.csv", index=False)
    else:
        print("Loading wikipedia data...")
        netflix_wiki = pd.read_csv("data_scraper/netflix_wiki.csv")
        netflix_wiki['Release date'] = pd.to_datetime(netflix_wiki['Release date'], format='%Y-%m-%d')

    return netflix_wiki
