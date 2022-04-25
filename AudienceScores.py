import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests


#Making Maturity Table (IDs)
def maturityTable():  
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Movies.db")
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS Maturity (id INTEGER PRIMARY KEY NOT NULL, Options TEXT)")
    conn.commit()
    return cur,conn 

# Filling Maturity Table (IDs)
def fillMaturityTable(cur, conn):
    options_list = ["G", "PG", "PG-13", "R", "NC-17", "Other"]  
    
    for i in range(len(options_list)):
        cur.execute("INSERT or IGNORE INTO Maturity (id,Options) VALUES (?,?)",(i ,options_list[i]))
    conn.commit()
    
# Making Movie Scores Table
def movieMaturities(cur, conn): 
    cur.execute('CREATE TABLE IF NOT EXISTS Maturity_Scores (movie_id INTEGER PRIMARY KEY UNIQUE, maturity_id NUMERIC)')
    conn.commit()
    
# Getting imbd's movie ids
def retrieveImbdID(cur, conn):
    formatted_ids = [] 
    cur.execute("SELECT imdb_id FROM IMDB_Ratings")
    imdb_identification = cur.fetchall() 
    for id in imdb_identification:
        formatted_ids.append(id[0]) 
        
    return formatted_ids  


def retrieveWatchModeScore(cur, conn, formatted_ids):
    # 'https://api.watchmode.com/v1/title/345534/details/?apiKey=YOUR_API_KEY&append_to_response=sources'
    us_rating_list = []
    base_url = "https://api.watchmode.com/v1/title/{}/details/?apiKey={}" 
    for id in formatted_ids:  
        formatted_url = base_url.format(id, "3usXCfkfRIArzEbI7JQM2oeiDlbuSCAqgYTv64h0")
        # formatted_url = base_url.format(id, "tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T")
        # d = {"apiKey": "tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T", "title_id": id} 
        # data = requests.get(base_url, params = d) 
        data = requests.get(formatted_url)
        data_list = json.loads(data.text)
        try:
            maturity = data_list['us_rating']
            cur.execute(f"SELECT movie_id from IMDB_Ratings WHERE imdb_id = ?", (id,))
            movieid = cur.fetchone()[0]
            tups = (movieid, maturity)
            us_rating_list.append(tups)
        except:
            continue

    return us_rating_list

# Filling Maturity_scores Table
def fillMaturity_ScoresTable(cur, conn, us_rating_list): 
    options_list = ["G", "PG", "PG-13", "R", "NC-17", "Other"] 
    
    cur.execute("SELECT max(movie_id) FROM Maturity_Scores")
    count = cur.fetchone()[0]
    if count ==  None:
        count = 0 

    for i in range(count, count+26): 
        # SYDNEY LOOK AT?
        id = us_rating_list[i][0] 
        score = us_rating_list[i][1]
        if score in options_list: 
            cur.execute(f"SELECT id from Maturity WHERE Options = ?", (score,))
            maturity = cur.fetchone()[0] 
        else: 
            cur.execute("SELECT id from Maturity WHERE Options = 'Other'")
            maturity = cur.fetchone()[0] 
        cur.execute("INSERT or IGNORE INTO Maturity_Scores (movie_id,maturity_id) VALUES (?,?)",(id, maturity))
    conn.commit()
    


# Making pie chart with Movie Names and Maturity Score (not ID) -- DO THIS ONE

        
    


def main():
    cur, conn = maturityTable() 
    fillMaturityTable(cur, conn)
    movieMaturities(cur, conn)
    formatted_ids = retrieveImbdID(cur, conn)  
    us_rating_list = retrieveWatchModeScore(cur, conn, formatted_ids) 
    fillMaturity_ScoresTable(cur, conn, us_rating_list)
    
  
if __name__ == "__main__":
    main()