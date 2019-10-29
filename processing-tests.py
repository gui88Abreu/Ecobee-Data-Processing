#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: Guilherme de Brito Abreu, undergraduate student at @unicamp.
"""

#importing libraries
import ecobee.preprocessing as pp
import numpy as np

path = '/home/guilherme/Documents/GIT REPOSITORIES/data_set/ecobee/003ad187b773affeb756ebcdb56f14594b814509.csv'

df = pp.ecobeeDataFrame(path)


# generate a data frame from the ecobee csv file
print('Generating Data Frame...')
'''
for i in range(1,11):

    try:
        if i == 1:
            df = pp.ecobeeDataFrame(path+str(i)+'.csv')
        else:
            df = pp.appendNewData(df,path+str(i)+'.csv')
    except FileNotFoundError:
        quit('Something went wrong with this file! No such file or directory: '+path+str(i)+'.csv')
'''
# shift all days untill the first day be 1
df[pp.julianDayCol] -= df[pp.julianDayCol].min() - 1
print('Done!')

# select just the most important data e calculate important parameters like mean, max, and min temperatures
print('Cleaning Up the Data...')
cln_df = pp.summarizeData(df)
print('Done')

print("Mean Temperature x Device On")
pp.plot_TxD(cln_df)

pp.plot_comparison(cln_df, ylabel = "Relative Humidity [%]", columns = [pp.meanOutHumCol, pp.meanInHumCol, pp.julianDayCol])

'''
It creates a copý of the original dataframe in order to have another 
dataframe that contains time colummn as numbers other than strings.
It makes animated plot faster."
'''
new_df = df.copy()
new_df[pp.timeCol] = np.arange(5,new_df.shape[0]*5 + 1, 5)

pp.animated_plot(new_df[(new_df[pp.julianDayCol] >= 4) & (new_df[pp.julianDayCol] <= 8)],
                        fileName   = 'tmp_animation.mp4',
                         columns   = [pp.outTemCol,pp.inTemCol, pp.timeCol], 
                         nFrames   = 900, 
                         nInterval = 1000,
                         measlabel = "Temperature (C)",
                         tlabel    = "Time Diference (min)",
                         xlabel    = "Outdoor Temperature",
                         ylabel    = "Indoor Temperature",
                         title     = "Comparison Between Outdoor and Indoor Temperature")

pp.animated_plot_static(new_df[(new_df[pp.julianDayCol] >= 4) & (new_df[pp.julianDayCol] <= 8)],
                        fileName   = 'tmp_animation2.mp4',
                         columns   = [pp.outTemCol,pp.inTemCol, pp.timeCol], 
                         nFrames   = 900, 
                         nInterval = 500,
                         step      = 2,
                         measlabel = "Temperature (C)",
                         tlabel    = "Time (min)",
                         xlabel    = "Outdoor Temperature",
                         ylabel    = "Indoor Temperature",
                         title     = "Comparison Between Outdoor and Indoor Temperature")
