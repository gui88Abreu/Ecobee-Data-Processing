#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""

#importing libraries
import pandas as pd
import cm_library as cm
    
df_dict = dict()
for year in range(1997, 2019):
    
    print('processing data: ' + str(year)+'.xlsx'+' ...')
    
    try:
        dataset = pd.read_excel("../data_set/Dados_CEPAGRI/"+str(year)+".xlsx")
        if '^Unnamed' in dataset.columns:
            dataframe = dataset.loc[:, ~dataset.columns.str.contains('^Unnamed')]
        else:
            dataframe = dataset
        flag = '0 (not HW)/ 1 (HW)'
        hw_name='HeatWaves'
        year_col = dataset.columns[1]
        day_col = dataset.columns[2]
        mean_tmp_col = dataset.columns[12]
        max_tmp_col = None
        min_tmp_col = None
        
        # Identify what type of data dataset is
        if dataframe[dataframe.columns[0]].any() == 222 or dataframe[dataframe.columns[0]].any() == 265:
            year_col = dataset.columns[1]
            day_col = dataset.columns[2]
            mean_tmp_col = None
            max_tmp_col = dataset.columns[12]
            min_tmp_col = dataset.columns[14]
        
        fv = cm.get_heatwave(data=dataframe, flag=flag, hw_name=hw_name, day_name = day_col, year_name = year_col,
                             mean_tmp_name = mean_tmp_col, max_tmp_name=max_tmp_col, min_tmp_name=min_tmp_col)
        main_col = [dataframe.columns[1],dataframe.columns[2],dataframe.columns[12],flag,hw_name, 'p90_max', 'p90_min']
        res_df = fv[main_col]
        
        df_dict[str(year)] = res_df
        
        print('data: ' + str(year)+'.xlsx'+' was processed.')
    except:
        print('Something went wrong with this file: '+str(year)+'.xlsx')
        
for year in df_dict:
    df_dict[year].to_excel("hw_"+year+".xlsx")