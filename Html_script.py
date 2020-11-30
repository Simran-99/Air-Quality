# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:14:50 2020

@author: Home
"""

import os
import time
import requests
import sys


def retrieve_data():
    for y in range(2013,2016):
        for m in range(1,13):
            if(m<10):
                url='http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(m
                                                                          ,y)
            else:
                url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(m
                                                                          ,y)
            texts=requests.get(url)
            text_utf=texts.text.encode('utf=8')
            
            if not os.path.exists("Data/Html_Data/{}".format(y)):
                os.makedirs("Data/Html_Data/{}".format(y))
            with open("Data/Html_Data/{}/{}.html".format(y,m),"wb") as output:
                output.write(text_utf)
            
        sys.stdout.flush()
        
if __name__=="__main__":
    start=time.time()
    retrieve_data()
    stop=time.time()
    print("Time taken {}".format(stop-start))
        