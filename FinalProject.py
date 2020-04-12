import matplotlib 
import matplotlib.pyplot as plt
import json
import requests
import sqlite3
import os
import tweepy as tw

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

def count_state_cases():
    request_url = 'https://covidtracking.com/api/v1/states/current.json'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    virus_data = requests.get(request_url, headers = headers)
    ordered_cases = []
    for state in virus_data:
        ordered_cases.append(state)
    return sorted(ordered_cases, key = lambda x: x[1], reverse=True)

def get_twitter_data():
    request_url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23superbowl&result_type=recent'
    r = api.requests('statuses/filter', {'track': '#covid19'})
    
    for item in r:
        count +=1
    
    return count

   url = self.base_url + f'/odata/Jobs({job_id})/UiPath.Server.Configuration.OData.StopJob'
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        payload = str({
                        "strategy": "Kill"
                      })
        r = requests.post(url, data=payload, headers=headers)


conn = sqlite3.connect('final.sqlite')
cur = conn.cursor()