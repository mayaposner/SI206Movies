import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests

def createTable():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Movies.db")
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS iTunes (movieID INTEGER PRIMARY KEY UNIQUE, price NUMERIC)')
    
    conn.commit()

    return cur, conn

def getData():
    data_tupls = []
    base_url = "https://itunes.apple.com/search?"
    for year in ['2019', '2020', '2021']:
        d = {'term': year, 'media':'movie', 'limit': '65'}
        resp = requests.get(base_url, params = d)
        data = json.loads(resp.text)

        for movie in data["results"]:
            name = movie["trackName"].rstrip('(2020), (2019), (2021)')
            data_tupls.append((name, movie["trackPrice"], year))

    return data_tupls

def addiTunesToMovies(tupls, cur, conn): 
    cur.execute("SELECT max(movie_id) FROM Movies")
    count = cur.fetchone()[0]

    cur.execute("SELECT movie_title FROM Movies")
    movies = cur.fetchall()
    movies_list = []
    for movie in movies:
        movies_list.append(movie[0].upper())

    for i in range(count, count+25):
        title = tupls[abs(i - len(tupls))][0]
        year = tupls[i - len(tupls)][2]
        cur.execute(f"SELECT ID from Years WHERE year = {(str(year))}")
        yearid = cur.fetchone()[0]
        if title.upper() not in movies_list:
            cur.execute("INSERT OR IGNORE INTO Movies (movie_title, movie_id, yearID) VALUES (?,?,?)", (title, i, yearid))

    conn.commit()

def fillItunesTable(tupls, cur, conn):
    cur.execute("SELECT COUNT (*) FROM iTunes")
    count = cur.fetchone()[0]

    for i in range(count, count+26):
        title = tupls[i][0]
        price = tupls[i][1]
        cur.execute(f'SELECT movie_id from Movies where movie_title = "{title}"')
        try:
            id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO iTunes (movieID, price) VALUES (?,?)", (id, price))
        except:
            "Not in movies database table"
        
    conn.commit()

def main():
    cur, conn = createTable()
    tupls = getData()
    addiTunesToMovies(tupls, cur, conn)
    fillItunesTable(tupls, cur, conn)

if __name__ == "__main__":
    main()