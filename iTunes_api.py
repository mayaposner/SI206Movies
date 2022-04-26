import sqlite3
import os
import matplotlib.pyplot as plt
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
    prices_data = []
    base_url = "https://itunes.apple.com/search?"
    for year in ['2019', '2020', '2021']:
        d = {'term': year, 'media':'movie', 'limit': '70'}
        resp = requests.get(base_url, params = d)
        data = json.loads(resp.text)

        for movie in data["results"]:
            name = movie["trackName"].rstrip('(2020), (2019), (2021)')
            prices_data.append((name, movie["trackPrice"]))

    return prices_data

def addiTunesToMovies(tupls, cur, conn): 
    cur.execute("SELECT max(movie_id) FROM Movies")
    count = cur.fetchone()[0]

    cur.execute("SELECT movie_title FROM Movies")
    movies = cur.fetchall()
    movies_list = []
    for movie in movies:
        movies_list.append(movie[0].upper())

    i = count
    index = 0
    while i < count+25:
        title = tupls[index][0]
        
        inList = False
        for movie in movies_list:
            if title.upper().split()[:3] == movie.split()[:3]:
                inList = True
        if inList == False:
            i += 1
            cur.execute("INSERT OR IGNORE INTO Movies (movie_title, movie_id) VALUES (?,?)", (title, i,))
        index += 1
    
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

def writeCalculatedData(file, cur, conn):
    cur.execute('SELECT AVG (price) FROM iTunes')
    avg_price = round(cur.fetchone()[0], 2)
    cur.execute('SELECT AVG (MetacriticScore) FROM IMDB_Ratings')
    avg_rating = round(cur.fetchone()[0])
    
    cur.execute('SELECT iTunes.price, IMDB_Ratings.MetacriticScore FROM iTunes JOIN IMDB_Ratings WHERE iTunes.movieID = IMDB_Ratings.movie_id')
    data = cur.fetchall()
    conn.commit()

    prices = []
    ratings = []
    for tupl in data:
        prices.append(float(tupl[0]))
        ratings.append(int(tupl[1]))

    correlation_count = 0
    for i in range(len(prices)):
        if (prices[i] < avg_price and ratings[i] < avg_rating) or (prices[i] > avg_price and ratings[i] > avg_rating):
             correlation_count += 1
    
    dir = os.path.dirname(file)
    with open(os.path.join(dir, file), "w") as f:
         f.write(f'The average movie price for the iTunes movies that were sampled is ${str(avg_price)}.')
         f.write(f'\nThe average Metacritic Rating for the IMDB movies that were sampled is {str(avg_rating)}.')
         f.write(f'\nThere were {correlation_count} movies where a higher than average price correlated with a higher than average rating, or a lower than average price correlated with a lower than average rating.')
    
    return prices, ratings

def visualize_data(prices, ratings):
    fig, ax = plt.subplots()

    ax.scatter(prices, ratings, s=50, c='lightseagreen', marker = '^')
    plt.title('Comparing Movie Prices and Ratings')
    ax.set(xlabel = 'Prices', xlim=(5, 25), xticklabels = [str(x) for x in prices], xticks = prices,   
       ylabel = 'Ratings', ylim=(50, 100))

    plt.show()  

def main():
    # Run at least 5 times to get 100 rows of data 
    cur, conn = createTable()
    tupls = getData()
    addiTunesToMovies(tupls, cur, conn)
    fillItunesTable(tupls, cur, conn)

    # To run calculations and see visualizations, uncomment the two lines below  
    # prices, ratings = writeCalculatedData('iTunes_data.txt', cur, conn)
    # visualize_data(prices, ratings)

if __name__ == "__main__":
    main()


