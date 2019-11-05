#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: Guilherme de Brito Abreu, undergraduate student at @unicamp.
"""

datasetPath = '../data_set/ecobee/'
accountFile = 'account'
#importing libraries
import ecobee.preprocessing as pp
import ecobee.metadata as md
import numpy as np

import os

os.chdir(datasetPath)
metadata = md.metaData("meta_data.csv")

x = metadata.data[metadata.data[md.frstCnctCol] == '00:00.0']
device = (x[md.dataIdCol].values)[-1] 
file =  device + '.csv'
del x

#download data from google cloud
os.system('gcloud auth login '+ ((os.popen("cat "+ accountFile)).read()).replace('\n',''))
for year in np.arange(2015,2020,1).astype('str'):
    os.system('gsutil cp gs://donate_your_data_2019/files/'+year+'/'+file+'.zip '+year)
    os.system('unzip '+year+'/'+file+'.zip -d ' + year)

# get the Data
ecobee = pp.ecobeeData()
# generate a data frame from the ecobee csv file
print('Generating Data Frame...')
for year in np.arange(2015,2020,1).astype('str'):
    ecobee.append(year+'/'+file)
print('Done!')

# select just the most important data e calculate important parameters like mean, max, and min temperatures
print('Summerizing Data...')
ecobee.summarizeData()
print('Done')

ecobee.plotTxD()
ecobee.plotComparison(summ = True, 
                    ylabel = "Air Mean Relative Humidity [%]", 
                    columns = [pp.meanOutHumCol, pp.meanInHumCol, pp.julianDayCol])

new_df = ecobee.data.copy()
new_df[pp.timeCol] = np.arange(5,new_df.shape[0]*5 + 1, 5)
ecobee.animatedPlotStatic(dataframe = new_df[(new_df[pp.julianDayCol] >= 4) & (new_df[pp.julianDayCol] <= 8)],
                        fileName   = 'tmp_animation.mp4',
                         columns   = [pp.outHumCol,pp.inHumCol, pp.timeCol], 
                         nFrames   = 1000,
                         nfps      = 60,
                         step      = 2,
                         nInterval = 500,
                         ylabel = "Humidity (%)",
                         xlabel    = "Time Diference (min)",
                         y1label    = "Outdoor Humidity",
                         y2label    = "Indoor Humidity",
                         title     = "Comparison Between Outdoor and Indoor Humidity")

deviceInfo = metadata.data.loc[metadata.data[md.dataIdCol] == device]
print(deviceInfo.iloc[0])