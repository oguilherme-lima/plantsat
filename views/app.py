from flask import Flask
from flask import render_template, request, flash
from flask_googlemaps import GoogleMaps, Map
from flask_compress import Compress
import os
import googlemaps
from views import GoogleMapDownloader

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Configura a api do Gmaps
GoogleMaps(app, key="AIzaSyBybFqISUIGfRoLJoSyDUOa_4N4pRUIF8g")
gmaps = googlemaps.Client(key='AIzaSyBybFqISUIGfRoLJoSyDUOa_4N4pRUIF8g')


# Página de inicio
@app.route('/')
def index():
    return render_template('index.html', titulo="PlantSat")

# Pagina do mapa
@app.route('/mapa')
def mapa():
    endereco = ''
    # Visualização Padrão - Brazil
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
            #salva_imagem(latitude,longitude)
            # Apresenta mensagem de sucesso
            flash("Local encontrado com sucesso!")
        except:
            flash("Erro ao buscar local")
    # Se não existir texto no campo de endereço
    # Verifica se existe texto no campo latitude e longitude
    elif (request. args.get('latitude') and request. args.get('longitude')):
        try:
            latitude = request. args.get('latitude')
            longitude = request. args.get('longitude')
            mapa = maps(latitude, longitude, 17)
            # Salva a imagem no diretorio
            #salva_imagem(latitude,longitude)
            # Apresenta mensagem de sucesso
            flash("Local encontrado com sucesso!")
        except:
            flash("Erro ao buscar local")

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

# Salvar a imagem em alta qualidade
def salva_imagem(latitude, longitude):
    # Instancia um objeto do GoogleMapDownloads
    gmd = GoogleMapDownloader.GoogleMapDownloader(float(latitude), float(longitude), 17)
    # Gera a imagem
    img = gmd.generateImage()
    # Cria um nome para imagem
    nomeImagem = str(latitude) + str(longitude) + ".png"
    # Salva a imagem
    img.save(nomeImagem)


if __name__ == '__main__':
    app.run()