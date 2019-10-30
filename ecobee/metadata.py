#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:45:31 2019

@author: Guilherme de Brito Abreu, undergraduate student at @unicamp.
"""

# metadata column names
dataIdCol    = 'Identifier'
countryCol   = 'Country'
frstCnctCol  = 'First Connected'
filenameCol  = 'filename'
plcStyleCol  = 'Style'
provStateCol = 'ProvinceState'
userIdCol    = 'UserID'
areaCol      = 'Floor Area [ft2]'
cityCol      = 'City'
modelCol     = 'Model'
plcAgeCol    = 'Age of Home [years]'
occpNumCol   = 'Number of Occupants'
coolStageCol = 'installedCoolStages'
heatStageCol = 'installedHeatStages'
compAuxCol   = 'allowCompWithAux'
ElectricCol  = 'Has Eletric'
heatPumpCol  = 'Has a Heat Pump'
heatTypeCol  = 'Auxilliary Heat Fuel Type'
remSenNumCol = 'Number of Remote Sensors'
plsEnrCol    = 'eco+ enrolled'
plsEnrLvlCol = 'eco+ slider level'

import pandas as pd

class metaData:
  
    def __init__(self, path):
        self.data = pd.read_csv(path)