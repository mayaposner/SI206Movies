
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests
from bs4 import BeautifulSoup

def createRatingTable():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Movies.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS IMDB_Ratings (movie_id INTEGER PRIMARY KEY, MetacriticScore INTEGER, ImdbRate INTEGER)")
    #cur.execute("ALTER TABLE IMDB_Ratings ADD COLUMN imdb_id TEXT") #comment this line out after you run the code once
    conn.commit()
    return cur,conn

def retrieveIMDBdata():
    response = requests.get('https://imdb-api.com/API/AdvancedSearch/k_u7vte5gf?title_type=feature&release_date=2019-01-01,2022-01-01&groups=oscar_nominees&count=250&sort=alpha,asc')
    data = json.loads(response.text)
    movie_ratings = []
    for movies in data['results']:
        meta = int(movies['metacriticRating'])
        imdb = int(float(movies['imDbRating'])*10)
        title = movies['title']
        id = movies['id']
        tuple = meta,imdb,title,id
        movie_ratings.append(tuple)
    return movie_ratings

def fillRatingTable(movieratings, cur, conn):
    #cur.execute("ALTER TABLE student ADD COLUMN Address varchar")
    cur.execute("SELECT max(movie_id) FROM IMDB_Ratings")
    count = cur.fetchone()[0]
    if count ==  None:
        count = 0

    for i in range(count, count+26):
        meta = movieratings[i][0]
        imdb = movieratings[i][1]
        title = movieratings[i][2] 
        id = movieratings[i][3]
        cur.execute(f"SELECT movie_id from Movies WHERE movie_title = ?", (title,))
        movieid = cur.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO IMDB_Ratings (movie_id, MetacriticScore, ImdbRate, imdb_id) VALUES (?,?,?,?)", (movieid, meta, imdb, id))

    conn.commit()

'''
select from oscars join ratings where movie_id.oscars = movie_id.ratings if oscars_id = 1
for data in bargraph, select from the oscars table all the movies that won oscars
for each movie, 1 bar going up to the rate out of 100 for critic reviews, and 1 bar for audience reviews'''

def main():
    cur,conn = createRatingTable()
    movieratings = retrieveIMDBdata()
    fillRatingTable(movieratings, cur, conn)

    
if __name__ == "__main__":
    main()