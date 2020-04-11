import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os

#GET DATA

def get_state_virus_data():
    request_url = 'https://covidtracking.com/api/v1/states/current.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    virus_data = requests.get(request_url, headers = headers)
    return (virus_data)

def get_state_populations():
    request_url = 'https://datausa.io/api/data?drilldowns=State&measures=Population&year=latest'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    population_data = requests.get(request_url, headers = headers)
    population_list = json.loads(population_data.text)
    return (population_list)
def create_table():
    #store 100 items from an API into a table, one table for each API

#PROCESS DATA

def count_state_cases():
    request_url = 'https://covidtracking.com/api/v1/states/current.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    virus_data = requests.get(request_url, headers = headers)
    ordered_cases = []
    for state in virus_data:
        ordered_cases.append(state)
    return sorted(ordered_cases, key = lambda x: x[1], reverse=True)

def cases_per_pop():
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