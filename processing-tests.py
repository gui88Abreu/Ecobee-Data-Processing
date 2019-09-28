#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""

#importing libraries
import climate.heatwaveFinder as hwf
import ecobee.preprocessing as pp
    
df_dict = dict()
for year in range(1997, 2019):
    
    print('processing data: ' + str(year)+'.xlsx'+' ...')
    
    try:
        path = '../data_set/ecobee/House 1/Temperature/1.csv'
        df = pp.ecobeeDataFrame(path)
        flag = '0 (not HW)/ 1 (HW)'
        hw_name='HeatWaves'
        year_col = 'Year'
        day_col = 'Non-chronological day'
        mean_tmp_col = 'Outdoor Temp (C)'
        
        fv = hwf.get_heatwave(data=df, 
                              flag=flag, 
                              hw_name=hw_name, 
                              day_name = day_col, 
                              year_name = year_col,
                              mean_tmp_name = mean_tmp_col)
        
        main_col = ['Year','Day',mean_tmp_col,flag,hw_name, 'p90_max', 'p90_min']
        res_df = fv[main_col]
        
        df_dict[str(year)] = res_df
        
        print('data: ' + str(year)+'.xlsx'+' was processed.')
    except:
        print('Something went wrong with this file: '+str(year)+'.xlsx')
        
for year in df_dict:
    df_dict[year].to_excel("hw_"+year+".xlsx")