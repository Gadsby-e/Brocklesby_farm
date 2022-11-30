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
from PIL import Image
import itertools

#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates

logo = Image.open('logo.jpg')
st.set_page_config(page_icon=logo, page_title = 'Brocklesby Farm')
grey_shade  = '#abb8c3'
blue_shade = '#223448'
black_shade = '#1a1a1a'
chart_xaxis_date_format = mdates.DateFormatter("%b-%y")
 
#centre justified

st.markdown("<h1 style='text-align: center; '>Brocklesby Farm Dashboard</h1>", unsafe_allow_html=True) #works
st.markdown("<h2 style='text-align: center;'>Harvest 2022 forward sales </h2>", unsafe_allow_html=True) #works

#st.title("Brocklesby Farm Dashboard") #works but wrapped in column
#st.subheader('Harvest 2022 forward sales') #works but wrapped in column

config = pd.read_csv('config.csv',
                     dtype = {0: str, 1: str, 2: str, 3: np.float64, 4: bool, 5: str, 6:np.float64, 7:np.float64})
config['sales_date'] = pd.to_datetime(config.sales_date, infer_datetime_format=True)

crops = config.crop.drop_duplicates().tolist()
#chosen_crop = crops[0]
#st.markdown('<div style="text-align: center;">Which crop dashboard would you like to view?</div>', unsafe_allow_html=True)
#col1, col2, col3 = st.columns([1.5,1,1])
chosen_crop = st.radio(
     '',
     (crops[0], crops[1], crops[2]))


#now left justified with extra line space
st.write('\n')
st.subheader(chosen_crop)

filtered_config = config[config.crop == chosen_crop].dropna().reset_index(drop = True)
market_id = filtered_config.market_id[0]
market_date = filtered_config.market_date[0]
wheat_crop = next(itertools.takewhile(lambda x: 'wheat'.casefold() in x.casefold(), crops))#extracts wheat crop from list


url = 'https://www.theice.com/marketdata/DelayedMarkets.shtml?getHistoricalChartDataAsJson=&marketId='+market_id+'&historicalSpan=3'

r = requests.get(url)
js = r.json()

listo1 = []
listo2 = []

for i in js['bars']:
    listo1.append(i[0])
    listo2.append(i[1])

dict1 = dict(zip(pd.to_datetime(listo1, format = '%a %b %d %H:%M:%S %Y'),listo2))

annotate_key = (list(dict1)[1]) #annotate top left
annotate_value = max(dict1.values())


fig, ax = plt.subplots()
ax.plot(dict1.keys(), dict1.values(), c = black_shade)

ax.scatter(filtered_config.sales_date, filtered_config.sales_price, marker='o', c=blue_shade)
ax.xaxis.set_major_formatter(chart_xaxis_date_format)
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
for label in ax.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
#ax.annotate('LIFFE '+chosen_crop+' May-23', (annotate_key, annotate_value))#sort for barley
ax.set_ylabel('Price (£/t)')
if 'barley'.casefold() in chosen_crop.casefold():
    ax.annotate('LIFFE *'+wheat_crop+'* '+market_date, (annotate_key, annotate_value)) #not ideal non dynamic
else:
    ax.annotate('LIFFE '+chosen_crop+' '+market_date, (annotate_key, annotate_value))#sort for barley


tonnage_is_estimate = filtered_config.total_crop_tonnage_is_estimate[0]
latest_total_crop_tonnage = filtered_config[filtered_config.sales_date == max(filtered_config.sales_date)].total_crop_tonnage.reset_index(drop = True)[0]
latest_is_estimate_flag = filtered_config[filtered_config.sales_date == max(filtered_config.sales_date)].total_crop_tonnage_is_estimate.reset_index(drop = True)[0]
total_sales_tonnage = filtered_config.sales_tonnage.sum()
remaining_tonnage_to_sell = latest_total_crop_tonnage - total_sales_tonnage

total_sales_avg_price = np.average(filtered_config.sales_price, weights=filtered_config.sales_tonnage)

percentage_of_total_sold = 100*filtered_config.sales_tonnage/latest_total_crop_tonnage


fig_b, ax_b = plt.subplots()
ax_b.bar(filtered_config.sales_date,percentage_of_total_sold, width = 5, color = blue_shade)
if tonnage_is_estimate:
    ax_b.set_ylabel('Sale percentage of the estimated total')#note that a width of 1.0 is 1 day
else:
    ax_b.set_ylabel('Sale percentage of the total')#note that a width of 1.0 is 1 day
ax_b.xaxis.set_minor_locator(mdates.MonthLocator())
ax_b.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3,6,9,12)))
for label in ax_b.get_xticklabels(which='major'):
    label.set(rotation=30, horizontalalignment='right')
ax_b.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=False))
ax_b.set_xlim(ax.get_xlim())
#tick marks per month, labels every 3month
ax_b.xaxis.set_major_formatter(chart_xaxis_date_format)


pie_chart_values = list([total_sales_tonnage, 
                         remaining_tonnage_to_sell])
# =============================================================================
# 
# col1, col2 = st.columns([1,1])
# 
# with col1:
#  #st.write(f"你选择了{color1}")
#     st.write(str(int(total_sales_tonnage))+' tonnes sold at an average price of £'+str(int(total_sales_avg_price))+'/t')
# with col2:
#     st.write(f"{str(int(remaining_tonnage_to_sell))} tonnes left to sell")
# =============================================================================
#wrap text on pie too long atm
# =============================================================================
# if tonnage_is_estimate:
#     pie_chart_labels = list([str(int(total_sales_tonnage))+' tonnes sold at\nan average price of\n£'+str(int(total_sales_avg_price))+'/t',
#                              str(int(remaining_tonnage_to_sell))+' tonnes\nleft to sell\n(estimate)'])
# else:
#     pie_chart_labels = list([str(int(total_sales_tonnage))+' tonnes sold at\nan average price of\n£'+str(int(total_sales_avg_price))+'/t',
#                              str(int(remaining_tonnage_to_sell))+' tonnes\nleft to sell'])
# 
# =============================================================================

pie_label1 = f"{str(int(total_sales_tonnage))}t sold at an average price of £{str(int(total_sales_avg_price))}/t"
pie_label2 = f"{str(int(remaining_tonnage_to_sell))}t left to sell"

fig_p, ax_p = plt.subplots()

ax_p.pie(pie_chart_values, colors = [blue_shade, grey_shade]) 
fig_p.tight_layout()
fig_p.suptitle(f"{pie_label1} ({pie_label2})", fontsize = 'small')
#ax_p.legend(labels = [pie_label1,pie_label2], frameon = False, fancybox = False, bbox_to_anchor=(1,0), loc="lower right", 
#                          bbox_transform=plt.gcf().transFigure)
st.pyplot(fig)
st.pyplot(fig_b)
st.write('\n')
# =============================================================================
# col1, col2 = st.columns([1,1])
# 
# with col1:
#     st.write(pie_label1)
# with col2:
#     st.write(pie_label2)
# =============================================================================

st.pyplot(fig_p)
#st.markdown('<div style="text-align: left;">Hello World!</div>', unsafe_allow_html=True)
#st.markdown('<div style="text-align: right;">Hello World!</div>', unsafe_allow_html=True)

#if latest_is_estimate_flag:
#    st.write('Expected crop yeild')
#else:
#    st.write('Actual crop yeild')
        
  