import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
import json 
import requests
from bs4 import BeautifulSoup

def setUpDataBase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    setUpDataBase('Movies.db')


if __name__ == "__main__":
    main()
