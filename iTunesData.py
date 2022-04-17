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

def getData():
    base_url = "https://itunes.apple.com/search?"
    #cur.execute(SELECT ...)
    #movies = cur.fectchall()
    for movie in movies:
        d = {'term': year, 'media': 'movie', 'limit': 25}
        resp = requests.get(base_url, params = d)
        data = json.loads(resp.text)


def main():
    createTable()
    

if __name__ == "__main__":
    main()