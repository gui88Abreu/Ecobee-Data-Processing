#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: Guilherme de Brito Abreu, undergraduate student at @unicamp.
"""

#importing libraries
import ecobee.preprocessing as pp
import ecobee.metadata as md

datasetPath = '../data_set/ecobee/'

metadata = md.metaData(datasetPath+"meta_data.csv")

# generate a data frame from the ecobee csv file
print('Generating Data Frame...')
ecobee = pp.ecobeeData(datasetPath+"2018/00994395a299fdb2f2377879bec134d0047f6267.csv")
print('Done!')

# select just the most important data e calculate important parameters like mean, max, and min temperatures
print('Cleaning Up the Data...')
ecobee.summarizeData()
print('Done')

ecobee.plot_TxD()

ecobee.plot_comparison(summ = True, ylabel = "Relative Humidity [%]", columns = [pp.meanOutHumCol, pp.meanInHumCol, pp.julianDayCol])
