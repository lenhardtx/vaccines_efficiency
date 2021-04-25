import json
from pymongo import MongoClient
import pandas as pd

#https://opendatasus.saude.gov.br/dataset/bd-srag-2021

class Case:

    def load(self):
        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['cases']

        db.drop_collection('cases')
        db.create_collection('cases')

        ##Todas as colunas
        #df = pd.read_csv('./CSV/BR_CASES_TESTES.csv', sep=';', engine='python')

        ## Escolhendo as colunas ##
        columns = ['NU_IDADE_N', 'CS_SEXO',
                   'ID_MN_RESI', 'SG_UF', 'DT_NOTIFIC']

        df = (pd.read_csv('./CSV/BR_CASES.csv', sep=';', engine='python', usecols=columns) [lambda x: x['SG_UF'] == 'PB'])

        df = df.rename(columns={'NU_IDADE_N': 'personAge', 'CS_SEXO': 'personGender',
                                'ID_MN_RESI' : 'personAddressLocality',
                                'SG_UF' : 'personAddressUF', 'DT_NOTIFIC' : 'caseDate'})

        df["personGender"].replace({"M": "Masculino", "F": "Feminino"}, inplace=True)
        df['caseDate'] = pd.to_datetime(df['caseDate'], format='%d/%m/%Y')

        df['caseDate'] = df['caseDate'].astype(str)
        #print(df)

        collection_currency.insert_many(json.loads(df.T.to_json()).values())
        client.close()