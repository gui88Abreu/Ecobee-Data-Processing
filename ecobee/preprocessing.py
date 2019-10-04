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
    Description: It creates a data frame from a ecobee report csv table and includes new columns as the following:
        dayName             = 'Day'
        yearName            = 'Year'
        monthName           = 'Month'
        nonChronologicalDay = 'Non-chronological day'
        maxTemperatureName  = 'Max Temperature'
        minTemperatureName  = 'Min Temperature'
    
    Input:
        path: The path of the report file.
        
    Output:
        A pandas data frame.
    '''

    # column names
    dayName   = 'Day'
    yearName  = 'Year'
    monthName = 'Month'
    nonCday   = 'Julian day'
    tName     = 'Outdoor Temp (C)'
    tmaxName  = 'Max Temperature'
    tminName  = 'Min Temperature'
    dateName  = 'Date'
    
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
        if d.year%4:
            df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = dt.date(1,d.month,d.day).toordinal()
        elif d.month > 2:
            df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = dt.date(1,d.month,d.day).toordinal() + 1
        elif d.month == 2 and d.day == 29:
            df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = 60
        else:
            pass
        
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        df.loc[df[nonCday] == day,tmaxName] = np.max(d[tName])
        df.loc[df[nonCday] == day,tminName] = np.min(d[tName])
    
    return df

def appNewData(dest, path):
    new = ecobeeDataFrame(path)
    new['Julian day'] += dest['Julian day'].max()
    return dest.append(new, ignore_index=True)