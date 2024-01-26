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

#configurações do webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
navegador = webdriver.Chrome(options=options)

url= 'https://cidades.ibge.gov.br/brasil/sp/presidente-prudente/panorama'

lista_cidades = pd.DataFrame(Municipios().getDados()).query('uf=="SP" or uf=="PR"').reset_index().drop(['index'], axis = 1) 

linha = 0
linha_final = lista_cidades.index.max()


df = pd.DataFrame([['Muicipio'],['UF'],['População Estimada']]).transpose()


while True:
    #print(lista_cidades['nome'].loc[linha])
    #print(lista_cidades['uf'].loc[linha])
    navegador.get('https://cidades.ibge.gov.br/brasil/'+lista_cidades['uf'].loc[linha].lower()+'/'+lista_cidades['nome'].loc[linha].lower().replace(" ","-").replace("'","").replace("ç","c").replace("ã","a").replace("â","a").replace("õ","o").replace("ô","o").replace("ó","o").replace("í","i").replace("á","a").replace("é","e").replace("ê","e").replace("ú","u")+'/pesquisa/23/47427')
    time.sleep(2)
    teste = navegador.find_element(By.XPATH, '//*[@id="container"]/div[3]/pesquisa/div/pesquisa-tabela/table/tr[2]/td[2]').text
    tabela = pd.DataFrame([[lista_cidades['nome'].loc[linha]],[lista_cidades['uf'].loc[linha]],[teste]]).transpose()
    df=pd.concat([df,tabela])
    display(df)
    linha += 1
    if linha > linha_final:
        break
        
    df.to_csv('IBGE_PE.csv')
