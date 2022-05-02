#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 23:04:12 2022

@author: sahilmammadli
"""

#  importing

import csv
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import fiona
from adjustText import adjust_text
import squarify
import io
import zipfile
from collections import defaultdict 
import requests
from math import sin, cos, pi



#load csv
data_main = pd.read_csv("MUNW_28042022020655079.csv")


# show first 5 column
print(data_main.head())
print(len(data_main))

#Dataframe information
print('\nDataframe information:\n')
data_main.info()

#copy
oecd = data_main[[ "COU","Country","VAR","Variable","Year","Value" ]].copy()

#check columns
oecd.columns

#Data of VAR 
oecd.VAR.unique()

# check the countries
oecd.Country.unique()

#MUNICIPAL
oecd_data_mun = ['MUNICIPAL']
oecd_waste_mun = oecd[oecd.VAR.isin(oecd_data_mun)]   #https://www.youtube.com/watch?v=3Kl5oaT0dP0

#Recycling
oecd_data_recycle = ['RECYCLING']
oecd_waste_recycle = oecd[oecd.VAR.isin(oecd_data_recycle)]

#Recovery
oecd_data_recovery = ['RECOVERY']
oecd_waste_recovery = oecd[oecd.VAR.isin(oecd_data_recovery)]

#%%

# Extended Producer Responsibility (EPR) is a policy approach under which producers are given a significant responsibility – financial and/or physical – for the treatment or disposal of post-consumer products.
country_EPR_year = {
   "Finland": 1997, "Germany": 1991, 'United Kingdom':1997, 'Israel':2011, "France": 1992,
   "Japan": 1995,"Australia": 1997, 'Sweden': 1993,
   }
for country in country_EPR_year:
    #Muncipal
    mun = oecd_waste_mun[oecd_waste_mun.Country.isin([country])]
    #Recyling
    recycling = oecd_waste_recycle[oecd_waste_recycle.Country.isin([country])]
    #Recovery
    #recovery = oecd_waste_recovery [oecd_waste_recovery .Country.isin([country])]
    #Data using sort_value
    year = mun['Year'].sort_values()
    muni_waste = []
    
    for x in year:
        f = False
        for index, waste in mun.iterrows():
            if waste['Year'] == x:
                muni_waste.append(waste['Value'])
                f = True
        if not f:
            muni_waste.append(0)
            
    recycle_waste = []
    for x in year:
        f = False
        for index, recycle in recycling.iterrows():
            if recycle['Year'] == x:
                recycle_waste.append(recycle['Value'])
                f = True
        if not f:
            recycle_waste.append(0)


    # plot area

    fig = plt.figure()
    myaxes = fig.add_subplot()
    myaxes.plot(year,muni_waste,"r",lw=3, label = 'Total waste',marker='s', markersize=4,markerfacecolor="yellow", markeredgewidth=1, markeredgecolor="green")
    myaxes.plot(year,recycle_waste,"b",lw=3, label = 'Recycle', marker='o', markersize=4,markerfacecolor="black", markeredgewidth=1)
    #myaxes.plot(year,recovery_waste,"y",lw=3, label = 'recovery')
    myaxes.set_xlabel('Years')
    myaxes.set_ylabel('Tonnes, Thousands')
    myaxes.set_title(country + ': Waste generation vs Recycling')
    plt.axvline(x=country_EPR_year[country], label = 'EPR adoption(year)', color='g', linestyle='--')

    myaxes.legend()
    fig.tight_layout()
    fig.savefig(country + '.png')

