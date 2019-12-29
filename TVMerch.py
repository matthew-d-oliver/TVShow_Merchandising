#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:53:55 2019

@author: MatthewOliver
"""

from datetime import datetime
import sqlite3
import pandas as pd
conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()
import json

f=open('students.json','r')
data=json.load(f)
keys_list = []
for student in data:
    print(student['name'])
    keys = student.keys()
    for word in keys:
        if word not in keys_list:
            keys_list.append(word)
print (keys_list)



cnx = mysql.connector.connect(
    host = config.host,
    user = config.user,
    passwd = config.pword
)
db='class_info'
cursor = cnx.cursor()
#cur.execute('USE class_info')
for student in data:
     cur.execute("""INSERT INTO class_info (name, dob, siblings, birthplace, yearinnyc, favoritefood) 
     VALUES ('{name}',
     '{birthdate}', 
     '{siblings}',
     '{Birthplace}',
     '{yearsinnyc}',
     '{favoritefood}'
     )""".format(**student))
cnx.commit()
cursor.close()
cnx.close()

new_dates=[]
for i, datestr in enumerate(listy):
    if datestr==None:
        j=None
    elif datestr[0][0].isdigit():
        j=datetime.strptime(datestr[0],'%m/%a/%Y')
    else:
        j=datetime.strptime(datestr[0],'%B/%a/%Y')
    new_dates.append(j)