import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import time

#Sacamos del jumbo, al buscar en la barra "Cervezas"
Cervezas=pd.DataFrame(columns=['Product','Brand' ,'Price','IMG','href'])
#La busqueda total tiene 13 paginas

for page in range(1,13):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': '*/*',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
    'Origin': 'https://www.jumbo.cl',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Referer': 'https://www.jumbo.cl/',
    'Connection': 'keep-alive',
    'TE': 'trailers',
  }

  data = '{"selectedFacets":[{"key":"trade-policy","value":"39"}]}'


  url='https://apijumboweb.smdigital.cl/catalog/api/v1/search/cervezas?page='+str(page)
  response = requests.post(url, headers=headers, data=data)
  data=json.loads(response.text)
  for i in range(0,len(data['products'])):
    Cervezas=Cervezas.append({'Product' : data['products'][i]['productName'] ,'Brand':data['products'][i]['brand'] ,'Price' : data['products'][i]['items'][0]['sellers'][0]['commertialOffer']['Price'], 'IMG' : data['products'][i]['items'][0]['images'][0]['imageUrl'],'href' : data['products'][i]['linkText']+'/p'},ignore_index=True)
  time.sleep(10)
Cervezas.to_csv('Chelas_jumbo_480.csv')

#Obtener las descripciones de cada chela, MEJORAR EL TEMA CON LOS ACENTOS :C
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': '*/*',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
    'Origin': 'https://www.jumbo.cl',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Referer': 'https://www.jumbo.cl/',
    'Connection': 'keep-alive',
    'TE': 'trailers',
}

data = '{"selectedFacets":[{"key":"trade-policy","value":"39"}]}'
Descrip_chelas=pd.DataFrame(columns=['Description'])

for x in Cervezas['href']:
  url='http://www.jumbo.cl/'+x
  r=requests.post(url, headers=headers, data=data)
  soup=BeautifulSoup(r.text)
  try:
    description=soup.find('div', attrs={'class':'product-description-content'})
    Descrip_chelas=Descrip_chelas.append({'Description':description.text},ignore_index=True)
  except:
    Descrip_chelas=Descrip_chelas.append({'Description':'None'},ignore_index=True)
  time.sleep(2)


Chelas_final=pd.concat([Cervezas,Descrip_chelas],axis=1)

#pal colab
Chelas_final.to_csv('Chelas_DB.csv')
from google.colab import files
files.download('Chelas_DB.csv')
  
