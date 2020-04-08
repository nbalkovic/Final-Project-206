import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os

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


conn = sqlite3.connect('final.sqlite')
cur = conn.cursor()