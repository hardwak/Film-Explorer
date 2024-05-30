import os
from io import StringIO
import gzip
import shutil
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_film_data():
    if not os.path.exists("full_film_data.csv"):
        ratings = get_film_ratings()
        wiki_films = get_wiki_films()

        print('Merging film data...')

        wiki_films['Year'] = wiki_films['Release date'].dt.year.astype(str)

        ratings = ratings[['primaryTitle', 'startYear', 'averageRating', 'numVotes']]

        films_data = pd.merge(wiki_films, ratings, how='left', left_on=['Title', 'Year'],
                              right_on=['primaryTitle', 'startYear'])
        films_data.drop(columns=['primaryTitle', 'startYear', 'Year'], inplace=True)

        films_data['weighted_rating'] = films_data['averageRating'] * films_data['numVotes']

        films_data_avg_rate = films_data.groupby(['Release date', 'Title', 'Genre', 'Runtime', 'Language', 'Type']).agg({
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

        films_data_avg_rate.to_csv('full_film_data.csv', index=False)

        return films_data_avg_rate
    else:
        print("Reading films data...")
        return pd.read_csv('full_film_data.csv')


def get_film_ratings():
    if not os.path.exists('title.basics.tsv'):
        print('Downloading and unpacking title.basics.tsv...')

        response = requests.get('https://datasets.imdbws.com/title.basics.tsv.gz', stream=True)
        with open('title.basics.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.basics.tsv.gz', 'rb') as f_in:
            with open('title.basics.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove('title.basics.tsv.gz')

    if not os.path.exists('title.ratings.tsv'):
        print('Downloading and unpacking title.ratings.tsv...')

        response = requests.get('https://datasets.imdbws.com/title.ratings.tsv.gz', stream=True)
        with open('title.ratings.tsv.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        with gzip.open('title.ratings.tsv.gz', 'rb') as f_in:
            with open('title.ratings.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove('title.ratings.tsv.gz')

    if not os.path.exists('films_ratings.csv'):
        print('Merging IMDB data...')
        titles = pd.read_csv('title.basics.tsv', sep='\t')
        ratings = pd.read_csv('title.ratings.tsv', sep='\t')

        films_ratings = pd.merge(titles, ratings, how='inner')
        films_ratings.to_csv('films_ratings.csv', index=False)

        return films_ratings
    else:
        print('Loading IMDB data...')
        return pd.read_csv('films_ratings.csv')


def get_wiki_films():
    if not os.path.exists('netflix_wiki.csv'):
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

        netflix_wiki.to_csv("netflix_wiki.csv", index=False)
    else:
        print("Loading wikipedia data...")
        netflix_wiki = pd.read_csv("netflix_wiki.csv")
        netflix_wiki['Release date'] = pd.to_datetime(netflix_wiki['Release date'], format='%Y-%m-%d')

    return netflix_wiki


if __name__ == "__main__":
    films = get_film_data()
    print(films.info())
