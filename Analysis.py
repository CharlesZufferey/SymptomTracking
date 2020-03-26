# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:56:36 2020

@author: charl
"""

import pandas as pd
import numpy as np
#%%
data = pd.read_csv("documents/projects/SymptomTracking/fd-export.csv")##,delimiter="\t" )

#%%
a = data["user_id"].drop_duplicates()

#%% filtering for highly reported conditions only
b = data[["user_id","checkin_date","trackable_type","trackable_name","trackable_value"]]
b = b[b["trackable_type"]=="Condition"]
b = b[b["trackable_value"].astype(int)>2]
b["countconditions"] = b.groupby(["trackable_name"])["trackable_name"].transform("count")
b = b[b["countconditions"]>=500]
#%% filtering for highly reported symptoms only
c = data[["user_id","checkin_date","trackable_type","trackable_name","trackable_value"]]
c = c[c["trackable_type"]=="Symptom"]
#c = c[c["trackable_value"].astype(int)>2]
c["countsymptoms"] = c.groupby(["trackable_name"])["trackable_name"].transform("count")
c = c[c["countsymptoms"]>=500]

#%% creation of multiple df with weather info
d = data[["user_id","checkin_date","trackable_type","trackable_name","trackable_value"]]
d = d[d["trackable_type"]=="Weather"]
d1 =  d[d["trackable_name"]=="icon"]
d2 =  d[d["trackable_name"]=="temperature_min"]
d3 =  d[d["trackable_name"]=="temperature_max"]
d4 =  d[d["trackable_name"]=="precip_intensity"]
d5 =  d[d["trackable_name"]=="pressure"]
d6 =  d[d["trackable_name"]=="humidity"]
#%% generation of a global df with weather info
fullweather = pd.merge(d1,d2,on=["user_id","checkin_date"],suffixes=('_icon', '_mintemp'))
fullweather = pd.merge(fullweather,d3,on=["user_id","checkin_date"],suffixes=('_mintemp', '_maxtemp'))
fullweather = pd.merge(fullweather,d4,on=["user_id","checkin_date"],suffixes=('_maxtemp', '_precip'))
fullweather = pd.merge(fullweather,d5,on=["user_id","checkin_date"],suffixes=('_precip', '_pressure'))
fullweather = pd.merge(fullweather,d6,on=["user_id","checkin_date"],suffixes=('_pressure', '_humidity'))
#%% all weather info on one raw and deletion of useless columns
fullweather = fullweather[["user_id","checkin_date","trackable_value_icon"
                           ,"trackable_value_mintemp","trackable_value_maxtemp"
                           ,"trackable_value_precip","trackable_value_pressure",
                           "trackable_value_humidity"]]

#%% temporary final dataframe with one raw per symptom / conditions per day 
completeC = pd.merge(b,fullweather,on=["user_id","checkin_date"])
completeS = pd.merge(c,fullweather,on=["user_id","checkin_date"])
#%% Creation of a new columns with good vs bad weather
completeS["trackable_value_icon"].value_counts()
completeS["GoodWeather"] = [1 if (i == "partly-cloudy-day" or i == "partly-cloudy-night" or 
         i == "clear-day") else 0 for i in completeS["trackable_value_icon"]]
#%% creation of a column with average temp (although not great as its just a mean)
meanS = completeS.loc[: , "trackable_value_mintemp":"trackable_value_maxtemp"]
completeS["AvgTemp"] = meanS.mean()

#%%



c = data[data["user_id"]=="QEVuQwEA+1a8gyc3D+F/bQfKWtMBSw=="]