##########################
## Librerias importadas ##
##########################

import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import time

#Sacamos del <SUPERMERCADO>, al buscar en la barra "Cervezas"
Cervezas=pd.DataFrame(columns=['Product','Brand' ,'Price','IMG','href'])
#La busqueda total tiene 13 paginas

###################################################################
# Informacion por catalogo de paginas del respectivo supermercado #
###################################################################

for page in range(1,13):
  # Obtenemos los heders de las request necesarios para realizar la conexion por pagina 
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': '*/*',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
    'Origin': 'https://www.<SUPERMERCADO>.cl',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Referer': 'https://www.<SUPERMERCADO>.cl/',
    'Connection': 'keep-alive',
    'TE': 'trailers',
  }

  data = '{"selectedFacets":[{"key":"trade-policy","value":"39"}]}'

  # Modificamos la URL con la respectiva pagina que se esta estudiando
  url='https://api<SUPERMERCADO>web.smdigital.cl/catalog/api/v1/search/cervezas?page='+str(page)
  # Creacion de la request POST para obtener la inforamcion de la pagina web
  response = requests.post(url, headers=headers, data=data)
  # La informacion de respuesta la obtenemos en JSON
  data=json.loads(response.text)
  
  # Separacion de la informacion del JSON por producto encontrado en la pagina web
  for i in range(0,len(data['products'])):
    Cervezas=Cervezas.append({'Product' : data['products'][i]['productName'] ,'Brand':data['products'][i]['brand'] ,'Price' : data['products'][i]['items'][0]['sellers'][0]['commertialOffer']['Price'], 'IMG' : data['products'][i]['items'][0]['images'][0]['imageUrl'],'href' : data['products'][i]['linkText']+'/p'},ignore_index=True)
  time.sleep(10) # Tiempo de descanso del proceso 

  # Guadado de la informacion en CSV
  Cervezas.to_csv('Chelas_<SUPERMERCADO>_480.csv')
  
#########################################################################
# Header de request para la obtencion las descripciones de cada cerveza #
#########################################################################
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': '*/*',
    'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'x-api-key': 'IuimuMneIKJd3tapno2Ag1c1WcAES97j',
    'Origin': 'https://www.<SUPERMERCADO>.cl',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Referer': 'https://www.<SUPERMERCADO>.cl/',
    'Connection': 'keep-alive',
    'TE': 'trailers',
}

data = '{"selectedFacets":[{"key":"trade-policy","value":"39"}]}'
Descrip_chelas=pd.DataFrame(columns=['Description'])

################################################################################
# Uso de BEAUTIFULSOUP para la obtencion de las descripciones de los productos #
################################################################################

for x in Cervezas['href']:
  url='http://www.<SUPERMERCADO>.cl/'+x
  r=requests.post(url, headers=headers, data=data)
  soup=BeautifulSoup(r.text)
  try:
    description=soup.find('div', attrs={'class':'product-description-content'})
    Descrip_chelas=Descrip_chelas.append({'Description':description.text},ignore_index=True)
  except:
    Descrip_chelas=Descrip_chelas.append({'Description':'None'},ignore_index=True)
  time.sleep(2)

# Concatenacion de la inforamcion obtenida por el metodo bruto mas el metodo de beatifulsoup
Chelas_final=pd.concat([Cervezas,Descrip_chelas],axis=1)



########################
# download DB in colab #
########################

Chelas_final.to_csv('Chelas_DB.csv')
from google.colab import files
files.download('Chelas_DB.csv')
  
#Descarga de fotos de cada producto
import time
from google.colab import auth
auth.authenticate_user()

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials

gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

import requests
from io import BytesIO
from PIL import Image

k=0
FOLDER_ID = 'YOUR-ID-FOLDER' #Specify the folder ID you want to save
for url in chelas_db['IMG']:
  k+=1
  file_name='chela'+str(k)+'.png'
  try:
    r = requests.get(url)
    i = Image.open(BytesIO(r.content))
    i.save(file_name)
    f = drive.CreateFile({'title' : file_name, 'parents':[{'id' : FOLDER_ID }]})
    f.SetContentFile(file_name)
    f.Upload()
    print('ok ',k)
  except:
    pass
  time.sleep(3)
