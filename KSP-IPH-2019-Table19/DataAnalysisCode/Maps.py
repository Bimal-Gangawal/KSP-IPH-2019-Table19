# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 09:43:53 2019

@author: girish.chidananda
"""
import requests
for index,row in bangalore_data.iterrows():
    try:
        address = row['Unit_Name']
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyA5qyM3gHn92xqV3Gnbenq7gOHQQwjufos".format(address)
        resp = requests.get(url).json()
        row['lat'] = resp['results'][0]['geometry']['location']['lat']
        row['long'] = resp['results'][0]['geometry']['location']['lng']
        with_lat_long = with_lat_long.append(row,ignore_index=True)
    except Exception as e:
        print(e)

df=[]