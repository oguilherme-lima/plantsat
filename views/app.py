from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_googlemaps import GoogleMaps, Map
from flask_compress import Compress
from urllib import request as request_urllib
from io import BytesIO
from PIL import Image
import googlemaps
import os
from .RedeNeuralTreinada import retorna_tipo_plantacao

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Configura as apis do Gmaps
# Chave de utilização Google Maps
gmaps_key = "AIzaSyC18sKb1tmkH6aj3XHTjG-3V6XHIlINw-k"
# API que cria o mapa na tela
GoogleMaps(app, key=gmaps_key)
# API que faz a busca dos endereços
gmaps = googlemaps.Client(key=gmaps_key)

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html', titulo="PlantSat")

# Pagina com o resultado
@app.route('/resultado')
def resultado():
    # Recebe o nome da imagem da sessão
    nomeImagem = session.get('nomeImagem', None)
    # Recebe o resultado da IA da sessão
    e_laranja = session.get('e_laranja', None)
    return render_template('resultado.html', titulo='Resultado', nomeImagem=nomeImagem, e_laranja=e_laranja)

# Pagina do mapa
@app.route('/mapa')
def mapa():
    endereco = ''
    # Boolean que define se existe plantação ou não
    # Recebe o resultado da IA
    e_laranja = False
    # Boolean que define o botão do mapa
    processar = True
    # Visualização Padrão - Brasil
    mapa = maps(-21.9697, -47.8199, 5)
    # Input do frontend que recebe o valor da latitude
    latitude = ''
    # Input do frontend que recebe o valor da longitude
    longitude = ''
    # Recebe o nome da imagem
    nomeImagem = ''
    # Se existir texto no botão processar
    if (request. args.get('processar')):
        # Salva a imagem
        # Retorna o nome da imagem e salva na sessão
        # Retorna 0 ou 1 de acordo com o resultado da IA e salva a sessão
        session['nomeImagem'], session['e_laranja'] = salvar_imagem(str(request. args.get('latitude')).strip(), str(request. args.get('longitude')).strip())
        # Redireciona para a página de resultado
        return redirect(url_for('resultado'))
    # Se existir texto no campo endereço da tela
    elif (request. args.get('endereco')):
        # Recebe o endereço do input
        endereco = request. args.get('endereco')
        try:
            # Faz a busca de todos os dados do endereço na API
            geocode_result = gmaps.geocode(endereco)
            # Recebe a latitude do retorno da API
            latitude = str(geocode_result[0]['geometry']['location']['lat']).strip()
            # Recebe a longitude do retorno da API
            longitude = str(geocode_result[0]['geometry']['location']['lng']).strip()
            # Define a visualização padrão do mapa que será visualizado pelo usuário
            mapa = maps(latitude, longitude, 18)
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
            latitude = str(request. args.get('latitude')).strip()
            # Recebe a longitude do input
            longitude = str(request. args.get('longitude')).strip()
            # Define a visualização padrão do mapa que será visualizado pelo usuário
            mapa = maps(latitude, longitude, 17)
            # Apresenta mensagem de sucesso
            flash("Local encontrado com sucesso!")
        # Se acontecer algum erro
        except Exception as e:
            # Apresenta mensagem de erro para o usuário
            flash("Não foi possível encontrar o local")
            # Printa no terminal o erro
            print(e)
    else:
        # Se não existir valores nos campos naõ exibe botão de processar
        processar = False

    return render_template('mapa.html', titulo="Mapa", movingmap=mapa, endereco_salvo=endereco.title(),
                           latitude=latitude, longitude=longitude, e_laranja=e_laranja,
                           nomeImagem=nomeImagem, processar=processar)

# Retorna uma instancia do tipo MAP com os dados para criar o mapa
def maps(latitude, longitude, zoom):
    return Map(
        identifier="movingmap",
        varname="movingmap",
        # Visualização padrão do mapa
        # latitude padrão
        lat=latitude,
        # longitude padrão
        lng=longitude,
        # Zoom do mapa
        zoom=zoom,
        # Tipo de visualização do mapa
        maptype="SATELLITE",
        # Linguagem do mapa
        language="pt",
        # Tamanho do mapa
        style="height:400px;width:100%;",
        # Remove todos os botões do mapa e iterações com o mapa
        # Permanece apenas clique para movimentar mapa
        zoom_control=False,
        maptype_control=False,
        scale_control=False,
        streetview_control=False,
        rotate_control=False,
        fullscreen_control=False,
        scroll_wheel=False
    )

# Gera uma imagem do local pesquisado no Google Maps
def salvar_imagem(latitude, longitude):
    try:
        # Define o tipo de visualização do mapa
        # Tipos:
            # roadmap   - Exibe a visualização padrão do mapa;
            # satellite - Exibe imagens de satelites do Google Earth;
            # hybrid    - Exibe uma mistura satellite com roadmap;
            # terrain   - Exibe um mapa físico com base nas informações do terreno.
        maptype = "satellite"
        # Define o tamanho da imagem que será baixada
        imageSize = '800x800'
        # Zoom padrão do mapa
        zoom = "18"
        # Cria a Visualizaçao do mapa com a API do google
        # Adiciona a Latitude, longitude, tamanho da imagem, zoom, tipo de mapa e key da API da Google na url
        url = 'http://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(
            longitude) + '&size=' + imageSize + '&zoom=' + zoom + '&maptype=' + maptype + '&key=' + gmaps_key
        # Abre a url e faz a leitura da pagina
        with request_urllib.urlopen(url) as url:
            page = url.read()
        # Aloca o resultado da página na memoria
        buffer = BytesIO(page)
        # Abre e identifica a imagem recebida
        image = Image.open(buffer)
        # Cria um nome para imagem - latitudelongitude.png que será utilizada para a API
        nomeImagem = "static/downloaded_images/" + str(latitude) + str(longitude) + ".png"
        # Salva a imagem no diretorio do projeto
        image.save(nomeImagem)
        # Recebe o retorno da API
        e_laranja = retorna_tipo_plantacao(nomeImagem)
        # Remove o caminho do nome da imagem
        nomeImagem = str(latitude) + str(longitude) + ".png"
        return nomeImagem, e_laranja
    # Se acontecer algum erro
    except Exception as e:
        # Printa o erro no terminal
        print(e)

if __name__ == '__main__':
    app.run()