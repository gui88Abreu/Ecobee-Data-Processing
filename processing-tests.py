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
day_col  = 'Julian day'
temp_col = 'Max Temperature'
tt_temp  = 'Outdoor Temp (C)'

print('Generating Data Frame...')
for i in range(1,7):

    try:
        path = '../data_set/ecobee/House 1/Temperature/'+str(i)+'.csv'
        if i == 1:
            df = pp.ecobeeDataFrame(path)
        else:
            df = pp.appNewData(df,path)
    except:
        print('Something went wrong with this file: '+str(i)+'.csv')
print('Done!')

print('Finding Heatwaves...')
fv = hwf.get_heatwave(data=df, 
                      flag=flag, 
                      hw_name=hw_name, 
                      day_name = day_col, 
                      year_name = year_col,
                      max_tmp_name = temp_col,
                      min_tmp_name = temp_col)
print('Done!')

res_df = fv[['Year','Julian day',tt_temp,temp_col,flag,hw_name, 'p90_max', 'p90_min']]
print('Heatwaves encountered: ', res_df[hw_name].max())