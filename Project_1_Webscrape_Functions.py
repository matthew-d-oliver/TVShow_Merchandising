#!/usr/bin/env python
# coding: utf-8



# Importing all the libraries we need and likely a lot we don't need.
# We used mostly re, requests, bs4, and selenium in this notebook
import re
import os
import time
import random
import requests
import numpy as np
import pandas as pd
from os import system
from math import floor
from copy import deepcopy
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Don't think I used this but I may have when I used selenium for webscraping Wikipedia
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)


# ## Writing the functions to webscrape for merchandise results


# This function will start by finding the ebay url for any tv show we call
# We then use beautiful soup to pull and parse the data as html text
# From there we tell it to search for the class that contains the number of results for our search
# Then we clean the returned text as necessary so we grab only the number
# Finally, we return a dictionary that labels the number of results as an integer and the name of the show
def ebay_results(tv_name):
    results = []
    for name in tv_name:
        name = name.replace(' ', '+').lower()
        url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw="+name+"+tv+show&_sacat=0"
        link = requests.get(url)
        link_soup = BS(link.content, 'html.parser')
        links = link_soup.find(class_='srp-controls__count-heading').text.split()[0].replace(',','')
        results.append({'Results' : int(links), 'Show': name.title().replace('+', ' ')})
    return results


'''
# This function will start by finding the bonanza url for any tv show we call
# We then use beautiful soup to pull and parse the data as html text
# From there we tell it to search for the class that contains the number of results for our search
# Then we clean the returned text as necessary so we grab only the number
# Finally, we return a dictionary that labels the number of results as an integer and the name of the show
'''
def bonanza_results(tv_name):
    results = []
    for name in tv_name:
        name = name.replace(' ', '%20').lower()
        url = """https://www.bonanza.com/items/search?q[catalog_id]=&q[country_to_filter]=
                 US&q[filter_category_id]=&q[in_booth_id]=&q[ship_country]=1&q[shipping_in_price]=
                 0&q[sort_by]=relevancy&q[suggestion_found]=&q[translate_term]=true&q[search_term]=
                 """+name+"""%20tv%20show"""
        link = requests.get(url)
        link_soup = BS(link.content, 'html.parser')
        links = link_soup.find(id='listing_count_number').text.replace(',','')
        results.append({'Results' : int(links), 'Show': name.title().replace('%20', ' ') })
    return results



# This function will start by finding the etsy url for any tv show we call
# We then use beautiful soup to pull and parse the data as html text
# From there we tell it to search for the class that contains the number of results for our search
# Then we clean the returned text as necessary so we grab only the number
# Finally, we return a dictionary that labels the number of results as an integer and the name of the show
def etsy_results(tv_name):
    results = []
    for name in tv_name:
        name = name.replace(' ', '%20').replace('&', 'and').lower()
        url = """https://www.etsy.com/search?q="""+name+"""%20tv%20show"""
        link = requests.get(url)
        time.sleep(random.choice([x/10 for x in range(8,14)]))
        link_soup = BS(link.content, 'html.parser')
        links = link_soup.find(class_='float-left wt-pt-lg-2 wt-nudge-b-1').text.split()[-2].replace('(', '').replace(',','') if link_soup.find(class_='float-left wt-pt-lg-2 wt-nudge-b-1') else 0
        results.append({'Results' : int(links), 'Show': name.title().replace('%20', ' ')})
    return results 


# ## Webscraping Wikipedia for a list of currently running shows since


# Use the webdriver to open chrome through selenium
driver = webdriver.Chrome()




# Set the driver to a specific url and open the browser
driver.get('https://en.wikipedia.org/wiki/List_of_American_television_programs_currently_in_production#2010s')




# Grab the whole list of shows from this specific class
list_of_shows = driver.find_elements_by_class_name('mw-parser-output')


def tv_list_makr():
    # Convert it into a string of text separated by a line
    # Pull only the show names from 2010 onwards and omit everything after the last show in 2019
    show = str(list_of_shows[0].text).split('\n')
    shows = show[480:1279]
    shows
    
    
    
    
    # Set an empty list which we will then add our shows to
    shows_2010 = []
    shows_2011 = []
    shows_2012 = []
    shows_2013 = []
    shows_2014 = []
    shows_2015 = []
    shows_2016 = []
    shows_2017 = []
    shows_2018 = []
    shows_2019 = []
    # Write a for loop that will take every show within the year we want
    # Use .index() to find the exact string we want to start and stop at
    # Clean the data so we get only the show's name and nothing after (there were parentheses with years that were unnecessary)
    # Append the results to the appropriate list
    for show in shows:
        if shows.index(show) > shows.index('2010[edit]') and shows.index(show) < shows.index('2011[edit]'):
            shows_2010.append(re.sub("\(.+\)",'',show)) 
        elif shows.index(show) > shows.index('2011[edit]') and shows.index(show) < shows.index('2012[edit]'):
            shows_2011.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2012[edit]') and shows.index(show) < shows.index('2013[edit]'):
            shows_2012.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2013[edit]') and shows.index(show) < shows.index('2014[edit]'):
            shows_2013.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2014[edit]') and shows.index(show) < shows.index('2015[edit]'):
            shows_2014.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2015[edit]') and shows.index(show) < shows.index('2016[edit]'):
            shows_2015.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2016[edit]') and shows.index(show) < shows.index('2017[edit]'):
            shows_2016.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2017[edit]') and shows.index(show) < shows.index('2018[edit]'):
            shows_2017.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2018[edit]') and shows.index(show) < shows.index('2019[edit]'):
            shows_2018.append(re.sub("\(.+\)",'',show))
        elif shows.index(show) > shows.index('2019[edit]'):
            shows_2019.append(re.sub("\(.+\)",'',show))
            
    all_shows=[ shows_2010,
            shows_2011,
            shows_2012,
            shows_2013,
            shows_2014,
            shows_2015,
            shows_2016,
            shows_2017,
            shows_2018,
            shows_2019]
    return all_shows
    





