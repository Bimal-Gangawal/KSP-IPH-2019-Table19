# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 01:13:14 2019

@author: girish.chidananda
"""

import pandas as pd


#['Unit_ID':'Primary','
# 'Accident_Classification':effect
#    , 'Severity':Effect,
#    
#    
#       'Collision_Type'-Cause
#       , 'Accident_Spot':-Cause
#       'NoOfVehicle_Involved',-Cause
#       'Junction_Control'-Cause
#       , 'Road_Character',-Cause
#       'Road_Type'-Cause
#       , 'Surface_Type'-Cause
#       , 'Surface_Condition',-Cause
#       'Road_Condition',-Cause
#       'weather'-Cause, 
#       'Main_Cause'-Cause
#       , 'Hit_Run'-Cause
#       'Actual_DateOf_Occurance',-Result
#       'Lane_Type'-Cause,
#       'Road_Markings',-Cause
#       'Spot_Conditions', -Cause
#       'NoOf_Animal_Injured'-Effect, 
#       'NoOf_Animal_Killed'-Effect
#       'Accident_Location_id'-Cause
#       'SpeedLimit'-Cause
#       'RoadJunction'-Cause       
#        'Beat_ID',-Primary
#    'Casualty_Type'-Effect
#    , 'Injury_Type',-Effect
#       'SeatBelt'-Cause
#       'Helmet'-Cause 
#       'Padestrian_Caused'-Cause
#       
#       , 'Padestrian_Action',-Cause
#       'Padestrian_Location'-Cause
#       
#         'Age'-Extra,
# 'Holiday'-Cause, 
# 'lat':Primary, 
# 'long':Primary]


#Primary_Columns=['Unit_ID','Beat_ID','lat','long']
CauseColumns=['Collision_Type','Accident_Spot','NoOfVehicle_Involved','Junction_Control',
              'Road_Character','Road_Type','Surface_Type','Surface_Condition','Road_Condition',
              'weather','Main_Cause','Hit_Run','Holiday']
df=combined_df           
df['lat'] = df['lat'].round(4)
df['lat'] = df['lat'].round(4)
MasterColumns=['Collision_Type','Accident_Spot','Junction_Control',
              'Road_Character','Road_Type','Surface_Type','Surface_Condition',
              'Road_Condition',
              'weather','Main_Cause','Hit_Run']
ClusterDf_Predict=pd.DataFrame()
for Unit_ID in combined_df.Unit_ID.unique():
    perge = df[df.Unit_ID==Unit_ID]
    bar = perge.groupby(['lat','long']).size().sort_values().reset_index().sort_values(0,ascending=False)
    bar = bar[bar[0]>5]
    bar.rename(columns={0:'Cluster_Score'},inplace=True)
    bar['Unit_ID']=Unit_ID
    bar['Cluster']=range(0,bar.shape[0])
    perge=pd.merge(perge,bar,on=['lat', 'long','Unit_ID'],how='inner')
    for Cluster in perge.Cluster.unique():
        Cluster_perge=perge[perge.Cluster==Cluster]
        Cluster_perge.fillna(-1,inplace=True)
        ClusterDf_Predict=ClusterDf_Predict.append(Cluster_perge)

for Column_M in MasterColumns:
    ClusterDf_Predict = ClusterDf_Predict.replace({Column_M: Master_filtered_dict})

ClusterDf_Predict.sort_values(by=['Unit_ID','Cluster_Score'],ascending=[True,False],inplace=True)

for Column_M in ['Unit_ID','Main_Cause',  'weather']:
    df = df.replace({Column_M: Master_filtered_dict})