import json

import unidecode as unidecode
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Graph:

    def byMonth(self):

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['deaths']

        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {"$substr": ["$deathDate", 0, 7]},
                "count": {"$sum": 1}
            }},
            { "$sort": {"_id": 1}}
        ])

        df_deaths_by_month = pd.DataFrame(list(result))
        df_deaths_by_month = df_deaths_by_month.rename(columns={'_id': 'mesAno', 'count': 'deaths'})
        #print(df_deaths_by_month)

        collection_currency = db['vaccines']
        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {"$substr": ["$vaccineDate", 0, 7]},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ])

        df_vaccine_by_month = pd.DataFrame(list(result))
        df_vaccine_by_month = df_vaccine_by_month.rename(columns={'_id': 'mesAno', 'count': 'vaccines'})
        #print(df_vaccine_by_month)

        df_graph = pd.merge(df_deaths_by_month, df_vaccine_by_month, on='mesAno')
        #print(df_graph)

        plt.xticks(rotation=90)
        plt.scatter(x=df_graph["mesAno"], y=df_graph["deaths"])
        plt.scatter(x=df_graph["mesAno"], y=df_graph["vaccines"])
        classes = ['Deaths', 'Vaccines']
        plt.legend(labels=classes)
        plt.show()

        #fig, axs = plt.subplots(figsize=(12, 4))
        #df_deaths_by_month.groupby(df_deaths_by_month["_id"])["count"].mean().plot(kind='bar', rot=0, ax=axs)
        #plt.xlabel("Meses")
        #plt.ylabel("Deaths")

        #plt.show()

        client.close()