from flask import Flask, render_template, request, flash
from flask_googlemaps import GoogleMaps, Map
from flask_compress import Compress
from urllib import request as request_urllib
from io import BytesIO
from PIL import Image
import googlemaps
import os

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Configura as apis do Gmaps
# API que cria o mapa na tela
GoogleMaps(app, key="AIzaSyBybFqISUIGfRoLJoSyDUOa_4N4pRUIF8g")
# API que faz a busca dos endereços
gmaps = googlemaps.Client(key='AIzaSyBybFqISUIGfRoLJoSyDUOa_4N4pRUIF8g')

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html', titulo="PlantSat")

# Pagina do mapa
@app.route('/mapa')
def mapa():
    endereco = ''
    # Visualização Padrão - Brasil
    mapa = maps(-21.9697, -47.8199, 5)
    # Se existir texto no campo endereço da tela
    if (request. args.get('endereco')):
        # Recebe o endereço do input
        endereco = request. args.get('endereco')
        try:
            # Faz a busca de todos os dados do endereço na API
            geocode_result = gmaps.geocode(endereco)
            # Recebe a latitude do retorno da API
            latitude = geocode_result[0]['geometry']['location']['lat']
            # Recebe a longitude do retorno da API
            longitude = geocode_result[0]['geometry']['location']['lng']
            # Define a visualização padrão do mapa que será visualizado pelo usuário
            mapa = maps(latitude, longitude, 17)
            # Salva a imagem no diretorio
            #salvar_imagem(latitude,longitude)
            # Apresenta mensagem de sucesso
            flash("Local encontrado com sucesso!")
        except Exception as e:
            # Apresenta mensagem de erro para o usuário
            flash("Erro ao buscar local")
            # Printa o erro no terminal
            print(e)
    # Se não existir texto no campo de endereço
    # Verifica se existe texto no campo latitude e longitude
    elif (request. args.get('latitude') and request. args.get('longitude')):
        try:
            # Recebe a latitude do input
            latitude = request. args.get('latitude')
            # Recebe a longitude do input
            longitude = request. args.get('longitude')
            # Define a visualização padrão do mapa que será visualizado pelo usuário
            mapa = maps(latitude, longitude, 17)
            # Salva a imagem no diretorio
            #salvar_imagem(latitude, longitude)
            # Apresenta mensagem de sucesso
            flash("Local encontrado com sucesso!")
        # Se acontecer algum erro
        except Exception as e:
            # Apresenta mensagem de erro para o usuário
            flash("Não foi possível encontrar o local")
            # Printa no terminal o erro
            print(e)

    return render_template('mapa.html', titulo="Mapa", movingmap=mapa)

# Retorna uma instancia do tipo MAP com os dados para criar o mapa
def maps(latitude, longitude, zoom):
    return Map(
        identifier="movingmap",
        varname="movingmap",
        # latitude padrão quando abrir o mapa
        lat=latitude,
        # longitude padrão quando abrir o mapa
        lng=longitude,
        # Distancia do mapa
        zoom=zoom,
        # Tipo de visualização do mapa
        maptype="SATELLITE",
        # Linguagem do mapa
        language="pt",
        # Tamanho do mapa
        style="height:400px;width:100%;",
        # Pontos do mapa
        markers=[(latitude, longitude)]
    )

# Gera uma imagem do local pesquisado no Google Maps
def salvar_imagem(latitude, longitude):
    try:
        # Define o tipo de visualização do mapa
        # Tipos
            # roadmap - Exibe a visualização padrão do mapa
            # satellite - Exibe imagens de satelites do Google Earth
            # hybrid - Exibe uma mistura satellite com roadmap
            # terrain - exibe um mapa físico com base nas informações do terreno.
        maptype = "satellite"
        # Define o tamanho da imagem que será baixada
        imageSize = '640x640'
        # Zoom padrão do mapa
        zoom = "17"
        # Cria a Visualizaçao do mapa com a API do google
        # Adiciona a Latitude, longitude, tamanho da imagem, zoom e tipo de mapa na url
        url = 'http://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(
            longitude) + '&size=' + imageSize + '&zoom=' + zoom + '&maptype=' + maptype
        # Abre a url e faz a leitura da pagina
        with request_urllib.urlopen(url) as url:
            page = url.read()
        # Aloca o resultado da página na memoria
        buffer = BytesIO(page)
        # Abre e identifica a imagem recebida
        image = Image.open(buffer)
        # Mostra a imagem recebida para o usuário
        image.show()
        # Cria um nome para imagem - latitudelongitude.png
        nomeImagem = str(latitude) + str(longitude) + ".png"
        # Salva a imagem no diretorio do projeto
        image.save(nomeImagem)
    # Se acontecer algum erro
    except Exception as e:
        # Printa o erro no terminal
        print(e)

if __name__ == '__main__':
    app.run()