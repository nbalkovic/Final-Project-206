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
    return (request_data.json())


def get_state_populations():
    request_url_pop = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Content-type': 'text/html', 'Accept-encoding':'Identity', 'upgrade-insecure-requests': '1'}
    population_data = requests.get(request_url_pop, headers = headers)
    return(population_data.content.decode())
    

def get_social_data():
    url = ('https://gs.statcounter.com/social-media-stats/all/united-states-of-america/#daily-20200101-20200409')
    titles = {'user-agent':'This is user agent'}
    x = requests.get(url, headers = titles)
    soup = bs4.BeautifulSoup(x.text, features='lxml')
    
    all_urls = soup
    new_urls = all_urls.find(class_ = 'raphael-group-11-hot')
    return(new_urls)

def get_world_info():
    url = ('https://www.worldometers.info/coronavirus/#countries')
    titles = {'user-agent':'This is user agent'}
    x = requests.get(url, headers = titles)
    soup = bs4.BeautifulSoup(x.text, features='lxml')
    
    all_urls = soup
    new_urls = all_urls.findAll(class_ = 'sorting')
    return new_urls



#calculates number of cases per state population (cases per capita)

#VISUALIZE DATA: We just need 2 charts

#REPORT: just need to insert code and visualizations. Mostly finished with every other aspect.
#Goals: see if there is a relationship between social media use and the prevelance of COVID-19
#Problems Faced: Issues with Twitter as an API
#Include the visualizations (2 charts from earlier)
#Instructions for running code
#Explain what each function did, run through each briefly
#State resources used: Github obviously, twitter, instagram api websites for example code
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
    
    # cur.execute("SELECT count(*) FROM SOCIAL")
    # conn.commit()
    # total_social = cur.fetchone()
    # new_list.append(total_social)
    
    # cur.execute("SELECT count(*) FROM SOCIAL2")
    # conn.commit()
    # total_social2 = cur.fetchone()
    # new_list.append(total_social2)

    return new_list

cur.execute('CREATE TABLE IF NOT EXISTS POPULATIONS (state TEXT, population INTEGER)')
state_pop = get_state_populations()
state_data = (state_pop['data']['state'])
print(state_data)

def population_table(state_data):
    total_pop_record = counter()
    counter_1 = -1
    total_pop = total_pop_record[0][0]
    for item in state_data:
        counter_1+=1
        if counter_1 < int(total_pop):
            continue

        else:
            state_name = item['State']
            print(state_name)
            state_total = item['Population']
            print(state_total)
            cur.execute('INSERT INTO POPULATIONS (state, populations) VALUES (?, ?)',(state_name, state_total))
            conn.commit()
        
            if counter_1 > 18+total_pop:
                break


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
    total_social = counter()
    count_1 = -1
    for x in range(start_pos, end_pos):
        count_1 += 1
        if count_1 < int(total_social):
            continue
        else:
            state_name = item['state']
            state_total = item['positive']
            cur.execute('INSERT INTO TOTAL_SOCIAL (state, total) VALUES (?, ?)',(state_name, state_total))
            conn.commit()
            if count_1 > 18 + total_social:
                break
    #insert into table 100 days and frequency of twitter use 
    # start_pos, end_pos may be replaced by json_data


def commit():
    conn.commit()

def main():
    commit()
    counter()
    json_data = get_state_virus_data()
    total_virus_table(json_data)
    state_data = get_state_populations()
    population_table(state_data)

if __name__ == "__main__":
    main()