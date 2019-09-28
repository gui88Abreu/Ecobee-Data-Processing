#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: guilherme
"""

#importing libraries
import pandas as pd
import numpy as np

def ecobeeDataFrame(path):
    '''
    Description: It creates a data frame from a ecobee report csv table and includes 4 new columns with names 'Year', 'Month', 'Day' and 'Non-chronological day'.
    
    Input:
        path: The path of the report file.
        
    Output:
        It returns a pandas data frame.
    '''

    # just open file and read the data
    file = open(path, 'r')
    data = file.readlines()
    file.close()
    
    # clean up the data removing empty rows and commentaries
    i = 0;
    while i < len(data):
        if '#' in data[i] or '\n' == data[i] or '' == data[i]:
            data.pop(i)
        else:
            i+=1
    
    # find the date of each row
    columns = data[0].split(',')
    data = [line.split(',')[:-1] for line in data[1:]]
    df = pd.DataFrame(data, columns=columns)
    date = np.asarray([d.split('-') for d in df['Date']], dtype='uint16')
    
    df['Outdoor Temp (C)'] = pd.to_numeric(df['Outdoor Temp (C)'])
    
    # create new coluns
    df['Year']  = date[:,0]
    df['Month'] = date[:,1]
    df['Day']   = date[:,2]
    
    i = 1
    df['Non-chronological day'] = 0
    for date in df['Date'].unique():
        df.loc[ df['Date'] == date ,'Non-chronological day'] = i
        i += 1
    return df