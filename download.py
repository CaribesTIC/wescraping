#######################################################################
## Script en python para descargar archivos leyendo un archivo .xlsx ##
## Autor: <Gregorio Bolivar> elalconxvii@gmail.com                   ##
########################################################################
# Paquete para poder leer el xls
import pandas as pd

# Pquete para hacer los request
import requests

# Paquete para hacer el webcraping
from bs4 import BeautifulSoup

# Paquete para hacer descarga de archivos
import wget

# Paquete para poder verificar si existe carpetas o archivos
import pathlib

# Para manipular archivos del sistema
import os

# Leer archivo xlsx con toda la informacion
df = pd.read_excel('springer_ebooks_converted_v2.xlsx', sheet_name='contents')

# Iterar en cada fila 
for index, row in df.iterrows():

    # Extraer el titulo replazando los espacios por -
    title = (row["Title"]).replace(" ", "-").strip()

    # Extraer el nombre del paquete replazando los espacios por -
    folder = (row["Package"]).replace(" ", "-").strip()

    # Crear directorio si no existe
    path = os.getcwd()+os.sep + 'springer' + os.sep + folder
    
    try:
        os.stat(path)
    except:
        os.mkdir(path)
    
    # Extraer la url del iem
    url = (row["OpenURL"]).strip()
    # Request a la url del item
    page = requests.get(url)
    # Webcraping 
    soup = BeautifulSoup(page.content, 'html.parser')
    # Buscar esta etiqueta a para los pdf de descarga
    for link in soup.find_all('a', class_='c-button c-button--blue c-button__icon-right test-download-book-options test-bookpdf-link'):
        # Extraer los href
        cont = link.get('href')
        # Fomatear la url para la descarga
        url = 'https://link.springer.com/' + cont
        
        # Para verificar que no exista el pdf localmente
        file = pathlib.Path(path + os.sep + title + '.pdf')
        if file.exists():
            print('Ya existe el archivo pdf: '+title)
        else:
            wget.download(url, path + os.sep + title + '.pdf')
            print('Descarga finalizada del pdf: '+title)
    

