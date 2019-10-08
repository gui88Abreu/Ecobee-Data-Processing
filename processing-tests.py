#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""

#importing libraries
import ecobee.preprocessing as pp

'''
import numpy as np
import matplotlib.pyplot as plt
'''


flag     = '0 (not HW)/ 1 (HW)'
hw_name  = 'HeatWaves'
year_col = 'Year'
day_col  = 'Days in Order'
temp_col = 'Max Temperature'
tt_temp  = 'Outdoor Temp (C)'

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
df[day_col] -= df[day_col].min() - 1
print('Done!')


print('Cleaning Up the Data...')
cln_df = pp.cleanData(df)
print('Done')
