import json

import requests as requests
from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

## Se quiser melhorar, pode fazer scrap no link abaixo, localizar o arquivo CSV da PB, baixar no diretorio CSV ##
#https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8

class Vaccine:

    def downloadCSV(self):
        print("Downloading CSV with Vaccines of state Brazil/PB...")
        html_page = urllib.request.urlopen("https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao/resource/ef3bd0b8-b605-474b-9ae5-c97390c197a8")
        soup = BeautifulSoup(html_page, "html.parser")
        for link in soup.findAll('a'):
            if "DPB" in link.get('href'):
                r = requests.get(link.get('href'), allow_redirects=True)
                open('./CSV/PB_VACCINES.csv', 'wb').write(r.content)
                #print(link.get('href'))

    def load(self):
        print("Loading CSV with Vaccines of state Brazil/PB")
        client = MongoClient('localhost', 27017)
        db = client['covidao']
        collection_currency = db['vaccines']

        db.drop_collection('vaccines')
        db.create_collection('vaccines')

        ##Todas as colunas
        #df = pd.read_csv('./CSV/PB_VACCINES_TESTES.csv', sep=';', engine='python')

        ## Escolhendo as colunas ##
        columns = ['paciente_idade', 'paciente_enumsexobiologico',
                   'paciente_endereco_nmmunicipio', 'paciente_endereco_uf', 'vacina_dataaplicacao', 'vacina_descricao_dose']
        df = pd.read_csv('./CSV/PB_VACCINES.csv', sep=';', engine='python', usecols=columns)

        df = df.rename(columns={'paciente_idade': 'personAge', 'paciente_enumsexobiologico': 'personGender',
                                'paciente_endereco_nmmunicipio' : 'personAddressLocality',
                                'paciente_endereco_uf' : 'personAddressUF', 'vacina_dataaplicacao' : 'vaccineDate',
                                'vacina_descricao_dose' : 'vaccineDose'})

        df['vaccineDose'] = df['vaccineDose'].str.lstrip()
        df['vaccineDose'] = df['vaccineDose'].str.slice(stop=1)

        df["personGender"].replace({"M": "Masculino", "F": "Feminino"}, inplace=True)

        df['vaccineDate'] = pd.to_datetime(df['vaccineDate'], errors='coerce')
        df['vaccineDate'] = df['vaccineDate'].dt.strftime('%Y-%m-%d')

        collection_currency.insert_many(json.loads(df.T.to_json()).values())
        client.close()