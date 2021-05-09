from matplotlib import pyplot as plt
from pymongo import MongoClient
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
#import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

class Predict:

    def start(self):

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection = db['deaths']

        result = collection.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {"_id": {"$substr": ["$deathDate", 0, 10]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])

        df_deaths_by_day = pd.DataFrame(list(result))
        df_deaths_by_day = df_deaths_by_day.rename(columns={'_id': 'day', 'count': 'deaths'})
        df_deaths_by_day = df_deaths_by_day[df_deaths_by_day["day"].str.contains("2021")==True]

        collection = db['vaccines']
        result = collection.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {"_id": {"$substr": ["$vaccineDate", 0, 10]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])

        df_vaccines_by_day = pd.DataFrame(list(result))
        df_vaccines_by_day = df_vaccines_by_day.rename(columns={'_id': 'day', 'count': 'deaths'})
        df_vaccines_by_day = df_vaccines_by_day[df_vaccines_by_day["day"].str.contains("2021") == True]

        df_predict = pd.merge(df_deaths_by_day, df_vaccines_by_day, how='left', on='day')
        df_predict = df_predict.rename(columns={'deaths_x': 'deaths', 'deaths_y': 'vaccines'})
        df_predict['deaths'] = df_predict['deaths'].fillna(0).astype(int)
        df_predict['vaccines'] = df_predict['vaccines'].fillna(0).astype(int)



        df = df_predict
        #df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
        #print(df_predict)

        plt.figure(figsize=(18, 9))
        plt.plot(range(df.shape[0]), (df['vaccines']/ df['deaths']))
        plt.xticks(range(0, df.shape[0], 5), df['day'].loc[::5], rotation=90)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Média by Vaccines / Deaths', fontsize=12)
        plt.show()