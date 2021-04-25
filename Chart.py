import pandas as pd
from flask import Flask, Markup, render_template
from pymongo import MongoClient


class Chart:

    def start(self):

        app = Flask(__name__)

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['deaths']

        result = collection_currency.aggregate([
            # Group the documents and "count" via $sum on the values
            {"$group": {
                "_id": {"$substr": ["$deathDate", 0, 7]},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ])

        df_deaths_by_month = pd.DataFrame(list(result))
        df_deaths_by_month = df_deaths_by_month.rename(columns={'_id': 'mesAno', 'count': 'deaths'})
        # print(df_deaths_by_month)

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
        # print(df_vaccine_by_month)

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
        # print(df_cases_by_month)

        df_graph = pd.merge(df_deaths_by_month, df_vaccine_by_month, on='mesAno')
        df_graph = pd.merge(df_graph, df_cases_by_month, on='mesAno')

        pc_vaccines = []
        total_vaccines = 0
        for value in df_graph["vaccines"]:
            total_vaccines = total_vaccines + value
            pc_vaccines.append(total_vaccines / 4000000 * 100)

        df_graph["pc_vaccines"] = pc_vaccines
        print(df_graph)

        labels = df_graph["mesAno"]

        values = [df_graph["pc_vaccines"],df_graph["cases"],df_graph["deaths"]]

        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

        @app.route('/line')
        def line():
            line_labels=labels
            line_values=values
            return render_template('teste.html', title='Vaccines Effectivity - State of Paraíba - Brazil', max=100, labels=line_labels, values=line_values)

        app.run(debug=False, host='localhost', port=8080)