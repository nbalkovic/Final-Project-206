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

conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()

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
    data = cur.fetchall()
    for x in data:
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

def daily_dictionary():
    try:
        conn = sqlite3.connect('finalproject.sqlite')
    except:
        print("Error")
    daily_dictionary = {}
    cur = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT date, positive FROM JOIN_TABLE")
    data = cur.fetchall()
    for x in data:
        if x[0] not in daily_dictionary:
            daily_dictionary[x[0]] = x[1]
        else:
            pass
    conn.commit()
    return (dict(daily_dictionary))

def social_dictionary():
    try:
        conn = sqlite3.connect('finalproject.sqlite')
    except:
        print("Error")
    social_dictionary = {}
    cur = conn.cursor()
    cur.execute("SELECT date, twitter FROM JOIN_TABLE")
    data = cur.fetchall()
    for x in data:
        if x[0] not in social_dictionary:
            social_dictionary[x[0]] = x[1]
        else:
            pass
    conn.commit()
    return dict(social_dictionary)


def visualize_past_50(social_dictionary, daily_dictionary):
    
    new = []
    for x in social_dictionary.keys():
        new.append(tuple([x,social_dictionary[x]]))
    sorted_new = sorted(new, key = lambda x: x[0])
    date = []
    twitter = []
    for x in sorted_new:
        date.append(x[0])
        twitter.append(x[1])

    new2 = []
    for x_ in daily_dictionary.keys():
        new2.append(tuple([x_,daily_dictionary[x_]]))
    sorted_new2 = sorted(new2, key = lambda x_: x_[0])
    date_virus = []
    positive = []
    for x_ in sorted_new2:
        date_virus.append(x_[0])
        positive.append(x_[1])
    

    plt.subplot(2,1,1)
    plt.plot(date, twitter, 'o-')
    plt.title('Comparing trendlines')
    plt.ylabel('Twitter')
    plt.xticks(fontsize=4, rotation = 90)

    plt.subplot(2, 1, 2)
    plt.plot(date_virus, positive, '.-')
    plt.xlabel('Date')
    plt.ylabel('Virus')  
    plt.xticks(fontsize=4, rotation = 90)


    
    plt.show()


def commit():
    conn.commit()

def main():

    calculations(cur, conn, 'Calculations.txt')

    visual_state_virus(virus_dictionary())
    visualize_past_50(social_dictionary(), daily_dictionary())
    commit()


if __name__ == "__main__":
    main()