#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:35:15 2019

@author: guilherme
"""
import pandas as pd
import urllib as url

metaData = pd.read_csv("../data_set/EnviromentCanada/stations_inventory.csv")
quebecStations = metaData[metaData["Province"] == "QUEBEC"]
IDs = quebecStations["Station ID"].unique()

station = list()

intYr = 2018

for ID in IDs:
    data = pd.DataFrame([])
    for intMnt in range(6,8+1):
        #build the query
        strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) +'&Month=' + str(intMnt) + "&timeframe=1&submit=Download+Data"  
        #print strQry
        print ('Querying station ' + str(ID) + ' for year ' + str(intYr) + ' and month ' + str(intMnt))
        try:
            response = url.request.urlopen(strQry)
            rawData = response.readlines()
            response.close()
            rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
           
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
            data = data.append(newData, ignore_index=True, sort=False)
        except Exception:
            print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr))
    
    data.to_csv("../data_set/EnviromentCanada/QuebecStations/"+str(ID)+".csv", index=False, line_terminator="")
    station.append(data)