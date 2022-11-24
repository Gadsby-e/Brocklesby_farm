# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import requests 
import json
import pandas as pd
import numpy as np
#import bisect
#import python_dateutil

#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt

unsold_tonnage = '1000'

st.title("Brocklesby Farm Dashboard")

crop = st.radio(
     "Which crop dashboard would you like to view?",
     ('Wheat', 'Barley', 'Oilseed rape'))

#Add crop to market id dictionary

r = requests.get('https://www.theice.com/marketdata/DelayedMarkets.shtml?getHistoricalChartDataAsJson=&marketId=6425069&historicalSpan=3')
js = r.json()

listo1 = []
listo2 = []

for i in js['bars']:
    listo1.append(i[0])
    listo2.append(i[1])

dict1 = dict(zip(pd.to_datetime(listo1, format = '%a %b %d %H:%M:%S %Y'),listo2))

#target_key = st.date_input("sale date", pd.to_datetime('2021-09-14 00:00:00'))
#target_key1 = pd.to_datetime(target_key)
#print(type(target_key1))

fig, ax = plt.subplots()
ax.plot(dict1.keys(), dict1.values())


# =============================================================================
# A = -0.75, -0.25, 0, 0.25, 0.5, 0.75, 1.0
# B = 0.73, 0.97, 1.0, 0.97, 0.88, 0.73, 0.54
# 
# ax.plot(A,B)
# for xy in zip(A, B):                                       # <--
#     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
# for i in range(len(x)):
# plt.annotate(text[i], (x[i], y[i] + 0.2))
# =============================================================================
sales0 = pd.read_csv('sales.csv', dtype={'Date': 'string', 'Price': 'float64', 'Quantity': 'string'}, parse_dates=['Date'])
sales = sales0[sales0.Crop == crop].reset_index()
sales['quan_text'] = 'Quantity: '+ sales.Quantity + 't'
#sales['scaled_q'] = 5*sales.Quantity/sales.Quantity.max()
ax.scatter(sales.Date, sales.Price, marker='o')#, c="red")
for i in range(len(sales)):
    ax.annotate(sales.quan_text[i], (sales.Date[i], sales.Price[i] -20))




st.pyplot(fig)

st.write('Proportion of estimated ' + crop + ' harvest tonnage')

latest_price = str(list(dict1.values())[-1])

prices = list(sales.Price.astype('string'))
prices.insert(0, latest_price)
prices2 = ['£' + sub for sub in prices]

quantities = list(sales.Quantity)
quantities.insert(0, unsold_tonnage)

fig1, ax1 = plt.subplots()

ax1.pie(quantities, labels = prices2)

st.pyplot(fig1)