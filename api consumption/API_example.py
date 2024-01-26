# API Leveduca
import requests as r
import pandas as pd

# Variáveis para api
url_auth = "site para a"
key = {"email":"email","password":""}
url_consult = "https://studio-backend.leveduca.com.br/api/reflex/relatorio/certificados"

response = r.post(url_auth, json=key)
token = response.json()["access_token"]
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

response_consult = r.get(url_consult, headers = headers)

consulta1 = response_consult.json()['Academy']
consulta2 = response_consult.json()['knowledge']

dados1 = pd.DataFrame(consulta1)
dados2 = pd.DataFrame(consulta2)

certificados = pd.concat([dados1,dados2], ignore_index = True)

certificados.to_excel(r"C:\Users\User\Desktop\dados.xlsx", index = False)
