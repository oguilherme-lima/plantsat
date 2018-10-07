import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K
from urllib import request as request_urllib
from io import BytesIO
from PIL import Image
import os

# Configura as apis do Gmaps
# Chave de utilização Google Maps
gmaps_key = "AIzaSyC18sKb1tmkH6aj3XHTjG-3V6XHIlINw-k"

def retorna_tipo_plantacao(nomeImagem):
    #Carrega rede neural
    arquivo = open("laranja.json", "r")
    estrutura_rede = arquivo.read()
    arquivo.close()
    classificador = model_from_json(estrutura_rede)
    classificador.load_weights("laranja.h5")

    # Carrega Imagem
    imagem = image.load_img(nomeImagem, target_size=(64,64))
    imagem = image.img_to_array(imagem)
    imagem /= 255
    imagem = np.expand_dims(imagem, axis=0)

    # Previsão
    previsor = classificador.predict(imagem)
    K.clear_session()
    return False if previsor > 0.50 else True

# Gera uma imagem do local pesquisado no Google Maps
def verifica_tipo(coordenadas):
    try:
        # Limpa o console
        os.system('cls' if os.name == 'nt' else 'clear')
        # Recebe a quantidade de erros
        qtd_erros = 0
        for coordenada in coordenadas:
            # Recebe as coordenadas do usuario
            latitude = coordenada[0]
            longitude = coordenada[1]
            # Recebe o resultado esperado da coordenada inserida
            resultado_esperado = coordenada[2]
            # Define o tipo de visualização do mapa
            #  Tipos
                #  roadmap - Exibe a visualização padrão do mapa
                #  satellite - Exibe imagens de satelites do Google Earth
                # hybrid - Exibe uma mistura satellite com roadmap
                # terrain - exibe um mapa físico com base nas informações do terreno.
            maptype = "satellite"
            # Define o tamanho da imagem que será baixada
            imageSize = '800x800'
            # Zoom padrão do mapa
            zoom = "18"
            # Cria a Visualizaçao do mapa com a API do google
            #  Adiciona a Latitude, longitude, tamanho da imagem, zoom, tipo de mapa e key da API da Google na url
            url = 'http://maps.googleapis.com/maps/api/staticmap?center=' + str(latitude) + ',' + str(longitude) + '&size=' + imageSize + '&zoom=' + zoom + '&maptype=' + maptype + '&key=' + gmaps_key
            # Abre a url e faz a leitura da pagina
            with request_urllib.urlopen(url) as url:
                page = url.read()
            # Aloca o resultado da página na memoria
            buffer = BytesIO(page)
            # Abre e identifica a imagem recebida
            image = Image.open(buffer)
            # Cria um nome para imagem - latitudelongitude.png que será utilizada para a API
            nomeImagem = str(latitude) + str(longitude) + ".png"
            # Salva a imagem no diretorio do projeto
            image.save(nomeImagem)
            # Recebe o retorno da IA
            e_laranja = retorna_tipo_plantacao(nomeImagem)
            # Remove a imagem do diretorio
            os.remove(nomeImagem)
            # Imprime no console
                # LATITUDE: X || LONGITUDE: Y
                # RESULTADO: É OU NÃO LARANJA
                # ESPERADO: É OU NÃO LARANJA
            print('LATITUDE: ', latitude, ' || LONGITUDE: ', longitude,
                '\nRESULTADO: ', 'É LARANJA' if e_laranja else 'NÃO É LARANJA',
                '\nESPERADO: ', resultado_esperado, '\n' )

            # Se o resultado é diferente do resultado esperado, adiciona 1 nos erros
            if (('E LARANJA' if e_laranja else 'NAO E LARANJA') != resultado_esperado):
                qtd_erros += 1

        # Informações dos resultados
        print('Total de comparações:', len(coordenadas))
        print('Quantidade de erros:', qtd_erros)
        print('Porcentagem de acertos:', 100.0 - (qtd_erros*100/len(coordenadas)), '%')
    # Se acontecer algum erro
    except Exception as e:
    # Printa o erro no terminal
        print(e)


coordenadas = [
	[-22.464062,-46.485597,"NAO E LARANJA"],
	[-22.025754,-46.612979,"NAO E LARANJA"],
	[-22.046688,-46.627706,"NAO E LARANJA"],
	[-22.904525,-44.506656,"NAO E LARANJA"],
	[-22.994972,-44.974351,"NAO E LARANJA"],
	[-21.877600,-47.146181,"E LARANJA"],
	[-21.837871,-47.096982,"E LARANJA"],
	[-21.842827,-47.117063,"E LARANJA"],
	[-21.832821,-47.118938,"E LARANJA"],
	[-21.855930,-47.134541,"E LARANJA"]
	]

verifica_tipo(coordenadas)