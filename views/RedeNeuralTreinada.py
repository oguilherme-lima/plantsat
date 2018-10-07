import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K

def retorna_tipo_plantacao(nomeImagem):
    #Carrega rede neural
    arquivo = open("files_ai\laranja.json", "r")
    estrutura_rede = arquivo.read()
    arquivo.close()
    classificador = model_from_json(estrutura_rede)
    classificador.load_weights("files_ai\laranja.h5")

    # Carrega Imagem
    imagem = image.load_img(nomeImagem, target_size=(64,64))
    imagem = image.img_to_array(imagem)
    imagem /= 255
    imagem = np.expand_dims(imagem, axis=0)

    # Previsão
    previsor = classificador.predict(imagem)
    K.clear_session()
    return False if previsor < 0.50 else True