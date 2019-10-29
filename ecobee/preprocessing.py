#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: guilherme
"""

# macro names
dayName   = 'Day'
yearName  = 'Year'
monthName = 'Month'
nonCday   = 'Days in Order'

dateName  = 'DateTime'
tonName   = 'Time on (min)'
sysMName  = 'HvacMode'
timeName  = 'Time'

hName     = 'Humidity'
hout      = 'RH_out'
ctName    = 'Thermostat_Temperature'
tName     = 'T_out'

hmaxName  = 'Max Indoor Humidity (%RH)'
ctmaxNam  = 'Max Indoor Temp (C)'
tmaxName  = 'Max Outdoor Temp (C)'
houtMax   = 'Max Outdoor Humidity (%RH)'

hminName  = 'Min Indoor Humidity (%RH)'
ctminNam  = 'Min Indoor Temp (C)'
tminName  = 'Min Outdoor Temp (C)'
houtMin   = 'Min Outdoor Humidity (%RH)'

hmeanName = 'Mean Indoor Hum (%RH)'
ctmnName  = 'Mean Indoor Temp (C)'
tmeanName = 'Mean Outdoor Temp (C)'
houtMean  = 'Mean Outdoor Hum (%RH)'

stdTemp   = 'Outdoor Temp Standard Deviation (C)'
stdHum    = 'Indoor Humidity Standard Deviation (%RH)'
stdCT     = 'Indoor Temp Standard Deviation (C)'
stdHout   = 'Outdoor Humidity Standard Deviation (%RH)'

eventName = 'Event'

def ecobeeDataFrame(path):
    '''
    Description: It creates a data frame from a ecobee report csv table and includes new columns as the following:
        dayName             = 'Day'
        yearName            = 'Year'
        monthName           = 'Month'
        nonChronologicalDay = 'Days in Order'    
    Input:
        path: The path of the report file.
        
    Output:
        A pandas data frame.
    '''
    import pandas as pd
    import numpy as np
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
    data = [line.split(',') for line in data[1:]]
    df = pd.DataFrame(data, columns=columns)
    
    df.rename(columns={'RH_out\n':'RH_out'}, inplace=True)
    
    #split datetime into date and time columns
    datetime = np.asarray([d.split(' ') for d in df[dateName]], dtype='str')
    df[dateName] = datetime[:,0]
    df[timeName] = datetime[:,1]
    
    # get year month and day from Date
    date = np.asarray([d.split('-') for d in df[dateName]], dtype='uint16')
    
    # create new coluns
    df[yearName]  = date[:,0]
    df[monthName] = date[:,1]
    df[dayName]   = date[:,2]
    df[nonCday] = 0
    
    # cast these columns from str to numeric
    df[tName]  = pd.to_numeric(df[tName], errors='coerce')
    df[hName]  = pd.to_numeric(df[hName], errors='coerce')
    df[ctName] = pd.to_numeric(df[ctName], errors='coerce')
    df[hout]   = pd.to_numeric(df[hout], errors='coerce')
    
    # get Julian Day
    for date in df[dateName].unique():
        d = dt.datetime.strptime(date, "%Y-%m-%d") # get datetime object
        df.loc[ (df[yearName] == d.year) & (df[monthName] == d.month) & (df[dayName] == d.day), nonCday] = dt.date(d.year,d.month,d.day).toordinal()
    
    return df

def appendNewData(dest, path):
    '''
    Description:
        It receives a ecobee data frame as input append 
        a new data set to it and return it.
    Input:
        datframe: An ecobee data frame.
    Output:
        It returns a new data frame with the new ecobee data set appended to dest.
    '''
    
    new = ecobeeDataFrame(path)
    return dest.append(new, ignore_index=True, sort=True)

def getMxMn(dataframe, column):
    '''
    Description:
        It receives a ecobee data frame as input and compute max and min value 
        of the specified column passed for each day. It returns a list with the 
        values for each day.
    Input:
        datframe: An ecobee data frame.
        
        column: The name of the column of interest.
    Output:
        A sorted list with list containing max and min value for each day. 
        As the following example:
            
        returning list := [[max1,min1], [max2,min2], ...,[maxN,minN]]
    '''
    import numpy as np
    
    df = dataframe.copy()
    
    mxmn_list = list()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day] 
        mxmn_list.append([np.max(d[column]), np.min(d[column])])
    return mxmn_list

def getMean(dataframe, column):
    '''
    Description:
        It receives a ecobee data frame as input and compute mean and standard 
        deviation of the specified column passed for each day. It returns a list 
        with the values for each day.
    Input:
        datframe: An ecobee data frame.
        
        column: The name of the column of interest.
    Output:
        A sorted list with list containing mean and stddev for each day. 
        As the following example:
            
        returning list := [[mean1,stddev1], [mean2,stddev2], ...,[meanN,stddevN]]
    '''
    import numpy as np
    
    df = dataframe.copy()
    
    mean_list = list()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        mean_list.append([round(np.mean(d[column]), 2), round(np.std(d[column]), 2)])
    return mean_list

def getTimeOn(dataframe):
    '''
    Description:
        It receives a ecobee data frame as input and compute how much time the device 
        that controls temperature was left on. It returns a list with the values for 
        each day.
    Input:
        An ecobee data frame.
    Output:
        A sorted list with each time that the device was left on mode on for each day.
    '''
    
    df = dataframe.copy()
    
    count_list = list()
    for day in df[nonCday].unique():
        d = df[df[nonCday] == day]
        modes = d[sysMName].values
        clock = d[timeName].values
        clock = [x.split(':') for x in clock]
        
        count = 0
        i = 0
        while i < len(modes):
            if modes[i]!= "off":
                b = int(clock[i][0])*60 + int(clock[i][1])
                i+=1
                while i < len(modes) and modes[i]!= "off":
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
    '''
    Description:
        It receives a ecobee data frame as input and compute some data as mean, 
        max and min from Outside and Inside measures. It returns a new data frame
        with these values.
    Input:
        An ecobee data frame.
    Output:
        A simplified data frame containing mean, standard deviation, max, and
        min values from Inside and Outside Humidity and Temperature.
    '''
    import pandas as pd
    import numpy as np
    
    df = dataframe.copy()
    
    columns= [tName, ctName, hName, hout]
    
    meanv = list()
    mxmnv = list()
    for c in columns:
        meanv.append(np.asarray(getMean(df, c)))
        mxmnv.append(np.asarray(getMxMn(df, c)))
    
    tmOn = np.asarray([getTimeOn(df)])
    days = np.asarray([df[nonCday].unique()])
    
    meanv = np.concatenate((meanv[:]), axis=1)
    mxmnv = np.concatenate((mxmnv[:]), axis=1)
    
    values = np.concatenate((days.T,meanv,mxmnv,tmOn.T), axis=1)
    
    
    cln_columns = [nonCday, 
                  tmeanName, stdTemp,
                  ctmnName, stdCT,
                  hmeanName, stdHum,
                  houtMean, stdHout,
                  tmaxName, tminName,
                  ctmaxNam, ctminNam,
                  hmaxName, hminName,
                  houtMax, houtMin,
                  tonName]
    
    clean_df = pd.DataFrame(values, columns = cln_columns)
    
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
    import numpy as np
    
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
    '''
    Description:
        It receives a clean dataframe object and plot Inside temperature 
        and Outside Temperature for each day of measurement.
    Input:
        A clean data frame of the same type of the returning data frame of the funtion ecobee.preprocessing.cleanData().
    '''
    import matplotlib.pyplot as plt
    import pylab as pl
    import numpy as np
    
    # get values
    x, y, t = dataframe[tmeanName].values, dataframe[ctmnName].values, dataframe[nonCday].values
    
    # remove nan from x and y
    fltr = ~np.isnan(x)
    x, y, t = x[fltr], y[fltr], t[fltr]
    fltr = ~np.isnan(y)
    x, y, t = x[fltr], y[fltr], t[fltr]
    
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
    
    ax.plot(t, x, 'darkblue', linestyle='--', label = 'Outside Temperature', marker='o')
    ax.plot(t, y, 'lime', linestyle='--', label = 'Inside Temperature' , marker='o')
    pl.legend(loc='lower right')
    plt.show()  
    
def animated_plot(dataframe, fileName, columns=[tName,ctName,timeName], nFrames = 300, 
                 nfps = 30, nInterval = 500, step = 10, legend = "", ylabel = "", 
                 xlabel= "", tlabel = "", measlabel = "", title = ""):
    
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import pylab as pl
    import numpy as np
    
    # get values
    x, y, t = dataframe[columns[0]].values, dataframe[columns[1]].values, dataframe[columns[2]].values
    
    # remove nan from x and y
    fltr = ~np.isnan(x)
    x, y, t = x[fltr], y[fltr], t[fltr]
    fltr = ~np.isnan(y)
    x, y, t = x[fltr], y[fltr], t[fltr]
    
    if 'Time' in columns[2]:
        t = t - t.min()
    
    fig = plt.figure(figsize = (24,16))
    ax = fig.add_subplot(1, 1, 1)
    
    ax.set_xlabel(tlabel)
    ax.set_ylabel(measlabel)
    
    k = x[:step]
    k[0], k[-1] = x.max(), x.min()
    
    l = y[:step]
    l[0], l[-1] = y.max(), y.min()
    
    line = list()
    ax1, = ax.plot(t[:step], k, 'darkblue', label = xlabel)
    ax2, = ax.plot(t[:step], l, 'lime', label = ylabel)
    line.append(ax1)
    line.append(ax2)
    pl.legend(loc='lower right')
    pl.title(title)
    
    def init():  # only required for blitting to give a clean slate.
        line[0].set_ydata([np.nan]*step)
        line[1].set_ydata([np.nan]*step)
        return line
    
    def animate(i):
        if len(x[i: i+ step]) == step:
            line[0].set_ydata(x[i:i + step])
            line[1].set_ydata(y[i:i + step])
        return line
        
    ani = animation.FuncAnimation(
        fig, animate, init_func=init, interval=nInterval, blit=True, save_count=50, frames=nFrames)
    
    ani.save(fileName, fps=nfps, extra_args=['-vcodec', 'libx264'])
    
    plt.show()
    
def animated_plot_static(dataframe, fileName, columns=[tName,ctName,timeName], nFrames = 300, 
                         nfps = 30, nInterval = 500, step = 10, legend = "", ylabel = "", 
                         xlabel= "", tlabel = "", measlabel = "", title = ""):
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import pylab as pl
    import numpy as np

    # get values
    x, y, t = dataframe[columns[0]].values, dataframe[columns[1]].values, dataframe[columns[2]].values

    # remove nan from x and y
    fltr = ~np.isnan(x)
    x, y, t = x[fltr], y[fltr], t[fltr]
    fltr = ~np.isnan(y)
    x, y, t = x[fltr], y[fltr], t[fltr]

    fig = plt.figure(figsize = (24,16))
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlabel(tlabel)
    ax.set_ylabel(measlabel)

    line = list()
    ax1, = ax.plot(t, x, 'darkblue', label = xlabel)
    ax2, = ax.plot(t, y, 'lime', label = ylabel)
    line.append(ax1)
    line.append(ax2)
    pl.legend(loc='lower right')
    pl.title(title)

    def init():  # only required for blitting to give a clean slate.
        line[0].set_data([], [])
        line[1].set_data([], [])
        return line

    def animate(i):
        line[0].set_data(t[:i*step], x[:i*step])
        line[1].set_data(t[:i*step], y[:i*step])
        return line

    ani = animation.FuncAnimation(
        fig, animate, init_func=init, interval=nInterval, blit=True, save_count=50, frames=nFrames)

    ani.save(fileName, fps=nfps, extra_args=['-vcodec', 'libx264'])

    plt.show() 