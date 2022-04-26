import sqlite3
import os
import json 
import requests

def setUpDataBase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createMainTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_title TEXT UNIQUE, movie_id INTEGER PRIMARY KEY UNIQUE)")
    conn.commit()

def retrieveIMDBdata():
    response = requests.get('https://imdb-api.com/API/AdvancedSearch/k_u7vte5gf?title_type=feature&release_date=2019-01-01,2022-01-01&groups=oscar_nominees&count=250&sort=alpha,asc')
    data = json.loads(response.text)
    movie_titles = []
    for movies in data['results']:
        title = movies['title']
        movie_titles.append(title)
    return movie_titles

def fillMovieTable(movies, cur, conn):
    cur.execute("SELECT max(movie_id) FROM Movies")
    count = cur.fetchone()[0]
    if count ==  None:
        count = 0

    for i in range(count, count+25):
        try:
            title = movies[i]
            cur.execute("INSERT OR IGNORE INTO Movies (movie_title, movie_id) VALUES (?,?)", (title, i))
        except:
            'exceeded 100 items'

    conn.commit()

def main():
    cur, conn = setUpDataBase('Movies.db')
    createMainTable(cur, conn)
    movies = retrieveIMDBdata()
    fillMovieTable(movies, cur, conn)


if __name__ == "__main__":
    main()
