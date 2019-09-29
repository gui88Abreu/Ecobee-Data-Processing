#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 17:55:20 2019

@author: guilherme
"""

import pandas as pd
import numpy as np

def check_shape(data, day, day_name = 'DAY365'):
    '''
    Input:
        data: Pandas Data Frame Object.
        day: A dat as an integer.
        day_name: The name of the column that contains the days.
    Output:
        It returns a boolean. It returns True if the number of 
        the lines of the specified column is more than one and
        False otherwise.
    '''
    if(data[data[day_name] == day].shape[0] == 0):
        return False
    else:
        return True
    
def check_2days(data, day, day_name = 'DAY365'):
    '''
    Input:
        data: Pandas Data Frame Object.
        day: A dat as an integer.
        day_name: The name of the column that contains the days.
    Output:
        It returns a boolean. It returns True if there are data
        from 2 days back until the day specified and False otherwise.
    '''
    
    # If there is information in df in the day in question and 2 back as well, then return True, else there is no way to there is a heatwave
    if((check_shape(data,day,day_name)) & (check_shape(data,day-1, day_name)) & (check_shape(data,day-2, day_name))):
        return True
    else:
        return False

# Function that if "check_2days" is True we check if in these 2 days the definition of heatwave is satisfied
def init_hw(data,day,index = 'CTX90pct',min_tmp_name = 'MIN_N_AIRTMP_MED10', max_tmp_name = 'MAX_N_AIRTMP_MED10',
            day_name = 'DAY365'):
    '''
    Input:
        data: Pandas Data Frame Object.
        day: the value of the day.
        min_air_var_name: the name of the column that contains the min_air temperature.
        max_air_var_name: the name of the column that contains the max_air temperature.
        min_air_p90: the value of the min temperature that represents the percentil 90 for this day.
        max_air_p90: the value of the max temperature that represents the percentil 90 for this day.
    Output:
        It returns a boolean. It returns True if it was registered tempreratures above the percentil 90
        from 2 days back until the day specified or from this day until 2 days forward. It returns False otherwise.
    '''
    
    if min_tmp_name == max_tmp_name:
        var_names = [min_tmp_name, day_name, 'p90_min', 'p90_max']
    else:
        var_names = [min_tmp_name,max_tmp_name,day_name,'p90_min', 'p90_max']
    
    actual_df = data[data[day_name] == day][var_names]
    df1_back = data[data[day_name] == day - 1][var_names]
    df2_back = data[data[day_name] == day - 2][var_names]
    df1_forward = data[data[day_name] == day + 1][var_names]
    df2_forward = data[data[day_name] == day + 2][var_names]
    
    if(check_2days(data,day, day_name)):
            
        
        c1_b = c2_b = c1_f = c2_f = c3 = False
        # Defining conditions so that there is or not a heatwave
        if(index == 'CTN90pct'):
            if not df1_back.empty:
                c1_b = np.max(df1_back[min_tmp_name].values) >= df1_back['p90_min'].values[0]
            if not df2_back.empty:
                c2_b = np.max(df2_back[min_tmp_name].values) >= df2_back['p90_min'].values[0]
            if not df1_forward.empty:    
                c1_f = np.max(df1_forward[min_tmp_name].values) >= df1_forward['p90_min'].values[0]
            if not df2_forward.empty:
                c2_f = np.max(df2_forward[min_tmp_name].values) >= df2_forward['p90_min'].values[0]
            if not actual_df.empty:
                c3   = np.max(actual_df[min_tmp_name].values) >= actual_df['p90_min'].values[0]
        elif(index == 'CTX90pct'):
            if not df1_back.empty:
                c1_b = np.max(df1_back[max_tmp_name].values) >= df1_back['p90_max'].values[0]
            if not df2_back.empty:
                c2_b = np.max(df2_back[max_tmp_name].values) >= df2_back['p90_max'].values[0]
            if not df1_forward.empty:    
                c1_f = np.max(df1_forward[max_tmp_name].values) >= df1_forward['p90_max'].values[0]
            if not df2_forward.empty:
                c2_f = np.max(df2_forward[max_tmp_name].values) >= df2_forward['p90_max'].values[0]
            if not actual_df.empty:
                c3   = np.max(actual_df[max_tmp_name].values) >= actual_df['p90_max'].values[0]
        else:
            print('A valid index name is required.')
            return False
        
        #Condition if there are 2 days before now that the temperature exceeds the pth
        c_b = c1_b & c2_b
        
        #Condition if there are 2 days AFTER now that the temperature exceeds the pth
        c_f = c1_f & c2_f
        
        if c3&(c_b | c_f):
            return True
        else:
            return False
    else:
        return False

# Function to actually get heatwaves
def get_heatwave(data, flag, mean_tmp_name = None, hw_name='none', index = 'CTX90pct',percentile = 90, 
                 day_name = 'DAY365', year_name = 'YEAR',min_tmp_name = 'MIN_N_AIRTMP_MED10', max_tmp_name = 'MAX_N_AIRTMP_MED10'):
    '''
    Input:
        data: Pandas Data Frame Object.
        flag: The name of the column that will contain flags to denote heatwaves.
        hw_name: The name of the column that will contain the labels for each heatwave.
        mean_tmp_name: The name of the column that contains the air mean temperatures.
        day_name: The name of the column that contains the days.
        year_name: The name of the column that contains the years.
        min_tmp_name: The name of the column that contains the air min temperatures.
        max_tmp_name: The name of the column that contains the air max temperatures.
        percentile: the value of the percentile that will be used on the algorithm.
        index: Use 'CTX90pct' for maximum temperatures and 'CTN90pct' for minimum temperatures.
    Output:
        It returns a Pandas Data Frame with 3 new columns (flag column, hw_name column and 'Pencentil 90' column).
        For flag and hw_name colmuns, the days labeld with an integer greater than one denotes a heatwave.
        the last column, 'Percentil 90', contains de percentil calculated for each day.
    ''' 
    
    if mean_tmp_name != None:
        min_tmp_name = max_tmp_name = mean_tmp_name
    
    
    # copy data frame
    df = data.copy()
    
    flag_heat = flag
    flag_unique_heat = hw_name

    # Create new columns on the data frame and iniate them with zeros.
    df[flag_heat] = 0
    df[flag_unique_heat] = 0
    df['p90_max'] = np.nan
    df['p90_min'] = np.nan

    # Variable that labels unique heatwaves, each one of heatwaves will have a unique integer number
    which_heat_wave = 1
    new_hw = False
    
    for y in df[year_name].unique():
        df_year = df[df[year_name] == y]
        itera = iter(df_year[day_name].unique())

        for d in itera:
            # For each day there will be a different pct
            df_pct = df_year[(df_year[day_name] >= d-15) & (df_year[day_name] <= d + 15)]
            
            # organize data to get the percentiles
            max_t = []
            min_t = []
            for day in df_pct[day_name].unique():
                mx = df_pct[df_pct[day_name] == day][max_tmp_name].unique()
                max_t.append(mx)
            
            for day in df_pct[day_name].unique():
                mn = df_pct[df_pct[day_name] == day][min_tmp_name].unique()
                min_t.append(mn)
            
            # get the percentiles
            pth_max = np.percentile(np.asarray(max_t), percentile)
            pth_min = np.percentile(np.asarray(min_t), percentile)   
            
            # save percentiles
            df.loc[(data[year_name] == y) & (data[day_name] == d) , 'p90_max'] = pth_max
            df.loc[(data[year_name] == y) & (data[day_name] == d) , 'p90_min'] = pth_min
        
        itera = iter(df_year[day_name].unique())
        for d in itera:
            
            # verify if it was registered temperatures above the percentils
            if init_hw(df_year,d,index = index,max_tmp_name = max_tmp_name, min_tmp_name = min_tmp_name, day_name = day_name):
                
                # label the heat wave encountered on the data frame
                new_hw = True
                df.loc[(df[year_name] == y) & (df[day_name] == d) , flag_heat] = 1
                df.loc[(data[year_name] == y) & (data[day_name] == d) , flag_unique_heat] = which_heat_wave
            else:
                if(new_hw == True):
                    which_heat_wave = which_heat_wave + 1
                    new_hw = False
            # Fill the data frame with its percentils for each day.
            
    return df