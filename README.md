# PLANTSAT

Página que permite um usuário comparar tipos de vegetação.

## Deploy no HEROKU

**LINK HEROKU - [PLANTSAT](http://plantsat.herokuapp.com).**

## Deploy

### Python ###

Download e instalação da versão mais recente do Python

**Windows** - [Python](https://www.python.org/downloads/).

**Linux** - A maioria das versões linux já vem com python3 instalado.

### PIP ###

Agora, faça a instalação do Pip para Python 3

**Linux**
```
sudo apt-get install python3-pip
```

**Não é necessário a instalação do PIP no windows**

### Clone do repositório ###

**Opção 1: Faça o download do repositório** - [Download](https://github.com/oguilherme-lima/plantsat/archive/master.zip)

Extraia o ZIP, e acesse **maps-master**

**Opção 2: Faça o clone pelo Git Bash**
```
git clone https://github.com/oguilherme-lima/plantsat.git
```
Depois digite
```
cd maps
```

### Pacotes

Agora faça a instalação dos pacotes necessários para rodar a aplicação.

**Opção 1: No mesmo diretório do requiriments.txt execute:**

**Windows**
```
pip3 install -r requirements.txt
```

**Linux**
```
sudo pip3 install -r requirements.txt
```

**Opção 2: execute no terminal**

**Windows**
```
pip3 install gunicorn==19.9.0 flask==1.0.2 googlemaps==3.0.2 flask_compress==1.4.0 flask_googlemaps pillow tensorflow keras
```
**Linux**
```
sudo pip3 install gunicorn==19.9.0 flask==1.0.2 googlemaps==3.0.2 flask_compress==1.4.0 flask_googlemaps pillow tensorflow keras
```
### Exportar e rodar a aplicação

Por fim, para inicializar a aplicação, digite os comandos abaixo:

**Windows**
```
set FLASK_APP=app.py
```
```
flask run
```
**Linux**
```
export FLASK_APP=app.py
```
```
flask run
```

**Agora é só acessar a url http://127.0.0.1:5000/**
