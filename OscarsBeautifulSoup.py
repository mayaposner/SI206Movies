from bs4 import BeautifulSoup
import requests 
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

def createOscarsTable():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+"Movies.db")
    cur = conn.cursor() 
    
    cur.execute("CREATE TABLE IF NOT EXISTS Oscars (movie_id INTEGER PRIMARY KEY UNIQUE, wonID INTEGER, category STRING, yearID INTEGER)")
    conn.commit()
    
def awardCatergory(soup):      
    award = soup.find_all('h2') 
    award_list = [] 
    for items in award[3:]:
        award_list.append(items.text.strip()) 
    return award_list 
    
# def awardInTable(cur, conn, award_list): 
#     for award in award_list:
#         cur.execute("INSERT OR IGNORE INTO Oscars (category) VALUES (?)", (award))
#     conn.commit()


def main():
    url = "https://www.oscars.org/oscars/ceremonies/2022"
    r = requests.get(url) 
    soup = BeautifulSoup(r.text, 'html.parser')
    
    createOscarsTable()
    awardCatergory(soup)
    # awardInTable(cur, conn, award_list)
    
    
if __name__ == "__main__":
    main()
