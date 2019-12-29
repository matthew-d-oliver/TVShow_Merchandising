#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 13:17:44 2019

@author: MatthewOliver
"""

"""
API calls to OMDb for tv_show data.
Matt Oliver Taylor Appel
"""

import omdb
import time
import pandas as pd
import mysql.connector
from config import pword, host, user, api_key
import Project_1_Webscrape_Functions as web


# define omdb client for API calls
client=omdb.OMDBClient(apikey=api_key)

def omdb_call(api_key, tv_title, tv_year):
    '''
    takes in a key to the api, a title of a tv show, and the year it was released
    returns all the imdb data from the omdb API
    '''
    data = client.get(title=tv_title,  #omdb.OMDBC requires a tv title and a release year
                      year=tv_year,
                      tomatoes=False) #tomatoes is a parameter that returns rotten tomatoes data
    return data

def get_tvshow_data(listy,api_key,year):
    '''
    takes in a list of tv shows released in the same year, and a key to the api,
    returns a Pandas Data Frame of all the imdb info on the shows
    '''
    results=[]
    for i, show in enumerate(listy):
        results.append(omdb_call(api_key,show,year))
        time.sleep(.05) #wait 50 milliseconds
    return pd.DataFrame(results)

def ship_2_sql(dflisty):
    '''
    takes in a tv show dataframe then sends the data into AWS tv show database
    first doing the merchendise data
    '''
    cnx = mysql.connector.connect(
    #connect to mysql platform        
        host =host,
        user =user,
        passwd = pword
        )
    cur=cnx.cursor()
    cur.execute('USE tv_merch')
    for i, show in dflisty.iterrows():
        print(i)
    # first pass the show data into sql
        cur.execute("""INSERT INTO show_data (
                                    show_id,
                                    show_name,
                                    genre,
                                    imdb_rating,
                                    imdb_votes,
                                    metascore,
                                    released,
                                    rated
                                    ) 
        VALUES ("{}","{}","{}","{}","{}","{}","{}","{}"
        )""".format(show['imdb_id'],
                    show['title'],
                    show['genre'],
                    show['imdb_rating'],
                    show['imdb_votes'],
                    show['metascore'],
                    show['year'],
                    show['rated']))
    # then pass the sales data into sql
#         cur.execute("""INSERT INTO merch_data (
#                                     show_id,
#                                     etsy,
#                                     ebay,
#                                     bonanza,
#                                     show_name
#                                     ) 
#         VALUES ({},{},{},{},{}
#         )""".format(show['imdb_id'],
#                     show['etsy_count'],
#                     show['ebay_count'],
#                     show['bonanza_count'],
#                     show['title']))
    cnx.commit()
    cur.close()
    cnx.close()

def program():
    '''
    brings all programs together, creating cumulative dataframe and saving to SQL
    '''
    shows_by_year=web.tv_list_makr()
    for i, year in enumerate(shows_by_year):
        shows_by
    

'''
#test code
show_name = str(input('Name: \n'))
show_year = str(input('Year: \n'))

df = pd.DataFrame(omdb_call( api_key, show_name,show_year))
df.head(1)
'''