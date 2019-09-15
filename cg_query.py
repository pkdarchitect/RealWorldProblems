#!/usr/bin/python
# Copyright PKD, all rights reserved.

import json,urllib
import time
import pandas as pd
from BeautifulSoup import BeautifulSoup

sender = "changethis@gmail.com"
recipients = "changethisalso@gmail.com"

cg_data = urllib.urlopen("http://sfbay.craigslist.org/search/cto?maxAsk=10000&autoMinYear=2016&autoMilesMax=90000&auto_title_status=1")

html =  cg_data.read()

soup = BeautifulSoup(html)

#print soup.title

#divs = soup.findAll('div')
cars = soup.findAll('p', attrs={'class': 'row'})

#print(len(cars))

#this_car = cars[15]

findcars = []
for this_car in cars:
    #print(this_car.prettify())

    this_time = this_car.find('time')['datetime']
    this_time = pd.to_datetime(this_time)
    this_price = (this_car.find('span', {'class': 'price'}).text)
    this_title = this_car.find('a', attrs={'class': 'hdrlnk'}).text

    #print('  '.join([str(i) for i in [this_time, this_title, this_price]]))
    tempstr = '  '.join([str(i) for i in [this_title, this_price]])
    findcars.append(tempstr)

hondaindices = [i for i, x in enumerate(findcars) if "Honda" in x]
nissanindices = [i for i, x in enumerate(findcars) if "Nissan" in x]

print hondaindices
print nissanindices

outside_hondas = [findcars[i] for i in hondaindices]
outside_nissans = [findcars[i] for i in nissanindices]

print outside_hondas
print outside_nissans

findnewcars = []
while(True):
    del findnewcars[:]

    cg_data = urllib.urlopen("http://sfbay.craigslist.org/search/cto?maxAsk=10000&autoMinYear=2006&autoMilesMax=90000&auto_title_status=1")
    html =  cg_data.read()

    soup = BeautifulSoup(html)
    cars = soup.findAll('p', attrs={'class': 'row'})

    for this_car in cars:
        this_price = (this_car.find('span', {'class': 'price'}).text)
        this_title = this_car.find('a', attrs={'class': 'hdrlnk'}).text
        tempstr = '  '.join([str(i) for i in [this_title, this_price]])
        findnewcars.append(tempstr)

    hondaindices = [i for i, x in enumerate(findnewcars) if "Honda" in x]
    nissanindices = [i for i, x in enumerate(findnewcars) if "Nissan" in x]
    inside_hondas = [findnewcars[i] for i in hondaindices]
    inside_nissans = [findnewcars[i] for i in nissanindices]

    check_hondas = (outside_hondas == inside_hondas)
    #print check_hondas
    if check_hondas is False:
        print "A new honda is available"
        outside_hondas = inside_hondas

    check_nissans = (outside_nissans == inside_nissans)
    #print check_nissans
    if check_nissans is False:
        print "A new nissans is available"
        outside_nissans = inside_nissans
    print("Starting again\n")
    time.sleep(300)
