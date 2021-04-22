import json
from pymongo import MongoClient
import pandas as pd

#https://superset.plataformatarget.com.br/superset/dashboard/microdados/

class Death:

    def load(self):

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['deaths']

        db.drop_collection('deaths')
        db.create_collection('deaths')

        ##Todas as colunas
        df = pd.read_csv('./CSV/PB_DEATHS.csv', sep=',', engine='python')

        ## Escolhendo as colunas
        # columns = ['paciente_idade', 'paciente_racaCor_valor'];
        # df = pd.read_csv('PB.csv', sep=';', engine='python', usecols=columns)

        collection_currency.insert_many(json.loads(df.T.to_json()).values())
        client.close()