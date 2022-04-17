
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests
from bs4 import BeautifulSoup

def createMainTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS IMDB_Ratings (movie_id INTEGER PRIMARY KEY, MetacriticScore INTEGER, ImdbRate INTEGER)")
    conn.commit()

def retrieveIMDBdata():
    response = requests.get('https://imdb-api.com/API/AdvancedSearch/k_u7vte5gf?title_type=feature&release_date=2019-01-01,2022-01-01&groups=oscar_nominees&count=250&sort=alpha,asc')
    data = json.loads(response.text)
    movie_ratings = []
    for movies in data['results']:
        title = movies['title']
        year = movies['description'].replace('(', '').replace(')', '')
        tuple = title, int(year[-4:])
        movie_tuples.append(tuple)
    return movie_tuples
