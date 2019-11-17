# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:05:53 2019

@author: girish.chidananda
"""

import pandas as pd
import glob

list_file = glob.glob('*.xlsx')

for name in list_file[1:]:
    
    df = pd.read_excel(name)
    nunique = df.apply(pd.Series.nunique)
    cols_to_drop = nunique[nunique == 1].index
    df.drop(cols_to_drop, axis=1,inplace=True)
    df.dropna(axis=1, how='all',inplace=True)
    filename='.\\Cleaned\\'+name.split(".")[0]+'.csv'
    print(filename)
    df.to_csv(filename)


0=integer   
1- Categorical
2:Datetime
3:Object
4: Logical
tbl_tr_accident_report

{'Unit_ID':1, 'Crime_No':0, 'Accident_Classification':1,
       'Severity':1, 'Collision_Type':1, 'Accident_Spot':1, 'Accident_Location':1,
       'NoOfVehicle_Involved':0, 'Junction_Control':1, 'Road_Character':1,
       'Road_Type':1, 
       'Surface_Type':1, 'Surface_Condition':1, 'Road_Condition':1, 'weather':1,
       'Location_Type':1, 'Main_Cause':1, 'Hit_Run':1,
       'UserID':0,
       'Actual_DateOf_Occurance':2,
        'Lane_Type':1,
       'Road_Markings':1, 'Spot_Conditions':1,
       'Highway_Patrol_No':1, 'Checked':4,
       'Side_Walk':1, 'NoOf_Animal_Injured':1, 'NoOf_Animal_Killed':1,
       'Accident_Location_id':1, 
        'SpeedLimit':1, 'RoadJunction':1,
       'Accident_spotb':1, 'Footpath':1, 'Collision_Typeb':1}





TBL_TR_Accident_Casualties

{'Person_ID':0, 'Crime_No':1, 'Unit_ID':1, 'Registration_Number':3,
       'Casualty_Type':1, 'Injury_Type':1, 'SeatBelt':1, 'Helmet':1,
       'Passenger_Position':1, 'Hit_by':1, 'Padestrian_Caused':0,
       'Padestrian_Action':1, 'Padestrian_Location':1, 
       'Head_Injury':4}

TBL_TR_Accident_Driver

{'Registration_Number':3, 'Crime_No':0, 'Person_ID':0, 
       'Injury_Type':1, 'Licence':1, 'Licence_Type':1, 
       'Licence_Valid_Date':2, 'Possesing_Badges':1,
       'Driver_Error':1, 'Alcohol_Drugs':1, 'Helmet':1,
       'SeatBelt':1, 'Unit_ID':1, 'UserID':0, }

TBL_TR_Person_Details
{'Person_ID':0, 'Unit_ID':1, 'Crime_No':0, 'City_ID':1, 'State_ID':1, 
       'sex':1, 'Age':0, 'Qualification':1, 'Occupation_ID':1, 'Person_Type':1,
       'IsCompany_Paid':0}

tbl_CR_Victim_Info

{'Victim_ID':0, 'Unit_ID':1, 'FIR_ID':0, 'Arr_ID':0, 'Injury_type':1,
       'Major_Cause':1, 'Minor_Cause':1,'IsPoliceOnDuty':1, 'IsSuicide':1,
        'UserID':0}

tbl_CR_Arr_Person_Details
{'Arr_ID':0, 'Unit_ID':1, 'FIR_ID':0, 'Crime_No':0, 
       'Type':1, 'Sex':0, 'age':1,
       'Nationality':1, 'Occupation':1,  'UserID':0, 
       'ISPolice':1, 'Rank':1}

TR_Accident_Vehicle_Master
{'Unit_ID':1, 'Registration_Number':3, 'Vehicle_Type':1,
       'vehicle_Make':1, 'Vehicle_Model':1,
       'Vehicle_Load':1, 
       'Fuel_Type':1, 
       'IsPoliceVehicle':4, 'IsGov_Vehicle':4, 'UserID':0,
       'Vehicle_Sub_Type':1, 
       'TrafficViolation':1, 
       'MechanicalFailure':1}

TBL_TR_Offence_details
{ 'Unit_ID':1, 'Offence_Place':1, 'Offence_Date':2,
       'Registration_Number':0, 'Vehicle_Type_ID':1, 'Owner_PersonID':0,
       'Driver_PersonID':1, 
        'UserID':0, 'Flag':1,
       'Traffic_Point':1, 
       'Under_Aged':1}


tbl_CR_FIR_Details
{'FIR_ID':0, 'Unit_ID':1, 'Crime_No':0,
        'FIR_Category':1,   'GD_No':1, 'Beat_ID':1,  'UserID':0}


df=pd.merge(tbl_tr_accident_report,tbl_CR_FIR_Details,left_on=['Crime_No','Unit_ID'],right_on=['FIR_ID','Unit_ID'],how='left')
del df['Crime_No_y']
df.rename(columns={'Crime_No_x':'Crime_No'},inplace=True)
del tbl_tr_accident_report
del tbl_CR_FIR_Details
df=pd.merge(df,TBL_TR_Accident_Driver,left_on=['Crime_No'],right_on=['Crime_No'],how='left')
del TBL_TR_Accident_Driver
