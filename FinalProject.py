import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os
import numpy as np 
#GET DATA

def get_state_virus_data():
    request_url_virus = 'https://covidtracking.com/api/v1/states/current.json'
    request_data = requests.get(request_url_virus)
    virus_data = json.loads(request_data.text)
    return virus_data


def get_state_populations():
    request_url_pop = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    population_data = requests.get(request_url_pop, headers = headers)
    population_list = json.loads(population_data.text)
    return(population_list)

def create_table():
    pass
    #store 100 items from an API into a table, one table for each API

#PROCESS DATA

def count_state_cases():
    request_url = 'https://covidtracking.com/api/v1/states/current.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    virus_data = requests.get(request_url, headers = headers)
    ordered_cases = []
    for state in virus_data:
        ordered_cases.append(state)
    print(ordered_cases)
    return sorted(ordered_cases, key = lambda x: x[1], reverse=True)

def get_twitter_data():
    pass

def cases_per_pop():
    pass



#calculates number of cases per state population (cases per capita)

#VISUALIZE DATA: We just need 2 charts

#REPORT
#Goals:
#Problems Faced: Issues with Twitter as an API
#Include the visualizations (2 charts from earlier)
#Instructions for running code
#Explain what each function did, run through each briefly
#State resources used

conn = sqlite3.connect('final.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS POPULATIONS (name TEXT, population INTEGER)')
state_pop = get_state_populations()
state_pop_cache = state_pop['data']

def insert_states(start_pos, end_pos):
    for x in range(start_pos, end_pos):
        if (x <= 52):
            row = state_pop_cache[x]
            _name = row['State']
            _population = row['Population']
            cur.execute('INSERT INTO POPULATIONS (name, population) VALUES (?, ?)',(_name, _population))
            conn.commit()
        else:
            continue
    start_pos = end_pos
    end_pos += 13
    return start_pos, end_pos



def call():
    start_pos = 0
    end_pos = 13
    for i in range(4):
        insert_states(start_pos,end_pos)
        start_pos+= 13
        end_pos+= 13