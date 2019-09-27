#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: guilherme
"""

#importing libraries
import pandas as pd
import numpy as np

file = open("../data_set/ecobee/Plinio's Dataset - December 2016 to August 10 2018/"+
                        "House 1 - Iron Gate/Temperature/report-311001483636-2016-12-01-to-2016-12-31.csv", 'r')
data = file.readlines()
file.close()

i = 0;
while i < len(data):
    if '#' in data[i] or '\n' == data[i] or '' == data[i]:
        data.pop(i)
    else:
        i+=1
        
file = open("../data_set/ecobee/Plinio's Dataset - December 2016 to August 10 2018/"+
                        "House 1 - Iron Gate/Temperature/report-2016-12-01-to-2016-12-31.csv", 'w')

columns = data[0].split(',')

for line in data:
    file.write(line)
file.close()

data = [line.split(',')[:-1] for line in data[1:]]

df = pd.DataFrame(data, columns=columns)


date = np.asarray([d.split('-') for d in df['Date']])
  
df['Year'] = date[:,0]
df['Month'] = date[:,1]
days = np.arange(1,len(date)+1)
df['Non-chronological day'] = days