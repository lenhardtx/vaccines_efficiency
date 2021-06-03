import pandas
import pandas as pd
from flask import Flask, Markup, render_template
from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

class Chart:

    def start(self):

        app = Flask(__name__)

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['deaths']

        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {"_id": {"$substr": ["$deathDate", 0, 7]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])

        df_deaths_by_month = pd.DataFrame(list(result))
        df_deaths_by_month = df_deaths_by_month.rename(columns={'_id': 'mesAno', 'count': 'deaths'})
        #print(df_deaths_by_month)

        collection_currency = db['vaccines']
        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            #{"$match": {"$vaccineDose": "1ª Dose"}},
            {"$match": {"vaccineDose": "1"}},
            {"$group": {"_id": {"$substr": ["$vaccineDate", 0, 7]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])

        df_vaccine1dose_by_month = pd.DataFrame(list(result))
        df_vaccine1dose_by_month = df_vaccine1dose_by_month.rename(columns={'_id': 'mesAno', 'count': 'qt_vaccines1dose'})
        #print(df_vaccine1dose_by_month)

        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$match": {"vaccineDose": "2"}},
            {"$group": {"_id": {"$substr": ["$vaccineDate", 0, 7]}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])

        df_vaccine2dose_by_month = pd.DataFrame(list(result))
        df_vaccine2dose_by_month = df_vaccine2dose_by_month.rename(columns={'_id': 'mesAno', 'count': 'qt_vaccines2dose'})
        #print(df_vaccine2dose_by_month)

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

        df_graph = pd.merge(df_deaths_by_month, df_vaccine1dose_by_month, on='mesAno')
        df_graph = pd.merge(df_graph, df_vaccine2dose_by_month, on='mesAno')
        df_graph = pd.merge(df_graph, df_cases_by_month, on='mesAno')

        pc_vaccines1dose = []
        total_vaccines1dose = 0
        for value in df_graph["qt_vaccines1dose"]:
            total_vaccines1dose = total_vaccines1dose + value
            pc_vaccines1dose.append(total_vaccines1dose / 4000000 * 100)

        df_graph["pc_vaccines1dose"] = pc_vaccines1dose

        pc_vaccines2dose = []
        total_vaccines2dose = 0
        for value in df_graph["qt_vaccines2dose"]:
            total_vaccines2dose = total_vaccines2dose + value
            pc_vaccines2dose.append(total_vaccines2dose / 4000000 * 100)

        df_graph["pc_vaccines2dose"] = pc_vaccines2dose

        pandas.set_option('display.max_columns', 7)
        print(df_graph)

        labels = df_graph["mesAno"]

        values = [df_graph["pc_vaccines1dose"],df_graph["pc_vaccines2dose"],df_graph["deaths"],df_graph["cases"]]

        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

        @app.route('/vaccines')
        def line():
            line_labels=labels
            line_values=values
            return render_template('vaccines.html', title='Vaccines - State of Paraíba - Brazil', max=100, labels=line_labels, values=line_values)

        app.run(debug=False, host='localhost', port=8080)