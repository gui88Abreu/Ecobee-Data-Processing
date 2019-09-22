#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:57:37 2019

@author: guilherme
"""


#importing libraries
import pandas as pd
import sys, os
chpath = os.path.abspath('../climate_health')
if chpath not in sys.path:
    sys.path.append(chpath)
import climate as ch

dataset = pd.read_excel("../data_set/Dados_CEPAGRI/1997.xlsx")
dataframe = dataset.loc[:, ~dataset.columns.str.contains('^Unnamed')]
flag = '0/1 - not HW/ HW'
hw_name='HeatWaves'

fv = ch.get_heatwave(data=dataframe, flag=flag, hw_name=hw_name, day_name = dataset.columns[2], year_name = dataset.columns[1],
                     mean_tem_name = dataset.columns[12])
main_col = [dataframe.columns[1],dataframe.columns[2],dataframe.columns[12],flag,hw_name, 'Percentil 90']
res_df = fv[main_col]