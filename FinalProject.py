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
    population_req = requests.get(request_url_pop, headers = headers)
    pop_data = (population_req.content.decode())
    population_data = json.loads(pop_data)    
    return(population_data)
    
def get_social_data():
    url = ('https://gs.statcounter.com/social-media-stats/all/united-states-of-america/#daily-20200101-20200409')
    titles = {'user-agent':'This is user agent'}
    x = requests.get(url, headers = titles)
    soup = bs4.BeautifulSoup(x.text, features='lxml')
    
    all_urls = soup
    new_urls = all_urls.find(class_ = 'raphael-group-11-hot')
    return(new_urls)

def get_daily_virus():
    request_url_virus_pos = 'https://covidtracking.com/api/us/daily'
    request_data_pos = requests.get(request_url_virus_pos)
    return (request_data_pos.json())
#0528NATJUS

def get_world_info():
    world_url = 'https://api.thevirustracker.com/free-api?countryTotals=ALL'
    world_req = requests.get(world_url)
    return(world_req.json())


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


cur.execute('CREATE TABLE IF NOT EXISTS SOCIAL (state TEXT, total INTEGER)')

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

cur.execute('CREATE TABLE IF NOT EXISTS TOTAL_DAILY (date INTEGER, positive INTEGER)')
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


def calculations(cur, conn, filename):
    total_pop = 0
    cur.execute("SELECT population FROM POPULATIONS")
    for x in cur:
        total_pop = total_pop + int(x[0])
    
    total_virus = 0
    cur.execute("SELECT total FROM TOTAL_VIRUSES")
    for x in cur:
        total_virus = total_virus + int(x[0])
    
    cases_per = (total_virus/total_pop)
    cases_per_capita = ((cases_per*100000))

    full_path = os.path.join(os.path.dirname(__file__), filename)
    file_obj = open(full_path, 'w')
    file_obj.write('Calculations'+'\n')
    file_obj.write('First, we calculated the amount of positive cases per 100,000 for the United States. To do this, we added the total cases from each state and divided that by the total population of all states. Then we multiplied that total by 100,000: ')
    file_obj.write(str(cases_per_capita) + '\n')
    file_obj.close()

def virus_dictionary():
    try:
        conn = sqlite3.connect('finalproject.sqlite')
    except:
        print("Error")
    virus_dictionary = {}
    cur = conn.cursor()
    cur.execute("SELECT state, total FROM TOTAL_VIRUSES ")
    all_ = cur.fetchall()
    for x in all_:
        if x[0] not in virus_dictionary:
            virus_dictionary[x[0]] = x[1]
        else:
            pass
    conn.commit()
    return dict(virus_dictionary)


def visual_state_virus(virus_dictionary):
    final_list = []
    for x in virus_dictionary.keys():
        final_list.append(tuple([x,virus_dictionary[x]]))
    sorted_final_list = sorted(final_list, key = lambda x: x[0])
    names = []
    totals = []
    for x in sorted_final_list:
        names.append(x[0])
        totals.append(x[1])
    plt.bar(names, totals, color = ('yellow'), edgecolor = 'orange')
    plt.xlabel('State Name', fontsize=20)
    plt.ylabel('Positive Virus Cases', fontsize=20)
    plt.title('Positive Virus Cases Per State')
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.show()
    return sorted_final_list


def visualize_past_50():
    pass


def commit():
    conn.commit()

def main():
    counter()

    json_data = get_state_virus_data()
    total_virus_table(json_data)

    state_pop = get_state_populations()
    state_data = state_pop["data"]
    population_table(state_data)

    get_world_info()

    daily_data = get_daily_virus()
    total_daily_table(daily_data)

    
    calculations(cur, conn, 'Calculations.txt')

    world_stuff = get_world_info()
    world_data = world_stuff["countryitems"]
    world_table(world_data)

    commit()


if __name__ == "__main__":
    main()