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
    return cur, conn
    
def awardCatergory(soup):      
    award = soup.find_all('h2') 
    award_list = [] 
    for items in award[3:]:
        award_list.append(items.text.strip()) 
    return award_list 

# def createAwardIdTable3(cur, conn):
#     cur.execute("CREATE TABLE IF NOT EXISTS Awards3 (category TEXT, ID INTEGER PRIMARY KEY NOT NULL)")
#     conn.commit()
    
        
# def fillAwardTable3(cur, conn, award_list):
#     for award in range(len(award_list)):
#         cur.execute("INSERT OR IGNORE INTO Awards3 (category, ID) VALUES (?, ?)", (award, award_list[award]))
#     conn.commit()  

def fillYearsID(cur, conn): 
    pass
    

def main():
    url = "https://www.oscars.org/oscars/ceremonies/2021"
    r = requests.get(url) 
    soup = BeautifulSoup(r.text, 'html.parser')
    
    cur, conn = createOscarsTable()
    award_list = awardCatergory(soup)
    createAwardIdTable3(cur, conn)
    fillAwardTable3(cur, conn, award_list)
    fillYearsID(cur, conn)
    
    
if __name__ == "__main__":
    main()
