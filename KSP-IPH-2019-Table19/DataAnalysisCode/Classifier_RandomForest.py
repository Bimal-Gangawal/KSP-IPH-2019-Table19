# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 18:06:19 2018

@author: girish.chidananda
"""
import pandas as pd
import MySQLdb
from itertools import chain
import numpy as np
from datetime import datetime,timedelta
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import scikitplot as skplt
import pickle
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,roc_curve,auc
#TripID_Data.drop(['TripId', 'TripCreatedOn', 'CustomerMobile', 
#                  'CustomerEmail','DOJStart', 'DOJEnd','SourceCityName','DestinationCityName', 'DestinationCityId','NumberOfInteraction','NumberOfCalls',
#                  'CallDuration', 'LastCallBackRequestDateTime','IsPeakDOJ','OperatorRatingMax','IsCancelled','NumberOfBusBooked'],axis=1,inplace=True)
class_weight1 = {0 : 1,1: 1000}
X=TripID_Data.drop('IsConverted',axis=1)
y=TripID_Data['IsConverted']
X_train, X_test_trip, y_train, y_test_trip = train_test_split(X, y, test_size= 0.013, random_state=42)
#X_train, X_test_trip, y_train, y_test_trip = train_test_split(X, y, test_size= 0.013)
rfc=RandomForestClassifier(n_estimators=1000,class_weight = class_weight1)
#rfc=RandomForestClassifier(n_estimators=1000)
rfc.fit(X_train,y_train)
Trip_Feature_Importance=pd.DataFrame(rfc.feature_importances_,index=X_test_trip.columns)
# save the model to disk
filename = 'Trip_Finalized_Model.sav'
pickle.dump(rfc, open(filename, 'wb'))
# load the model from disk
startTime = datetime.now()
rfc = pickle.load(open(filename, 'rb'))
#filename.close()
TRIP=rfc.predict_proba(X_test_trip)
print(datetime.now()-startTime)
rfc_pred=rfc.predict(X_test_trip)    
X_test_trip['Actual_Converted_Result']=y_test_trip
X_test_trip['Predicted_probability_result'] = TRIP[:,1].tolist()
X_test_trip.sort_values(by=['Predicted_probability_result'],ascending=False,axis=0,inplace=True)
X_test_trip.reset_index(drop=True,inplace=True)
Trip_classification_RFC=classification_report(y_test_trip,rfc_pred)
Trip_confusion_RFC=confusion_matrix(y_test_trip,rfc_pred)

skplt.metrics.plot_confusion_matrix(y_test_trip,rfc_pred, normalize=True,title='Trip Confusion Matrix')
skplt.metrics.plot_precision_recall_curve(y_test_trip,TRIP,title='Trip Precision-Recall Curve')
skplt.metrics.plot_lift_curve(y_test_trip,TRIP,title='Trip Lift Curve')
skplt.metrics.plot_cumulative_gain(y_test_trip,TRIP,title='Trip Gain Curve')
skplt.metrics.plot_roc_curve(y_test_trip,TRIP,title='Trip ROC Curve')
X_test_trip.to_csv('X_test_trip.csv',index=False)
#skplt.metrics.plot_roc_curve(y_test_trip,TRIP, title='ROC Curves', curves=('each_class'))
