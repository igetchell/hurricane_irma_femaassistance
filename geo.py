#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:28:08 2022

@author: izzygetchell
"""

import geopandas as gpd
import pandas as pd 
import numpy as np 
import requests

geo = gpd.read_file('cb_2019_us_zcta510_500k.zip')

counts = pd.read_csv('Count_by_Zip.csv', dtype={'damagedZipCode':str})
#%% #merge fema count data onto the shapefile
geo = geo.merge(counts, left_on= 'ZCTA5CE10', right_on='damagedZipCode', 
                how='outer', validate='1:1', indicator=True)

print(geo['_merge'].value_counts())
geo = geo.drop(columns='_merge')

#%% #merge census data (population total and median income) onto irma data

variables = {'B02001_001E':'pop_total', 
             'B06011_001E':'median_income'
             }

var_list = variables.keys()

var_string = ','.join(var_list)

api = 'https://api.census.gov/data/2019/acs/acs5'

for_clause = 'zip code tabulation area:*'
in_clause = 'state:12'

payload = {'get':var_string, 'for':for_clause, 'in':in_clause}

response = requests.get(api, payload)

rows = response.json()

colnames = rows[0]
datarows = rows[1:]

pop = pd.DataFrame(columns=colnames, data=datarows)

pop = pop.replace('-666666666', np.nan)

pop = pop.rename(columns=variables)

pop = pop.rename(columns={ 'zip code tabulation area': 'ZCTA5CE10'})

pop.to_csv('pop_by_zip.csv')

#%% 
#fitler shapefile down to Miami-Dade and Broward County and merge new 
#population data onto it
county = gpd.read_file('tl_2019_us_county.zip')
county = county.query("GEOID == '12086' or GEOID == '12011'")

merged = geo.merge(pop, on='ZCTA5CE10', how='outer', indicator=True)

merged['pop_total']=merged['pop_total'].astype(float)
merged['median_income']=merged['median_income'].astype(float)

print(merged['_merge'].value_counts())
merged = merged.drop(columns='_merge')

geo = merged.dropna(subset=['0'])

geo = geo.clip(county, keep_geom_type=True)

geo.to_file('geo_clip.gpkg', layer='counts', index=False)

#writes out a geopackage to use map certain demographics and applicant data 
#in GIS 





