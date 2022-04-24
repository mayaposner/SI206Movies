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
    options_list = ["G", "PG", "PG-13", "R", "NC-17"]  
    
    for i in range(len(options_list)):
        cur.execute("INSERT or IGNORE INTO Maturity (id,Options) VALUES (?,?)",(i ,options_list[i]))
    conn.commit()
    
# Making Movie Scores Table
def movieMaturities(cur, conn): 
    cur.execute('CREATE TABLE IF NOT EXISTS Maturity_Scores (imdb_ID INTEGER PRIMARY KEY UNIQUE, maturity_id NUMERIC)')
    conn.commit()
    
# Getting imbd's movie ids -- FIX THIS ONE
def retrieveImbdID(cur, conn):
    formatted_ids = [] 
    cur.execute("SELECT imdb_id FROM IMDB_Ratings")
    imdb_identification = cur.fetchall() 
    for id in imdb_identification:
        formatted_ids.append(id[0]) 
        
    return formatted_ids  

# Filling Maturity_Scores Table With imbd_ID and maturity_ID -- DO THIS ONE

# Making pie chart with Movie Names and Maturity Score (not ID) -- DO THIS ONE

def retrieveWatchModeScore(cur, conn, formatted_ids):
    # 'https://api.watchmode.com/v1/title/345534/details/?apiKey=YOUR_API_KEY&append_to_response=sources'
    base_url = "https://api.watchmode.com/v1/{}/345534/details/?" 
    for id in formatted_ids:  
        # formatted_url = base_url.format(id, apiKey)
        d = {"apiKey": "tFJ9E73Y4k9GLjhJD7i2LR0aoKHj5MAtzYiaWg2T", "search_field": "name", "search_value": id} 
        data = requests.get(base_url, params = d) 
        data_list = json.loads(data.text)
    print(data_list)
    return data_list
    
        
    


def main():
    cur, conn = maturityTable() 
    fillMaturityTable(cur, conn)
    movieMaturities(cur, conn)
    formatted_ids = retrieveImbdID(cur, conn)  
    retrieveWatchModeScore(cur, conn, formatted_ids)
    
    
  
if __name__ == "__main__":
    main()