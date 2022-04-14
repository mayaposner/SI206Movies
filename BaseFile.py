import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests
from bs4 import BeautifulSoup

def setUpDataBase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createMainTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_title TEXT, movie_id INTEGER PRIMARY KEY UNIQUE , year INTEGER, yearID INTEGER)")
    conn.commit()

def retrieveIMDBdata(filename, cur, conn):
    response = requests.get('https://imdb-api.com/API/AdvancedSearch/k_u7vte5gf?title_type=feature&release_date=2019-01-01,2022-01-01&groups=oscar_nominees&count=250&sort=alpha,asc')
    data = json.loads(response.text)
    movie_tuples = []
    for movies in data['results']:
        title = movies['title']
        year = movies['description'].replace('(', '').replace(')', '')
        tuple = title, year
        movie_tuples.append(tuple)
    return movie_tuples

def fillMovieTable(moviestups, filename, cur, conn):
    indexvar = 25 
    for i in range(len):
        cur.execute("INSERT OR IGNORE INTO Movies (movie_title, movie_id, year, yearID")

def main():
    cur, conn = setUpDataBase('Movies.db')
    createMainTable(cur, conn)
    movies = retrieveIMDBdata('Movies.db', cur, conn)
    fillMovieTable(movies, 'Movies.db' , cur, conn)


if __name__ == "__main__":
    main()
