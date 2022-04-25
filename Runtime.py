import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests




path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+"Movies.db")
cur = conn.cursor()

# cur.execute('CREATE TABLE IF NOT EXISTS Maturity Scores (movieID INTEGER PRIMARY KEY UNIQUE, price NUMERIC)')
    
conn.commit()
cur.execute("SELECT movie_title FROM Movies")
movies = cur.fetchall() 

# print(movies) 

formatted_movies = [] 

for movie in movies:
    stripped = movie[0]
    formatted_movies.append(stripped) 
    
# print(formatted_movies)

# base_url = "https://api.watchmode.com/v1/search/?" 
base_url = "https://api.watchmode.com/v1/title/345534/details/?" 


'https://api.watchmode.com/v1/title/345534/details/?apiKey=YOUR_API_KEY&append_to_response=sources'

# https://api.watchmode.com/v1/title/tt8579674/details/?apiKey=tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T 

# apiKey=tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T&search_field=name&search_value=2019"


for movie in formatted_movies[:3]:  
    d = {"apiKey": "tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T", "search_field": "name", "search_value": movie} 
    data = requests.get(base_url, params = d) 
    data_list = json.loads(data.text)
    print(data_list)
    
    


# formated_url = base_url.get() 
# data = requests.get(base_url, d)
# data_list = json.loads(data1)
# print(data_list)