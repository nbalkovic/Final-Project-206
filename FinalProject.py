import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os
import numpy as np 
from bs4 import BeautifulSoup
import bs4

#GET DATA

def get_state_virus_data():
    request_url_virus = 'https://covidtracking.com/api/v1/states/current.json'
    request_data = requests.get(request_url_virus)
    virus_data = json.loads(request_data.text)
    return virus_data
    #not working


def get_state_populations():
    request_url_pop = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    population_data = requests.get(request_url_pop, headers = headers)
    population_list = json.loads(population_data.text)
    return(population_list)

def get_social_data():
    url = ('https://gs.statcounter.com/social-media-stats/all/united-states-of-america/#daily-20200101-20200409')
    titles = {'user-agent':'This is user agent'}
    x = requests.get(url, headers = titles)
    soup = bs4.BeautifulSoup(x.text, features='lxml')
    
    all_urls = soup
    new_urls = all_urls.find(class_ = 'raphael-group-11-hot')
    print(new_urls)

def get_world_info():
    url = ('https://www.worldometers.info/coronavirus/#countries')
    titles = {'user-agent':'This is user agent'}
    x = requests.get(url, headers = titles)
    soup = bs4.BeautifulSoup(x.text, features='lxml')
    
    all_urls = soup
    new_urls = all_urls.findAll(class_ = 'sorting')
    return new_urls

print(get_world_info)


#calculates number of cases per state population (cases per capita)

#VISUALIZE DATA: We just need 2 charts

#REPORT
#Goals: see if there is a relationship between social media use and the prevelance of COVID-19
#Problems Faced: Issues with Twitter as an API
#Include the visualizations (2 charts from earlier)
#Instructions for running code
#Explain what each function did, run through each briefly
#State resources used: Github obviously, twitter, instagram api websites for example code

conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS POPULATIONS (state TEXT, population INTEGER)')
state_pop = get_state_populations()
state_pop_cache = state_pop['data']

def population_table(start_pos, end_pos):
    for x in range(start_pos, end_pos):
        if (x <= 52):
            row = state_pop_cache[x]
            state_name = row['State']
            state_population = row['Population']
            cur.execute('INSERT INTO POPULATIONS (state, population) VALUES (?, ?)',(state_name, state_population))
            conn.commit()
        else:
            continue
    start_pos = end_pos
    end_pos +=51
    return start_pos, end_pos

cur.execute('CREATE TABLE IF NOT EXISTS TOTAL_VIRUSES (state TEXT, total INTEGER)')
virus_total = get_state_virus_data()
#virus_total_cache = virus_total['data2']


def total_virus_table(start_pos,end_pos):
    for x in range(start_pos, end_pos):
        if(x<=52):
            #row = virus_total_cache[x]
            state_name = row['state']
            state_total = row['total']
            cur.execute('INSERT INTO TOTAL_VIRUSES (state, total) VALUES (?, ?)',(state_name, state_total))
            conn.commit()
        else:
            continue

    #insert into state and total virus count 

# def pos_neg_table(start_pos, end_pos):
#     for x in range(start_pos, end_pos):
#         if (x <= 52):
#             row = state_pop_cache[x]
#             state_name = row['State']
#             #IDK what to put virus_result = row['Virus']["Positive"]
#             row2 = virus_pop_cache[x]
#             state_name2 = row['State']
#             #virus_result2 = row["Virus"]["Result"]
#             #cur.execute('INSERT INTO TOTAL_VIRUSES (state, total) VALUES (?, ?)',(state_name, virus_result))
#             #conn.commit()
#         else:
#             continue
#     #tried starting these
#     #insert into table state(pos/neg) and according count

def social_table(start_pos, end_pos):
    pass
    #insert into table 100 days and frequency of twitter use 

def insert_twenty():
    start_pos = 0
    end_pos = 13
    for i in range(5):
        population_table(start_pos,end_pos)
        start_pos+= 13
        end_pos+= 13

def commit():
    conn.commit()

def main():
    commit()

if __name__ == "__main__":
    main()