#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: guilherme
"""

#importing libraries
import pandas as pd
import numpy as np

# macro names
dayName   = 'Day'
yearName  = 'Year'
monthName = 'Month'
nonCday   = 'Days in Order'
tName     = 'Outdoor Temp (C)'
tmaxName  = 'Max Temperature'
tminName  = 'Min Temperature'
dateName  = 'Date'

def ecobeeDataFrame(path):
    '''
    Description: It creates a data frame from a ecobee report csv table and includes new columns as the following:
        dayName             = 'Day'
        yearName            = 'Year'
        monthName           = 'Month'
        nonChronologicalDay = 'Days in Order'
        maxTemperatureName  = 'Max Temperature'
        minTemperatureName  = 'Min Temperature'
    
    Input:
        path: The path of the report file.
        
    Output:
        A pandas data frame.
    '''
    import datetime as dt
    
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
    date = np.asarray([d.split('-') for d in df[dateName]], dtype='uint16')
    
    df[tName] = pd.to_numeric(df[tName])
    
    # create new coluns
    df[yearName]  = date[:,0]
    df[monthName] = date[:,1]
    df[dayName]   = date[:,2]
    df[nonCday] = 0
    df[tmaxName] = np.nan
    df[tminName] = np.nan
    
    for date in df[dateName].unique():
        d = dt.datetime.strptime(date, "%Y-%m-%d") # get datetime object
        df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = dt.date(d.year,d.month,d.day).toordinal()
    
    return df

def appendNewData(dest, path):
    new = ecobeeDataFrame(path)
    return dest.append(new, ignore_index=True)

def getmxtmp(dataframe):
    df = dataframe.copy()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        df.loc[df[nonCday] == day,tmaxName] = np.max(d[tName])
        df.loc[df[nonCday] == day,tminName] = np.min(d[tName])
    return df