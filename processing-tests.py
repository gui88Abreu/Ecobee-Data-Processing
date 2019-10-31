#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: Guilherme de Brito Abreu, undergraduate student at @unicamp.
"""

datasetPath = '../data_set/ecobee/'
account     = 'g173691@dac.unicamp.br'


#importing libraries
import ecobee.preprocessing as pp
import ecobee.metadata as md
import numpy as np

import os

os.chdir(datasetPath)
metadata = md.metaData("meta_data.csv")

os.system('gcloud auth login '+ account)

x = metadata.data[metadata.data[md.frstCnctCol] == '00:00.0']
file = (x[md.dataIdCol].values)[0] + '.csv'
del x

for year in np.arange(2015,2020,1).astype('str'):
    os.system('gsutil cp gs://donate_your_data_2019/files/'+year+'/'+file+'.zip '+year)
    os.system('unzip '+year+'/'+file+'.zip -d ' + year)

ecobee = pp.ecobeeData()

# generate a data frame from the ecobee csv file
print('Generating Data Frame...')
for year in np.arange(2015,2020,1).astype('str'):
    ecobee.appendNewData(year+'/'+file)
print('Done!')

# select just the most important data e calculate important parameters like mean, max, and min temperatures
print('Summerizing Data...')
ecobee.summarizeData()
print('Done')

ecobee.plot_TxD()

ecobee.plot_comparison(summ = True, 
                       ylabel = "Relative Humidity [%]", 
                       columns = [pp.meanOutHumCol, pp.meanInHumCol, pp.julianDayCol])
