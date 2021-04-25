import json
from pymongo import MongoClient
import pandas as pd

## Se quiser melhorar, pode fazer scrap no link abaixo, localizar o arquivo CSV da PB, baixar no diretorio CSV ##
#https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8

class Vaccine:

    def load(self):
        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['vaccines']

        db.drop_collection('vaccines')
        db.create_collection('vaccines')

        ##Todas as colunas
        #df = pd.read_csv('./CSV/PB_VACCINES_TESTES.csv', sep=';', engine='python')

        ## Escolhendo as colunas ##
        columns = ['paciente_idade', 'paciente_enumSexoBiologico',
                   'paciente_endereco_nmMunicipio', 'paciente_endereco_uf', 'vacina_dataAplicacao']
        df = pd.read_csv('./CSV/PB_VACCINES.csv', sep=';', engine='python', usecols=columns)

        df = df.rename(columns={'paciente_idade': 'personAge', 'paciente_enumSexoBiologico': 'personGender',
                                'paciente_endereco_nmMunicipio' : 'personAddressLocality',
                                'paciente_endereco_uf' : 'personAddressUF', 'vacina_dataAplicacao' : 'vaccineDate'})

        df["personGender"].replace({"M": "Masculino", "F": "Feminino"}, inplace=True)

        df['vaccineDate'] = pd.to_datetime(df['vaccineDate'], errors='coerce')
        df['vaccineDate'] = df['vaccineDate'].dt.strftime('%Y-%m-%d')

        collection_currency.insert_many(json.loads(df.T.to_json()).values())
        client.close()