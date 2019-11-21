#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:35:15 2019

@author: guilherme
"""
import pandas as pd
import urllib2

metaData = pd.read_csv("stations_inventory.csv")
quebecStations = metaData[metaData["Province"] == "QUEBEC"]
IDs = quebecStations["Station ID"].values

station = list()

for ID in IDs:
    data = pd.DataFrame([])
    for intYr in range(2015,2018+1):
        for intMnt in range(1,12+1):
            #build the query
            strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) +'&Month=' + str(intMnt) + "&timeframe=1&submit=Download+Data"  
            #print strQry
            print 'Querying station ' + str(ID) + ' for year ' + str(intYr) + ' and month ' + str(intMnt)
            try:
                response = urllib2.urlopen(strQry)
                rawData = response.readlines()
                rawData = [line.replace('"','').replace('\n','') for line in rawData]
                columns = rawData[0].split(',')
                d = [line.split(',') for line in rawData[1:]]
                
                for i in range(len(d)):
                    if len(d[i]) > len(columns):
                        d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                        d[i] = d[i][:len(columns)]
                        
                    if len(d[i]) < len(columns):
                        while len(d[i]) < len(columns):
                            d[i].append('')
                        
                newData = pd.DataFrame(d, columns=columns)
                data = data.append(newData, ignore_index=True, sort=True)
            except Exception, e:
                print 'Failure getting data for '  + str(ID) + ' for year ' + str(intYr)
    station.append(data)