# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:48:27 2022

@author: Joseph Bedford
"""

import streamlit as st
import requests 
import json
import pandas as pd
import numpy as np

#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

grey_shade  = '0.75'
chart_xaxis_date_format = mdates.DateFormatter("%b-%y")

st.title("Brocklesby Farm Dashboard")
st.subheader('Harvest 2022 forward sales')

config = pd.read_csv('config.csv',
                     dtype = {0: str, 1: str, 2: np.float64, 3: bool, 4: str, 5:np.float64, 6:np.float64})
config['sales_date'] = pd.to_datetime(config.sales_date, infer_datetime_format=True)

crops = config.crop.drop_duplicates().tolist()
#chosen_crop = crops[0]

chosen_crop = st.radio(
     "Which crop dashboard would you like to view?",
     (crops[0], crops[1], crops[2]))
filtered_config = config[config.crop == chosen_crop].dropna()
market_id = filtered_config.market_id.drop_duplicates().reset_index(drop = True)[0]

url = 'https://www.theice.com/marketdata/DelayedMarkets.shtml?getHistoricalChartDataAsJson=&marketId='+market_id+'&historicalSpan=3'

r = requests.get(url)
js = r.json()

listo1 = []
listo2 = []

for i in js['bars']:
    listo1.append(i[0])
    listo2.append(i[1])

dict1 = dict(zip(pd.to_datetime(listo1, format = '%a %b %d %H:%M:%S %Y'),listo2))



fig, ax = plt.subplots()
ax.plot(dict1.keys(), dict1.values(), c = 'black')

ax.scatter(filtered_config.sales_date, filtered_config.sales_price, marker='o', c="blue")
ax.xaxis.set_major_formatter(chart_xaxis_date_format)
if 'barley'.casefold() in chosen_crop.casefold():
    ax.set_ylabel('*Wheat* price £/t\n('+chosen_crop+' usually tracks ~ 10% below)')
else:
    ax.set_ylabel(chosen_crop+' price £/t')


    
latest_total_crop_tonnage = filtered_config[filtered_config.sales_date == max(filtered_config.sales_date)].total_crop_tonnage.reset_index(drop = True)[0]
latest_is_estimate_flag = filtered_config[filtered_config.sales_date == max(filtered_config.sales_date)].total_crop_tonnage_is_estimate.reset_index(drop = True)[0]
total_sales_tonnage = filtered_config.sales_tonnage.sum()
remaining_tonnage_to_sell = latest_total_crop_tonnage - total_sales_tonnage

total_sales_avg_price = np.average(filtered_config.sales_price, weights=filtered_config.sales_tonnage)

percentage_of_total_sold = 100*filtered_config.sales_tonnage/latest_total_crop_tonnage


fig_b, ax_b = plt.subplots()
ax_b.bar(filtered_config.sales_date,percentage_of_total_sold, width = 5, color = 'blue')
#ax_b.bar(filtered_config.sales_date,100-percentage_of_total_sold,width = 5, bottom=percentage_of_total_sold, color = grey_shade)
ax_b.set_ylabel('Sale percentage of the total')#note that a width of 1.0 is 1 day
ax_b.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=False))
ax_b.set_xlim(ax.get_xlim())
ax_b.xaxis.set_major_formatter(chart_xaxis_date_format)


pie_chart_values = list([total_sales_tonnage, 
                         remaining_tonnage_to_sell])


#pie_chart_labels = list(['Average sales price (£'+str(int(total_sales_avg_price))+'/t)',
#                        'Remaining tonnage to sell ('+str(int(remaining_tonnage_to_sell))+'t)'])

pie_chart_labels = list([str(int(total_sales_tonnage))+' tonnes sold at an average price of £'+str(int(total_sales_avg_price))+'/t',
                       str(int(remaining_tonnage_to_sell))+' tonnes left to sell'])

fig_p, ax_p = plt.subplots()

ax_p.pie(pie_chart_values, labels = pie_chart_labels, colors = ['blue', grey_shade]) #greyshade colour

st.pyplot(fig)
st.pyplot(fig_b)
#st.markdown('<div style="text-align: left;">Hello World!</div>', unsafe_allow_html=True)
#st.markdown('<div style="text-align: right;">Hello World!</div>', unsafe_allow_html=True)

#if latest_is_estimate_flag:
#    st.write('Expected crop yeild')
#else:
#    st.write('Actual crop yeild')
        
st.pyplot(fig_p)  