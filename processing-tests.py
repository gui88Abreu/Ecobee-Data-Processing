#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""
#importing libraries
import climate.heatwaveFinder as hwf
import ecobee.preprocessing as pp

flag     = '0 (not HW)/ 1 (HW)'
hw_name  = 'HeatWaves'
year_col = 'Year'
day_col  = 'Days in Order'
temp_col = 'Max Temperature'
tt_temp  = 'Outdoor Temp (C)'

print('Generating Data Frame...')
for i in range(1,7):

    try:
        path = '../data_set/ecobee/House1/'+str(i)+'.csv'
        if i == 1:
            df = pp.ecobeeDataFrame(path)
        else:
            df = pp.appendNewData(df,path)
    except:
        print('Something went wrong with this file: '+str(i)+'.csv')
df[day_col] -= df[day_col].min() - 1
df = pp.getmxtmp(df)
print('Done!')

print('Finding Heatwaves...')
fv = hwf.get_heatwave(data=df, 
                      flag=flag, 
                      hw_name=hw_name, 
                      day_name = day_col, 
                      year_name = year_col,
                      max_tmp_name = temp_col)
print('Done!')

res_df = fv[[day_col,temp_col,hw_name,'p90_max']]
print('Heatwaves encountered: ', res_df[hw_name].max())