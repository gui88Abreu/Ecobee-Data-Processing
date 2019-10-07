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
tmeanName = 'Mean Temperature'
stdName   = 'Temperature Standard Deviation'
dateName  = 'Date'
tonName   = 'Time on (Min)'
sysMName  = 'System Mode'

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
    
    for date in df[dateName].unique():
        d = dt.datetime.strptime(date, "%Y-%m-%d") # get datetime object
        df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = dt.date(d.year,d.month,d.day).toordinal()
    
    return df

def appendNewData(dest, path):
    new = ecobeeDataFrame(path)
    return dest.append(new, ignore_index=True, sort=True)

def getmxtmp(dataframe):
    df = dataframe.copy()
    
    df[tmaxName] = np.nan
    df[tminName] = np.nan
    
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        df.loc[df[nonCday] == day,tmaxName] = np.max(d[tName])
        df.loc[df[nonCday] == day,tminName] = np.min(d[tName])
    return df

def getmeantmp(dataframe):
    df = dataframe.copy()
    
    df[tmeanName] = np.nan
    df[stdName] = np.nan
    
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        df.loc[df[nonCday] == day,stdName] = round(np.std(d[tName]), 2)
        df.loc[df[nonCday] == day,tmeanName] = np.mean(d[tName])
    return df

def gettimeon(dataframe):
    df = dataframe.copy()
    
    df[tonName] = np.nan
    
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        modes = d[sysMName].values
        clock = d['Time'].values
        clock = [x.split(':') for x in clock]
        
        count = 0
        i = 0
        while i < len(modes):
            if modes[i].endswith("On"):
                b = int(clock[i][0])*60 + int(clock[i][1])
                i+=1
                while i < len(modes) and modes[i].endswith("On"):
                    i+=1
                if i < len(modes):
                    a = int(clock[i][0])*60 + int(clock[i][1])
                else:
                    a = 1440
                    
                count += a - b
            i+=1
        
        df.loc[df[nonCday] == day,tonName] = count
    return df