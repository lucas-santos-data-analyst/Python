from __future__ import print_function

import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import psycopg2
import time
from datetime import datetime
from datetime import time as t
from datetime import date
import sys

# caso as bibliotecas da api do google não tenha instalado
# Executar no terminal:
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

#sys.stdout = open('saida_bc.txt', 'w')

query = '''

QUERY A SER EXECUTADA

;'''

# Se modificar esses escopos, exclua o arquivo token.json.
# Scopes definem os níveis de acesso portanto precisa-se tirar da linha abaixo
# o cod .readonly caso precise ter acesso de escrita no arquivo
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Planilha (ID) que deseja editar e intervalo
SAMPLE_SPREADSHEET_ID = '' # ID DA PLANILHA

while True:
    hr_atual= datetime.time(datetime.today()).strftime("%H:%M:%S")
    hr_final= t(22,10,0).strftime("%H:%M:%S")

    if hr_atual >= hr_final:
        print('Parando processos e encerrando, horário excedido')
        break

    conn = psycopg2.connect(
        host='', 
        user='', 
        password='', 
        port=, 
        database='')
    cursor = conn.cursor()
    print("Iniciando consulta no banco de dados")
    a = datetime.now()
    print(a)
    try:
        cursor.execute(query)
        b = datetime.now()
        print(b-a)
        consulta_sql = cursor.fetchall()
    except BaseException as error:
        conn.close()
        time.sleep(60)
        cursor2 = conn.cursor()
        cursor2.execute(query)
        consulta_sql = cursor2.fetchall()
        pass
    conn.close()



    def main():
        
        token = (r'C:\Users\lucas.adriano\Documents\token_gsheets\token.json')
        credentials = (r'C:\Users\lucas.adriano\Documents\token_gsheets\credentials.json')
        
        print("Logando em conta e atualizando GSheets")
        creds = None
        # O arquivo token.json armazena os tokens de acesso e atualização do usuário, e é
        # criado automaticamente quando o fluxo de autorização é concluído para o primeiro
        # tempo.
        if os.path.exists(token):
            creds = Credentials.from_authorized_user_file(token , SCOPES)
        # Se não houver credenciais (válidas) disponíveis, permita que o usuário faça login.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            # Salve as credenciais para a próxima execução
            with open(token, 'w') as token:
                token.write(creds.to_json())
            
            ## até aqui o código acima serve pra fazer o "login" no google sheets

        service = build('sheets', 'v4', credentials=creds)

        # Chamar a API do sheets
        sheet = service.spreadsheets()
        # adicionar/editar valores no Google Sheets
        print("Deletando dados da planilha")
        clear = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='BASE DE DADOS!A2:Y').execute()
        time.sleep(5)
        print("Convertendo os dados da consulta para formato exigido pela planilha")
        values_list = [list(row) for row in consulta_sql]
        values_list = [[str(value) if isinstance(value, date) else value for value in row] for row in values_list]
        time.sleep(5)
        print("Incluindo dados atualizados")
        result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range='BASE DE DADOS!A2', 
            valueInputOption="RAW",
            body=dict(
                majorDimension='ROWS',
                values=values_list
                )
            ).execute()
        time.sleep(5)
        
        


    if __name__ == '__main__':
        main()

    print("Operação Concluída")
    b = datetime.now()
    print(b)
    print("Tempo de execução", b-a)
    print('----------------------------------')
    time.sleep(600)
