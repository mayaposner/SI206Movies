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
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_title TEXT UNIQUE, movie_id INTEGER PRIMARY KEY UNIQUE , yearID INTEGER)")
    conn.commit()

def createYearTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Years (year TEXT, ID INTEGER PRIMARY KEY UNIQUE)")
    conn.commit()

def retrieveIMDBdata():
    response = requests.get('https://imdb-api.com/API/AdvancedSearch/k_u7vte5gf?title_type=feature&release_date=2019-01-01,2022-01-01&groups=oscar_nominees&count=250&sort=alpha,asc')
    data = json.loads(response.text)
    movie_tuples = []
    for movies in data['results']:
        title = movies['title']
        year = movies['description'].replace('(', '').replace(')', '')
        tuple = title, int(year[-4:])
        movie_tuples.append(tuple)
    return movie_tuples

def fillYearTable(cur, conn):
    yr = 2019
    for i in range(3):
        cur.execute("SELECT max(ID) FROM Years")
        count = cur.fetchone()[0]
        if count != 2:
            cur.execute("INSERT OR IGNORE INTO Years (year, ID) VALUES (?, ?)", (yr, i))
        yr += 1
    conn.commit()

def fillMovieTable(moviestups, cur, conn):
    cur.execute("SELECT max(movie_id) FROM Movies")
    count = cur.fetchone()[0]
    if count ==  None:
        count = 0

    for i in range(count, count+25):
        try:
            title = moviestups[i][0]
            year = moviestups[i][1]
            cur.execute(f"SELECT ID from Years WHERE year = {(str(year))}")
            yearid = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO Movies (movie_title, movie_id, yearID) VALUES (?,?,?)", (title, i, yearid))
        except:
            'exceeded 100 items'

    conn.commit()

def main():
    cur, conn = setUpDataBase('Movies.db')
    createMainTable(cur, conn)
    createYearTable(cur, conn)
    fillYearTable(cur, conn)
    movies = retrieveIMDBdata()
    fillMovieTable(movies, cur, conn)


if __name__ == "__main__":
    main()
