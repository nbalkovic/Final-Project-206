import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os
import numpy as np 
from bs4 import BeautifulSoup
import bs4
import pandas as pd

def get_state_virus_data():
    request_url_virus = 'https://covidtracking.com/api/v1/states/current.json'
    request_data = requests.get(request_url_virus)
    return (request_data.json())

def get_state_populations():
    request_url_pop = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Content-type': 'text/html', 'Accept-encoding':'Identity', 'upgrade-insecure-requests': '1'}
    population_req = requests.get(request_url_pop, headers = headers)
    pop_data = (population_req.content.decode())
    population_data = json.loads(pop_data)    
    return(population_data)
    
def get_social_data():
    #request_url_social = 'https://gs.statcounter.com/social-media-stats/all/united-states-of-america/#daily-20200101-20200409'
    df = pd.read_csv('socialmediadata.csv') 
    return df

def get_daily_virus():
    request_url_virus_pos = 'https://covidtracking.com/api/us/daily'
    request_data_pos = requests.get(request_url_virus_pos)
    return (request_data_pos.json())

def get_world_info():
    world_url = 'https://api.thevirustracker.com/free-api?countryTotals=ALL'
    world_req = requests.get(world_url)
    return(world_req.json())

conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()

def counter():
    new_list = []
   
    cur.execute("SELECT count(*) FROM TOTAL_VIRUSES")
    total_virus = cur.fetchone()
    conn.commit()
    new_list.append(total_virus)
    
    cur.execute("SELECT count(*) FROM POPULATIONS")
    total_pop = cur.fetchone()
    conn.commit()
    new_list.append(total_pop)
    
    cur.execute("SELECT count(*) FROM SOCIAL")
    conn.commit()
    total_social = cur.fetchone()
    new_list.append(total_social)
    
    cur.execute("SELECT count(*) FROM WORLD")
    conn.commit()
    total_world = cur.fetchone()
    new_list.append(total_world)

    cur.execute("SELECT count(*) FROM TOTAL_DAILY")
    conn.commit()
    total_daily = cur.fetchone()
    new_list.append(total_daily)

    return new_list

cur.execute('CREATE TABLE IF NOT EXISTS TOTAL_VIRUSES (state TEXT, total INTEGER)')
json_data = get_state_virus_data()

def total_virus_table(json_data):
    total_record = counter()
    counter_1 = -1
    total_virus = total_record[0][0]
    for item in json_data:
        counter_1+=1
        if counter_1 < int(total_virus):
            continue

        else:
            state_name = item['state']
            state_total = item['positive']
            cur.execute('INSERT INTO TOTAL_VIRUSES (state, total) VALUES (?, ?)',(state_name, state_total))
            conn.commit()
        
            if counter_1 > 18+total_virus:
                break

cur.execute('CREATE TABLE IF NOT EXISTS POPULATIONS (state TEXT, population INTEGER)')
state_pop = get_state_populations()
state_data = state_pop["data"]

def population_table(state_data):
    total_pop_record = counter()
    counter_1 = -1
    total_pop = total_pop_record[1][0]
    for item in state_data:
        counter_1+=1
        if counter_1 < int(total_pop):
            continue

        else:
            state_name = item['State']
            state_total = item['Population']
            cur.execute('INSERT INTO POPULATIONS (state, population) VALUES (?, ?)',(state_name, state_total))
            conn.commit()
        
            if counter_1 > 18+total_pop:
                break


cur.execute('CREATE TABLE IF NOT EXISTS SOCIAL (date TEXT, twitter INTEGER)')

social_data =  get_social_data()

def social_table(social_data):
    total_social_count = counter()
    count_1 = -1
    total_social = total_social_count[2][0]

    for x in range(0, len(social_data.index)):
        count_1 += 1
        if count_1 < int(total_social):
            continue
        else:
            date = social_data.at[x, "Date"]
            twitter = social_data.at[x, "Twitter"]
            cur.execute('INSERT INTO SOCIAL (date, twitter) VALUES (?, ?)',(date, twitter))
            conn.commit()
            if count_1 > 18 + total_social:
                break

cur.execute('CREATE TABLE IF NOT EXISTS WORLD (country TEXT, total INTEGER)')
world_stuff = get_world_info()
world_data = world_stuff["countryitems"]

def world_table(world_data):
    total_world_record = counter()
    counter_1 = -1
    total_world = total_world_record[3][0]
    for item in world_data:
        for x in item.values():
            counter_1+=1
            if counter_1 < int(total_world):
                continue

            else:
                country_name = x['title']
                country_total = x['total_cases']
                cur.execute('INSERT INTO WORLD (country, total) VALUES (?, ?)',(country_name, country_total))
                conn.commit()
                
                if counter_1 > 18+total_world:
                    break

cur.execute('CREATE TABLE IF NOT EXISTS TOTAL_DAILY (date TEXT, positive INTEGER)')
daily_data = get_daily_virus()

def total_daily_table(daily_data):
    total_record = counter()
    counter_1 = -1
    total_daily = total_record[4][0]
    for item in daily_data:
        counter_1+=1
        if counter_1 < int(total_daily):
            continue

        else:
            date = item['date']

            positive = item['positive']
            cur.execute('INSERT INTO TOTAL_DAILY (date, positive) VALUES (?, ?)',(date, positive))
            conn.commit()
        
            if counter_1 > 18+total_daily:
                break

cur.execute('CREATE TABLE IF NOT EXISTS JOIN_TABLE (date TEXT, positive INTEGER, twitter INTEGER)')
def join_table():

    #cur.execute("SELECT t.date, t.positive, s.twitter FROM TOTAL_DAILY as t INNER JOIN SOCIAL as s ON ((substr(s.date,1,4)||substr(s.date,6,2)||substr(s.date,9,2))=t.date)")
    cur.execute("INSERT INTO JOIN_TABLE SELECT t.date, t.positive, s.twitter FROM TOTAL_DAILY as t INNER JOIN SOCIAL as s ON ((substr(s.date,1,4)||substr(s.date,6,2)||substr(s.date,9,2))=t.date)")
    conn.commit()

def commit():
    conn.commit()

def main():
    counter()

    json_data = get_state_virus_data()
    total_virus_table(json_data)

    state_pop = get_state_populations()
    state_data = state_pop["data"]
    population_table(state_data)

    world_stuff = get_world_info()
    world_data = world_stuff["countryitems"]
    world_table(world_data)

    daily_data = get_daily_virus()
    total_daily_table(daily_data)

    social_data =  get_social_data()
    social_table(social_data)

    
    join_table()
    commit()


if __name__ == "__main__":
    main()