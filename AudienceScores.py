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
    us_rating_list = []
    base_url = "https://api.watchmode.com/v1/title/{}/details/?apiKey={}" 
    for id in formatted_ids:  
        formatted_url = base_url.format(id, "phFnsumueQAmsHJRRABMsBSGUNfpnGBkcci9kyr8")
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

    for i in range(count, count+25): 
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


#Retrieve Pie Chart Data  
def retrievePieChartData(cur, conn): 
    cur.execute('''SELECT c.movie_title, a.Options FROM Maturity a
                JOIN Maturity_Scores b ON a.id = b.maturity_id
                JOIN Movies c ON c.movie_id = b.movie_id''')
    
    #SELECT c.movie_title, a.Options FROM Maturity a JOIN Maturity_Scores b ON a.id = b.maturity_id JOIN Movies c ON c.movie_id = b.movie_id
    
    data = cur.fetchall() 
    return data

#Making Pie Chart and Text File
def pieChartAndText(file, data): 
    movie_name = []
    maturity_rating = []
    options_list = ["G", "PG", "PG-13", "R", "NC-17", "Other"]
    g_count = 0 
    pg_count = 0
    pg13_count = 0
    r_count = 0 
    nc17_count = 0
    other_count = 0
    
    for i in data:
        movie_name.append(i[0])
        maturity_rating.append(i[-1]) 
    
    for rating in maturity_rating:
        if rating == "G":
            g_count += 1
        elif rating == "PG":
            pg_count +=1 
        elif rating == 'PG-13':
            pg13_count +=1
        elif rating == "R":
            r_count += 1
        elif rating == "NC-17":
            nc17_count +=1 
        elif rating == "Other":
            other_count +=1 
        
    labels = options_list 
    sizes = [g_count, pg_count, pg13_count, r_count, nc17_count, other_count]
    explode = (0, 0, 0.15, 0, 0, 0)
    colors = ('c', 'm', 'y', 'g', 'r', 'orange')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90, colors = colors, wedgeprops = {"edgecolor" : "black",
                      'linewidth': .5,
                      'antialiased': True})
    
    ax1.axis('equal')  
    plt.title('Percentage of Movies within Auidence Maturity Categories')
    plt.show() 
    
    
    dir = os.path.dirname(file)
    with open(os.path.join(dir, file), "w") as f:
         f.write(f'The total number of G rated movies is {str(g_count)}. \n')
         f.write(f'The total number of PG rated movies is {str(pg_count)}. \n')
         f.write(f'The total number of PG-13 rated movies is {str(pg13_count)}. \n')
         f.write(f'The total number of R rated movies is {str(r_count)}. \n') 
         f.write(f'The total number of NC-17 movies is {str(nc17_count)}. \n') 
         f.write(f'The total number of not rated movies is {str(other_count)}. \n') 
    
def main():
    #Run 2 times 
    cur, conn = maturityTable() 
    fillMaturityTable(cur, conn)
    movieMaturities(cur, conn)
    formatted_ids = retrieveImbdID(cur, conn)  
    
    #After 2 runs, comment out these two lines 
    us_rating_list = retrieveWatchModeScore(cur, conn, formatted_ids) 
    fillMaturity_ScoresTable(cur, conn, us_rating_list)
    
    #After commenting out retrieveWatchModeScore and fillMaturity_ScoresTable, remove the comment from pieChartAndText 
    data = retrievePieChartData(cur, conn)
    # pieChartAndText('Maturity.txt', data)
    
  
if __name__ == "__main__":
    main()