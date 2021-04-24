import json

import unidecode as unidecode
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

#https://superset.plataformatarget.com.br/superset/dashboard/microdados/

class Death:

    def remove_accents(a):
        return unidecode.unidecode(a.decode('utf-8'))

    def load(self):

        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['deaths']

        db.drop_collection('deaths')
        db.create_collection('deaths')

        ##Todas as colunas
        #df = pd.read_csv('./CSV/PB_DEATHS.csv', sep=',', engine='python')

        ## Escolhendo as colunas
        columns = ['Idade', 'Sexo', 'Município de Residência', 'Data do Óbito']
        df = pd.read_csv('./CSV/PB_DEATHS.csv', sep=',', engine='python', usecols=columns)

        df = df.rename(columns={'Idade': 'personAge', 'Sexo': 'personGender',
                                'Município de Residência': 'personAddressLocality',
                                'Data do Óbito': 'deathDate'})

        df['personAddressUF'] = 'PB'
        df['personAddressLocality'] = df['personAddressLocality'].str.upper()

        ## Ver se tem como melhorar isso ##
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ç", "C")

        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ã", "A")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Õ", "O")

        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Â", "A")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ê", "E")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Î", "I")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ô", "O")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Û", "U")

        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Á", "A")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"É", "E")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Í", "I")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ó", "O")
        df['personAddressLocality'] = df['personAddressLocality'].str.replace(u"Ú", "U")

        collection_currency.insert_many(json.loads(df.T.to_json()).values())

        client.close()