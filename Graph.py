import json

import unidecode as unidecode
from mpl_toolkits.axes_grid1 import host_subplot
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes

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

        collection_currency = db['cases']
        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {"$substr": ["$caseDate", 0, 7]},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ])

        df_cases_by_month = pd.DataFrame(list(result))
        df_cases_by_month = df_cases_by_month.rename(columns={'_id': 'mesAno', 'count': 'cases'})
        #print(df_cases_by_month)

        df_graph = pd.merge(df_deaths_by_month, df_vaccine_by_month, on='mesAno')
        df_graph = pd.merge(df_graph, df_cases_by_month, on='mesAno')

        pc_vaccines = []
        total_vaccines = 0
        for value in df_graph["vaccines"]:
            total_vaccines = total_vaccines + value
            pc_vaccines.append(total_vaccines / 4000000 * 100)

        df_graph["pc_vaccines"] = pc_vaccines
        print(df_graph)

        fig = plt.figure()

        host = fig.add_axes([0.15, 0.1, 0.65, 0.8], axes_class=HostAxes)
        par1 = ParasiteAxes(host, sharex=host)
        par2 = ParasiteAxes(host, sharex=host)
        host.parasites.append(par1)
        host.parasites.append(par2)

        host.axis["right"].set_visible(False)

        par1.axis["right"].set_visible(True)
        par1.axis["right"].major_ticklabels.set_visible(True)
        par1.axis["right"].label.set_visible(True)

        par2.axis["right2"] = par2.new_fixed_axis(loc="right", offset=(60, 0))

        p1, = host.plot(df_graph["mesAno"], df_graph["pc_vaccines"], label="% Vaccines")
        p2, = par1.plot(df_graph["mesAno"], df_graph["cases"], label="Cases")
        p3, = par2.plot(df_graph["mesAno"], df_graph["deaths"], label="Deaths")

        #host.set_xlim(0, 2)
        #host.set_ylim(0, 2)
        par1.set_ylim(0, 5000)
        par2.set_ylim(1, 1100)

        host.set_xlabel("Period")
        host.set_ylabel("% Vaccines")
        par1.set_ylabel("Cases")
        par2.set_ylabel("Deaths")

        host.legend()

        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
        par2.axis["right2"].label.set_color(p3.get_color())

        plt.show()

        client.close()