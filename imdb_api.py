import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests

def createRatingTable():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Movies.db")
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS IMDB_Ratings (movie_id INTEGER PRIMARY KEY, MetacriticScore INTEGER, ImdbRate INTEGER, imdb_id TEXT)")

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

def graph_ratings_movies1to30(cur, conn):
    cur.execute("SELECT Movies.movie_title, IMDB_Ratings.ImdbRate, IMDB_Ratings.MetacriticScore FROM IMDB_Ratings JOIN Movies ON Movies.movie_id = IMDB_Ratings.movie_id")
    res = cur.fetchall()[:30]
    ngroups = len(res)

    imdb = []
    meta = []
    titles = []

    for tups in res:
        title = tups[0]
        titles.append(title)
        imdbrate = tups[1]
        imdb.append(imdbrate)
        metarate = tups[2]
        meta.append(metarate)

    fig, ax = plt.subplots()
    index = np.arange(ngroups)
    bar_width = 0.25
    opacity = 0.8

    rects1 = plt.bar(index, imdb, bar_width, alpha = opacity, color = 'navy', label = "Audience Ratings") 
    rects2 = plt.bar(index + bar_width, meta, bar_width, alpha = opacity, color = 'salmon', label = "Critic Ratings")
    
    plt.xlabel('Movie')
    plt.ylabel('Ratings')
    plt.title('Ratings by Movie')
    plt.xticks(index + bar_width, titles, fontsize = 'small')
    fig.autofmt_xdate()
    plt.legend()

    plt.tight_layout()
    plt.show()

def pieChartofRatings(cur, conn):
    cur.execute("SELECT ImdbRate, MetacriticScore FROM IMDB_Ratings")
    res = cur.fetchall()

    audience_higher = 0 
    critic_higher = 0 
    tie = 0 

    for tups in res:
        audience = tups[0]
        critic = tups[1]
        if audience > critic: 
            audience_higher += 1 
        if critic > audience:
            critic_higher += 1 
        if audience == critic:
            tie += 1
    
    labels = 'Audience', 'Critic', 'Tie' 
    sizes = [audience_higher, critic_higher, tie]
    explode = (0, 0.1, 0)
    colors = ('lightgreen', 'deepskyblue', 'tomato')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90, colors = colors)
    plt.title("Do Critics or Audience Rate Movies Higher?")
    
    ax1.axis('equal')  

    plt.show()

    sizetup = (audience_higher, critic_higher, tie)
    return(sizetup)

def findAverageRatingDifference(cur, conn):
    cur.execute("SELECT ImdbRate, MetacriticScore FROM IMDB_Ratings")
    res = cur.fetchall()

    total = len(res)

    difference = 0

    for tups in res:
        audience = tups[0]
        critic = tups[1]
        dif = abs(audience - critic)
        difference += dif

    average = difference/total
    return average

def averageRatetoFile(cur, average, audience, critic, tie):

    file = open('ImdbOutfile.txt', 'w')
 
    cur.execute("SELECT max(movie_id) FROM IMDB_Ratings")
    totalintable = cur.fetchone()[0]

    file.write("Number of times (out of {}) the Audience score was greater than the Critic score: {}\n".format(totalintable, audience))
    file.write("Number of times (out of {}) the Critic score was greater than the Audience score: {}\n".format(totalintable, critic))
    file.write("Number of times (out of {}) the Audience score was the same as the Critic score: {}\n".format(totalintable, tie))

    file.write("Average difference between critic and audience rating scores: {}".format(average)) 

    
    file.close()


def main():
    cur,conn = createRatingTable()
    movieratings = retrieveIMDBdata()
    fillRatingTable(movieratings, cur, conn)
    graph_ratings_movies1to30(cur, conn)
    audience, critic, tie = pieChartofRatings(cur, conn)
    average = findAverageRatingDifference(cur, conn)
    averageRatetoFile(cur, average, audience, critic, tie)

if __name__ == "__main__":
    main()