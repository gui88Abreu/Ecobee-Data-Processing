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

dateName  = 'Date'
tonName   = 'Time on (min)'
sysMName  = 'System Mode'

hName     = 'Current Humidity (%RH)'
ctName    = 'Current Temp (C)'
tName     = 'Outdoor Temp (C)'

hmaxName  = 'Max Inside Humidity (%RH)'
ctmaxNam  = 'Max Inside Temp (C)'
tmaxName  = 'Max Outside Temp (C)'

hminName  = 'Min inside Humidity (%RH)'
ctminNam  = 'Min Inside Temp (C)'
tminName  = 'Min Outside Temp (C)'

hmeanName = 'Mean Inside Hum (%RH)'
ctmnName  = 'Mean Inside Temp (C)'
tmeanName = 'Mean Outside Temp (C)'

stdTemp   = 'Outside Temp Standard Deviation'
stdHum    = 'Inside Humidity Standard Deviation'
stdCT     = 'Inside Temp Standard Deviation'

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
    df[hName] = pd.to_numeric(df[hName])
    df[ctName] = pd.to_numeric(df[ctName])
    
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

def getMxMn(dataframe, column):
    df = dataframe.copy()
    
    mxmn_list = list()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day] 
        mxmn_list.append([np.max(d[column]), np.min(d[column])])
    return mxmn_list

def getMean(dataframe, column, stdCol):
    df = dataframe.copy()
    
    mean_list = list()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        mean_list.append([round(np.mean(d[column]), 2), round(np.std(d[column]), 2)])
    return mean_list

def getTimeOn(dataframe):
    df = dataframe.copy()
    
    count_list = list()
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
        
        count_list.append(count)
    return count_list

def cleanData(dataframe):
    df = dataframe.copy()
    
    columns= [[tName, stdTemp], [hName, stdHum], [ctName, stdCT]]
    
    meanv = list()
    mxmnv = list()
    for c in columns:
        meanv.append(np.asarray(getMean(df, c[0], c[1])))
        mxmnv.append(np.asarray(getMxMn(df, c[0])))
    
    tmOn = np.asarray([getTimeOn(df)])
    days = np.asarray([df[nonCday].unique()])
    
    meanv = np.concatenate((meanv[:]), axis=1)
    mxmnv = np.concatenate((mxmnv[:]), axis=1)
    
    values = np.concatenate((days.T,meanv,mxmnv,tmOn.T), axis=1)
    
    clean_df = pd.DataFrame(values, columns = [nonCday, tmeanName, stdTemp, hmeanName, stdHum, ctmnName, stdCT, 
                                     tmaxName, tminName, hmaxName, hminName, ctmaxNam, ctminNam, tonName])
    
    return clean_df

def plot_TxD(dataframe):
    '''
    Description:
        It receives a clean dataframe object and plot the relation between the temperature bands
        and the mean time that the user let the device on. Each band has a width of 5 Celsius degrees.
    Input:
        A clean data frame of the same type of the returning data frame of the funtion cleanData().
    '''
    import matplotlib.pyplot as plt
    
    cln_df = dataframe.copy()
    
    # get boundaries and bands
    min_t = cln_df[tmeanName].min()
    max_t = cln_df[tmeanName].max()
    temp = np.arange(min_t+5,max_t+5,5)
    mean = []
    std = []
    
    # get mean time on and the respectives standard deviations
    for t in temp:
        f = cln_df.loc[(cln_df[tmeanName] < t) & (cln_df[tmeanName] > t - 5), tonName]
        mean.append(f.sum()/f.size)
        std.append(np.std(f))
            
    x = temp
    y = mean
    e = std
    
    fig = plt.figure(figsize = (16,12))
    ax = fig.add_subplot(1, 1, 1)
    
    ax.set_xlabel('Mean Temperature Band (C)')
    ax.set_ylabel('Device On Mean Time (min/day)')
    
    # Major ticks every 20, minor ticks every 1
    major_ticks = np.arange(0, int(np.max(y))+int(np.max(e) + 50 ), 20)
    minor_ticks = np.arange(int(min_t)-5, int(max_t)+5, 1)
    
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks, minor=True)
    
    ax.grid(which='minor', alpha=1)
    ax.grid(which='major', alpha=0.5)
    
    plt.errorbar(x, y, yerr = e, ecolor = 'r', linestyle='None', marker='d')
    plt.show()
    
def plot_DayxTcTo(dataframe):
    import matplotlib.pyplot as plt
    import pylab as pl
    
    # get values
    x, y, t = dataframe[tmeanName].values, dataframe[ctmnName].values, dataframe[nonCday].values
    
    # remove nan from x and y
    x, y, t = x[~np.isnan(x)], y[~np.isnan(x)], t[~np.isnan(x)]
    x, y, t = x[~np.isnan(y)], y[~np.isnan(y)], t[~np.isnan(y)]
    
    fig = plt.figure(figsize = (16,12))
    ax = fig.add_subplot(1, 1, 1)
    
    ax.set_xlabel('day')
    ax.set_ylabel('Temperature (C)')
    
    # Major ticks every 20, minor ticks every 1
    major_ticks = np.arange(-20, 40, 1)
    minor_ticks = np.arange(0, t[-1]+5, 5)
    
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks, minor=True)
    
    ax.grid(which='both')
    
    ax.plot(t, x, 'r', linestyle=':', label = 'Outside Temperature', marker='o')
    ax.plot(t, y, 'b', linestyle=':', label = 'Inside Temperature' , marker='o')
    pl.legend(loc='lower right')
    plt.show()