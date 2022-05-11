#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:39:27 2022

@author: izzygetchell
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 

plt.rcParams['figure.dpi']=300
#set default resolution 

sns.set_theme(style='white')

irma_data = pd.read_csv('irma.csv')

print('Information within Dataset:', irma_data.info())

variables = ['damagedZipCode', 'householdComposition', 'grossIncome', 'ownRent', 'residenceType', 'rentalAssistanceEligible']
usable_irma = irma_data.dropna(subset=variables)

count_by_zip = usable_irma.groupby('damagedZipCode').size()

count_by_zip.to_csv('Count_by_Zip.csv')
#creates a file recording the number of applicants for Individual Housing 
#Assistance per zip code in Miami
#%% 
#Filter to find the 5 zip codes with the most applicants, and 5 zip codes 
#with the most low income applicants (according to self reported gross income), 
#then write the top 5 zips (by applicant number) to a new file
n=5
top_five_count = usable_irma['damagedZipCode'].value_counts().index.tolist()[:n]
print(top_five_count)

lowinc = usable_irma.query("grossIncome <= 24050")
n=5 
low_inc_count = lowinc['damagedZipCode'].value_counts().index.tolist()[:n]
print(low_inc_count)

by_zip_count = usable_irma.sort_values('damagedZipCode')
by_zip_count.set_index('damagedZipCode', inplace=True)

by_zip_count = by_zip_count.loc[[33142, 33147, 33125, 33177, 33165]]

by_zip_count.to_csv('Top_5_Zips.csv')

most=pd.read_csv('Top_5_Zips.csv')
#%%
#Visual Overview of the top 5 Zip Code Data 

variables = ['damagedZipCode', 'householdComposition', 'grossIncome', 'ownRent', 'residenceType', 'rentalAssistanceEligible']
for var in variables:
    print(var)
    print(most[var].value_counts())
    fig = sns.catplot(y=var, data=most, kind='count')

#%%
#Household Composition across 5 zip codes with most applicants 
residence = most.query("ownRent == 'Owner' or ownRent=='Renter'")
fig,ax1 = plt.subplots()
sns.violinplot(data=residence, x='damagedZipCode', y='householdComposition', hue='ownRent', split=True, ax=ax1)
ax1.set_xlabel('Zip Code')
ax1.set_title('Household Composition (Individuals) Across Zip Code')
fig.tight_layout()
fig.savefig('f_householdComp_vio.png')
#%%
# Residence Type across top 5 zip codes - house/duplex, townhouse, or apartment RENTERS only
residence = residence.query("residenceType == 'Apartment' or residenceType =='House/Duplex' or residenceType == 'Townhouse'")
residence = residence.query("ownRent == 'Renter'")

fig2, ax2 = plt.subplots()
sns.countplot(x='residenceType', hue='damagedZipCode', data=residence)
ax2.set_title('Renter Residence Type Across Zip Code')
fig2.tight_layout()
fig2.savefig('f2residence_zip.png')
#%% 

#filter down to low income renters only in the 5 zip codes with the most applicants
mean_inc = most['grossIncome'].median()
print('median renter income:', mean_inc)

low = most.query("grossIncome <= 24050")

variables2 = ['damagedZipCode', 'householdComposition', 'ownRent', 'residenceType', 'rentalAssistanceEligible']
use = low.dropna(subset=variables2)

for var in variables2:
    fig=sns.catplot(y=var, data=low, kind='count')

#%%
#household composition across 5 zip codes - low income renter applicants
lowest=low.query("ownRent == 'Owner' or ownRent=='Renter'")

print('Low Income Renters:', len(low))

fig3, ax1 = plt.subplots()
sns.violinplot(data=lowest, x='damagedZipCode', y='householdComposition', hue='ownRent', split=True, ax=ax1)
ax1.set_title('Low Income Household Composition Across Zip Code')
fig3.tight_layout()
fig3.savefig('low_inc_house_comp.png')

#residence type across 5 zip codes - low income renter applicants 

lowest=lowest.query("residenceType == 'Apartment' or residenceType =='House/Duplex' or residenceType == 'Townhouse'")
lowest=lowest.query("ownRent=='Renter'")

fig4,ax1 = plt.subplots()
sns.countplot(x='residenceType', hue='damagedZipCode', data = lowest, ax=ax1)
ax1.set_title('Low Income Renter Residence Type Across Zip Code')
fig4.tight_layout()
fig4.savefig('low_inc_residence.png')

#renter assistance eligbility across low income renters in top 5 zip codes 

fig5 = sns.catplot(y='rentalAssistanceEligible', data = lowest, kind='count')
fig5.tight_layout()
fig5.savefig('LowInc_RentalAssistance.png')
