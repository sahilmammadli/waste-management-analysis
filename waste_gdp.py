#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 19:20:03 2022

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

#load csv
data = pd.read_csv("country_level_data_0.csv")

#load GDP from another csv file
data_gdp = pd.read_csv("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4019306.csv")
print(data_gdp.head())
#data_gdp.info()

# find and assign the gdp of a country from data_gdp based on the name of the country
for index_gdp, row_gdp in data_gdp.iterrows():
    for index, row in data.iterrows():
        if row_gdp['Country Name'] == row['country_name']:
            data.at[index,'gdp'] = row_gdp['2019']


# show first 5 c)olumn
#print(data.head())
#print(len(data))
#print('\nDataframe information:\n')
#data.info()


data.dropna(subset=['gdp'])
data.dropna(subset=['population_population_number_of_people'])
data.dropna(subset=['total_msw_total_msw_generated_tons_year'])


# Using DataFrame.copy() create new DaraFrame.
df2 = data[[ 'iso3c','country_name', 'gdp',"population_population_number_of_people" ]].copy()


# The formula to calculate GDP per capita is a country's gross domestic product (GDP) divided by its population. This calculation reflects a nation's standard of living.

# calc GDP per capita. dividing gdp to total population
gdp_per_capita = data ["gdp"]/data["population_population_number_of_people"]
#print( gdp_per_capita)

per_capita_MSW_generation = data ["total_msw_total_msw_generated_tons_year"]*1000/data["population_population_number_of_people"]/365

per_capita_MSW_generation_year = (data ["total_msw_total_msw_generated_tons_year"])*1000/data["population_population_number_of_people"]  #kg/person/year

#print (per_capita_MSW_generation)

df2['GDP per Capita'] = gdp_per_capita
df2 ['Daily waste generation per capita'] = per_capita_MSW_generation
df2['per_capita_MSW_generation_year' ] = per_capita_MSW_generation_year 


df2 = df2.rename(columns={'country_name':'Country',
                           'population_population_number_of_people':'Population',
                           'gdp':'GDP'})

# Countries that are going to be highlighted
country_small = [
    "Turks and Caicos Islands", "Sint Maarten (Dutch part)", "Cayman Islands ", "Guam", "Singapore", 
    "Greenland", "Aruba", "British Virgin Islands", "Channel Islands ", "Monaco", 
    "Faeroe Islands", "Bermuda", "Virgin Islands (U.S.)", 'Cayman Islands', 'Channel Islands'
]

df2= df2[~df2['Country'].isin(country_small)]
countries = df2['Country']


#%%


# Countries that are going to be highlighted
COUNTRY_HIGHLIGHT = [
    "Germany", "Norway", "United States", "Greece", "Singapore", 
    "Rwanda", "Russia", "Venezuela", "Sudan", "Iraq", "Ghana", 
    "Niger", "Chad", "Kuwait", "Qatar",     "Myanmar", "Nepal", 
    "Chile", "Argentina", "Japan", "China", "Germany", 
    'Turkey', 'Luxembourg', 'Qatar', 'Canada', 'France', 'United Kingdom',
    'Brazil', 'Kenya', 'Indonesia','India', 'Afganistan', 'Estonia', 'Finland', 'Sweeden', 
]


#
MSWPC = df2["GDP per Capita"].values
GDPPC = df2['per_capita_MSW_generation_year'].values

#
fig, ax = plt.subplots(figsize=(12, 8));
ax.scatter(MSWPC, GDPPC);


# Add labels
# Iterate through all the countries in COUNTRIES
# `ax.text()` outputs are appended to the `TEXTS` list. 
# This list is passed to `adjust_text()` to adjust the position of
# the legends and add connecting lines
TEXTS = []
for idx, country in enumerate(countries):
    # Only append selected countries
    if country in COUNTRY_HIGHLIGHT:
        x, y = MSWPC[idx], GDPPC[idx]
        TEXTS.append(ax.text(x, y, country, fontsize=12));

# Adjust text position and add lines
# 'expand_points' is a tuple with two multipliers by which to expand
# the bounding box of texts when repelling them from points

# 'arrowprops' indicates all the properties we want for the arrows
# arrowstyle="-" means the arrow does not have a head 
adjust_text(
    TEXTS, 
    expand_points=(3, 3),
    arrowprops=dict(arrowstyle="-", lw=1),
    ax=ax
);

# plotting
ax.set_facecolor("white") # set axis background color to white
ax.set_xlabel('GDP per capita($)')
ax.set_ylabel('Waste generation per capita year (kg)')
ax.set_title("GDP per capita & Waste generation per capita ")
fig.set_facecolor("white") # set figure background color to white
fig.savefig("GDP_MSW.png", dpi=300)

#%%

df2 = df2.set_index('Country')
top_waste = df2['Daily waste generation per capita'].sort_values()[-20:]

#print("type of top_waste",type(top_waste))
#top_waste_list = df2['Daily waste generation per capita'].tolist()
#print ("\nTop 20 most waste generate")
#print ("Top Waste len", len(top_waste_list), type(top_waste_list))
#top_waste_list, country_names = zip(*sorted(zip(top_waste_list, top_waste_list)))


least_waste =  df2['Daily waste generation per capita'].sort_values()[:20]

print ("\nTop and Least Daily Waste Generation")
print (least_waste)

fig, (ax1,ax2) = plt.subplots(1,2,dpi=300)
fig.suptitle("Countries' daily waste generation per capita (kg)")
top_waste.plot.barh(ax=ax1,fontsize=7)
ax1.set_ylabel("Most waste-producing countries")
least_waste.plot.bar(ax=ax2, fontsize=7)
ax2.set_xlabel ("Least waste-producing countr.")
fig.tight_layout()
fig.savefig ("most_least.png",dpi=300)



#%%


#Save csv file
global_waste_index = df2[[ 'iso3c', 'Daily waste generation per capita' ]].copy()
global_waste_index.to_csv("global_waste_index.csv")


