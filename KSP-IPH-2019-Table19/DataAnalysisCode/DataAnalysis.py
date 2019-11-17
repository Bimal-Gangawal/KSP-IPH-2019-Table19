#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:27:15 2019

@author: ubuntu
"""

import pandas as pd
import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import os


ProcessedAccidentData = pd.read_csv('ClusterDf.csv', index_col=False)
del ProcessedAccidentData['Unnamed: 0']
ProcessedAccidentData['Cluster_Denominator'] = ProcessedAccidentData['Cluster_Score'] / (365*4.5)
ProcessedAccidentData['Cluster_Denominator'] = 1/ProcessedAccidentData['Cluster_Denominator']

master = pd.read_csv('Master.csv', index_col=False)
del master['Unnamed: 0']

Prediction_Data = pd.read_csv('Prediction_Data.csv', index_col=False)
del Prediction_Data['Unnamed: 0']

unitid_latlon_map = pd.read_csv('unitid_latlon_map.csv', index_col=False)
unitid_latlon_map = unitid_latlon_map[['Unit_ID', 'Unit_Name']]

area_map = pd.read_csv('area_map.csv', index_col=False)

ProcessedAccidentData = pd.merge(ProcessedAccidentData, unitid_latlon_map, on=['Unit_ID'], how='left')
ProcessedAccidentData = pd.merge(ProcessedAccidentData, area_map, on=['lat', 'long'], how='left')
ProcessedAccidentData = pd.merge(ProcessedAccidentData, Prediction_Data, on=['Unit_ID'], how='left')

columns_to_clean = ['Collision_Type', 'Accident_Spot', 'Junction_Control',
       'Road_Character', 'Road_Type', 'Surface_Type', 'Surface_Condition',
       'Road_Condition', 'weather', 'Main_Cause', 'Hit_Run']

ignore_id = [6525, 6093, 20104, 6068, 6075, 6513, 6080, 6083, 6513, 6521,
             6096, 6095, 6811, 6498, 6109, 6501, 6733, 6520, 11050, 6520,
             6518, 6129, 6500, 6517, 6923, 6522, 6516]

cleaned_master = pd.DataFrame()
for column in columns_to_clean:
    col_val = ProcessedAccidentData[column].unique()
    col_val_df = master[master.ID.isin(col_val)]
    col_val_df = col_val_df[~(col_val_df['ID'].isin(ignore_id))]
    cleaned_master = cleaned_master.append(col_val_df)

cleaned_master_dict = dict(zip(cleaned_master.ID, cleaned_master.Description))
for column in columns_to_clean:
    ProcessedAccidentData = ProcessedAccidentData.replace({column: cleaned_master_dict})

ProcessedAccidentData = ProcessedAccidentData[~(ProcessedAccidentData.area_name.isna())]

inferential_columns = ['Collision_Type', 'Accident_Spot', 'Junction_Control', 
                       'Road_Character', 'Road_Type', 'Surface_Type', 
                       'Surface_Condition', 'Road_Condition', 'weather', 
                       'Main_Cause', 'Hit_Run']
result_dict = {}
for key, group in ProcessedAccidentData.groupby('Unit_ID'):
    group = group.sort_values('Cluster')
    unit_data = {'Unit_Name': list(group['Unit_Name'])[0]}
    unit_data.update({'Unit_Name': list(group['Unit_Name'])[0]})
    unit_data.update({'Unit_Name': list(group['Unit_Name'])[0]})
    Unit_Details = []
    for sub_key, sub_group in group.groupby('Cluster'):
        infer_sub_data = {}
        infer_sub_data_cnt = {}
        infer_data = {'area_address': list(sub_group['area_name'])[0]}
        for columns in inferential_columns:
            sub_group_temp = sub_group[~sub_group[columns].isin(ignore_id)]
            if sub_group_temp.empty:
#                infer_sub_data.update({columns: {'0':0}})
#                infer_sub_data_cnt.update({columns: {'0':0}})
                continue
            value_cnt = dict(sub_group_temp[columns].value_counts(normalize=True).mul(100).round(2).nlargest(5))
            value_cnt_cnt = sub_group_temp[columns].value_counts().nlargest(5).to_json()
            infer_sub_data.update({columns: value_cnt})
            infer_sub_data_cnt.update({columns: value_cnt_cnt})
        infer_data.update({'Inference': infer_sub_data})
        infer_data.update({'Inference_cnt': infer_sub_data_cnt})
        Unit_Details.append(infer_data)
    unit_data.update({'Unit_Details': Unit_Details})
    result_dict.update({key: unit_data})

result_dict_json = json.dumps(result_dict).replace('NaN', '')
with open('result.json', 'w') as fp:
    fp.write(result_dict_json)

#descriptive_result = ProcessedAccidentData[['Unit_ID', 'Unit_Name']].groupby('Unit_ID').size().reset_index(name='count')
#descriptive_result['count'] = round((descriptive_result['count'] / descriptive_result['count'].sum()) * 100, 2)
#descriptive_result = descriptive_result.sort_values(by='count', ascending=False)
#
#def millions(x, pos):
#    'The two args are the value and tick position'
#    return '$%1.1fM' % (x * 1e-6)
#
#Unit_ID = descriptive_result['Unit_ID']
#count = descriptive_result['count']
#x = np.arange(len(count))
#
#formatter = FuncFormatter(millions)
#fig, ax = plt.subplots()
#ax.yaxis.set_major_formatter(formatter)
#plt.figure(figsize=(25,10))
#bar_plot = plt.bar(x, count)
#plt.xticks(x,Unit_ID, rotation='vertical')
#def autolabel(rects):
#    for idx,rect in enumerate(bar_plot):
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                Unit_ID[idx],
#                ha='center', va='bottom', rotation=0)
#autolabel(bar_plot)
#
#plt.title('Unit wise accidents',  fontsize=22)
#plt.xlabel('accident in %',  fontsize=18)
#plt.ylabel('Unit_Name',  fontsize=18)
#plt.savefig(os.path.join('descriptive_result.png'), dpi=300, format='png', bbox_inches='tight')
#plt.show()