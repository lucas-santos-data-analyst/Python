from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from requests.exceptions import SSLError
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from ibge.localidades import *
import time

#id      indicador
#29171	 População estimada [2021]
#25207	 População no último censo [2010]
#29168	 Densidade demográfica [2010]
#29765	 Salário médio mensal dos trabalhadores formais [2020]
#29763	 Pessoal ocupado [2020]
#60036	 População ocupada [2020]
#60037	 Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo [2010]
#47001	 PIB per capita [2019]
#60048	 Percentual das receitas oriundas de fontes externas [2015]
#30255	 Índice de Desenvolvimento Humano Municipal (IDHM) [2010]
#28141	 Total de receitas realizadas [2017]
#29749	 Total de despesas empenhadas [2017]
#91251	 Hierarquia urbana [2018]
#91249	 Região de Influência [2018]
#91247	 Região intermediária [2021]
#91245	 Região imediata [2021]
#87350	 Mesorregião [2021]
#87529	 Microrregião [2021]

#configurações do webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
navegador = webdriver.Chrome(options=options)

id_relatorio = '29168'

uf_br = ['ro','ac','am','rr','pa','ap','to','ma','pi','ce','rn','pb','pe','al','se','ba','mg','es','rj','sp','pr','sc','rs','ms','mt','go']

navegador.get('https://cidades.ibge.gov.br/brasil/sintese/pr?indicadores='+id_relatorio)

fonte = navegador.find_element(By.ID , 'municipios')
time.sleep(2)
tabela = pd.DataFrame([fonte.find_elements(By.TAG_NAME , 'th')[0].text,'UF',fonte.find_elements(By.TAG_NAME , 'th')[2].text]).transpose()
arquivo = fonte.find_elements(By.TAG_NAME , 'th')[2].text
print(arquivo)
for uf in uf_br:
    url = 'https://cidades.ibge.gov.br/brasil/sintese/'+uf+'?indicadores='+id_relatorio
    print(url)
    navegador.get(url)

    fonte = navegador.find_element(By.ID , 'municipios')
    time.sleep(2)
    
    base = [fonte.find_elements(By.TAG_NAME , 'tbody')[0].find_elements(By.TAG_NAME , 'td')[0].text,uf.upper(),fonte.find_elements(By.TAG_NAME , 'tbody')[0].find_elements(By.TAG_NAME , 'td')[2].text]
    df = pd.DataFrame(base).transpose()

    x = 1
    while True:
        dados = pd.DataFrame([fonte.find_elements(By.TAG_NAME , 'tbody')[x].find_elements(By.TAG_NAME , 'td')[0].text,uf.upper(),fonte.find_elements(By.TAG_NAME , 'tbody')[x].find_elements(By.TAG_NAME , 'td')[2].text]).transpose()
        x+=1
        df = pd.concat([df,dados]).dropna()
        if x == len(fonte.find_elements(By.TAG_NAME , 'tbody')):
            break
    tabela = pd.concat([tabela,df])
navegador.close()

tabela.to_csv(arquivo+'.csv')
print("Concluído")
