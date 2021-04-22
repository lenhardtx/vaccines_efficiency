import json
from pymongo import MongoClient
import pandas as pd

#https://s3-sa-east-1.amazonaws.com/ckan.saude.gov.br/PNI/vacina/uf/2021-04-17/uf%3DPB/part-00000-f22ba8ea-5049-48ca-8f82-c271f5841875.c000.csv

class Vaccine:

    def load(self):
        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['vaccines']

        db.drop_collection('vaccines')
        db.create_collection('vaccines')

        ##Todas as colunas
        df = pd.read_csv('./CSV/PB_VACCINES.csv', sep=';', engine='python')

        ## Escolhendo as colunas
        #columns = ['paciente_idade', 'paciente_racaCor_valor'];
        #df = pd.read_csv('PB.csv', sep=';', engine='python', usecols=columns)

        collection_currency.insert_many(json.loads(df.T.to_json()).values())
        client.close()