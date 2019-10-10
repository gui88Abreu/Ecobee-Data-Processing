#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""

#importing libraries
import ecobee.preprocessing as pp

# generate a data frame from the ecobee csv file
print('Generating Data Frame...')
for i in range(1,11):

    try:
        path = '../data_set/ecobee/House1/'+str(i)+'.csv'
        if i == 1:
            df = pp.ecobeeDataFrame(path)
        else:
            df = pp.appendNewData(df,path)
    except:
        print('Something went wrong with this file: '+str(i)+'.csv')

# shift all days untill the first day be 1
df[pp.nonCday] -= df[pp.nonCday].min() - 1
print('Done!')

# select just the most important data e calculate important parameters like mean, max, and min temperatures
print('Cleaning Up the Data...')
cln_df = pp.cleanData(df)
print('Done')

print("Mean Temperature x Device On")
pp.plot_TxD(cln_df)