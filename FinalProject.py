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
    #not working


def get_state_populations():
    request_url_pop = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    population_data = requests.get(request_url_pop, headers = headers)
    population_list = json.loads(population_data.text)
    return(population_list)

def get_positive_results():
    pass


def get_negative_results():
    pass
    #store 100 items from an API into a table, one table for each API

def get_social_data():
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

conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS POPULATIONS (name TEXT, population INTEGER)')
state_pop = get_state_populations()
state_pop_cache = state_pop['data']

def population_table(start_pos, end_pos):
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



def total_virus_table(start_pos,end_pos):
    pass
    #insert into state and total virus count 

def pos_neg_table(start_pos, end_pos):
    pass
    #insert into table state(pos/neg) and according count

def social_table(start_pos, end_pos):
    pass
    #insert into table 100 days and frequency of twitter use 

def insert_twenty():
    start_pos = 0
    end_pos = 13
    for i in range(20):
        population_table(start_pos,end_pos)
        start_pos+= 13
        end_pos+= 13

def commit():
    conn.commit()
    
def main():
    commit()

if __name__ == "__main__":
    main()