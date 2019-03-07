# SGCE

[![Build Status](https://travis-ci.org/vinigracindo/sgce.svg?branch=master)](https://travis-ci.org/vinigracindo/sgce.svg?branch=master)
[![Code Health](https://landscape.io/github/vinigracindo/sgce/master/landscape.svg?style=flat)](https://landscape.io/github/vinigracindo/sgce/master)
[![Coverage Status](https://coveralls.io/repos/github/vinigracindo/sgce/badge.svg?branch=master)](https://coveralls.io/github/vinigracindo/sgce?branch=master)
[![Requirements Status](https://requires.io/github/vinigracindo/sgce/requirements.svg?branch=master)](https://requires.io/github/vinigracindo/sgce/requirements/?branch=master)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

## Sistema Gerenciador de Certificados Eletrônicos

### [Changelog](CHANGELOG.md)

Live demo:<br/>
https://sgce-app.herokuapp.com/<br/>
https://sgce-app.herokuapp.com/login/ (User: admin | Password: adm11200)


O SGCE está sendo desenvolvido baseado no [SGCE criado pela Universidade Federal de Pampa](https://softwarepublico.gov.br/social/sgce).

## Screenshots
![Main](https://user-images.githubusercontent.com/999040/44290422-0b453080-a24f-11e8-9075-fbcdfab8a96e.png)
![Certificado](https://user-images.githubusercontent.com/999040/44290578-b81fad80-a24f-11e8-9277-2fcdb33d071a.png)

## Requerimentos
1. Django >= 2.0
2. Python >= 3.6
3. PostgresSQL >= 9.4

## Como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com Python 3.6
3. Ative o virtualenv.
4. Instale as depêndencias.
5. Configure a instância com o .env
6. Rode as Migrações
7. Importe os Dados Iniciais
8. Execute os testes.
9. Crie um super usuário.
9. Rode o servidor


### Linux
```console
git clone https://github.com/vinigracindo/sgce.git sgce
cd sgce
python -m venv .sgce
source .sgce/bin/activate
pip install -r requirements.txt
cp contrib/ini-sample settings.ini
python manage.py migrate
python manage.py loaddata Group
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

### Windows
```console
git clone https://github.com/vinigracindo/sgce.git sgce
cd sgce
python -m venv .sgce
.sgce\Scripts\activate
pip install -r requirements.txt
copy contrib\ini-sample settings.ini
python manage.py migrate
python manage.py loaddata Group
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```
