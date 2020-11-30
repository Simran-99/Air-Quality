# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:23:58 2020

@author: Home
"""

from Plots import avg2013,avg2014,avg2015
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

def met_data(m, y):
    
    file = open('Data/Html_Data/{}/{}.html'.format(y,m), 'rb')
    p_text = file.read()

    tempD = []
    finalD = []

    soup = BeautifulSoup(p_text, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                op = tr.get_text()
                tempD.append(op)

    rows = len(tempD) / 15

    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length - 1)
    finalD.pop(0)

    for op in range(len(finalD)):
        finalD[op].pop(6)
        finalD[op].pop(13)
        finalD[op].pop(12)
        finalD[op].pop(11)
        finalD[op].pop(10)
        finalD[op].pop(9)
        finalD[op].pop(0)

    return finalD

def combine(y, cs):
    for op in pd.read_csv('Data/Final_Data/real_' + str(y) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=op)
        my_list = df.values.tolist()
    return my_list


if __name__ == "__main__":
    if not os.path.exists("Data/Final_Data"):
        os.makedirs("Data/Final_Data")
    for y in range(2013, 2016):
        final_data = []
        with open('Data/Final_Data/real_' + str(y) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for m in range(1, 13):
            temp = met_data(m, y)
            final_data = final_data + temp
            
        pm = getattr(sys.modules[__name__], 'avg{}'.format(y))()

        if len(pm) == 364:
            pm.insert(364, '-')

        for i in range(len(final_data)-1):
            # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm[i])

        with open('Data/Final_Data/real_' + str(y) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    data_2013 = combine(2013, 600)
    data_2014 = combine(2014, 600)
    data_2015 = combine(2015, 600)
    
     
    total=data_2013+data_2014+data_2015
    
    with open('Data/Final_Data/Combined.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
dataset=pd.read_csv('Data/Final_Data/Combined.csv')
