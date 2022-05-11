#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:08:17 2022

@author: izzygetchell
"""

import requests 
import pandas as pd 

#uses API call to retrieve housing applicant records for Individual Housing
#assistance in Miami following Hurricane Irma 
    
api = 'https://www.fema.gov/api/open/v1/IndividualAssistanceHousingRegistrantsLargeDisasters'
 
irma = {
        '$filter': "disasterNumber eq '4337' and damagedCity eq 'MIAMI'",
        '$format':'json',
        '$select':'disasterNumber, damagedCity, damagedZipCode, ownRent, residenceType, householdComposition, grossIncome, rentalAssistanceEligible'
        }

skip = 0
top = 1000

frame = pd.DataFrame()

#Since FEMA only allows 1000 records to be downloaded at a time, this loop 
#retreives all records (a little over 352,000)

for n in range(0, 353):
    irma['$top']=str(top)
    irma['$skip']=str(skip)
    response = requests.get(api, irma)
    info = response.json() 
    data = info['IndividualAssistanceHousingRegistrantsLargeDisasters']
    values = pd.DataFrame(data)
    print(n, len(values), flush = True) #tells operating system to write info out 
    #immediately 
    frame = pd.concat( [frame, values] )
    if len(values) < top:
        break 
    skip = skip+top

frame.set_index('disasterNumber', inplace=True)

#writes the dataframe to a CSV to use later

frame.to_csv('irma.csv')
