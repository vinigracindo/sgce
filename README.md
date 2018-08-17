# SGCE

[![Build Status](https://travis-ci.org/vinigracindo/sgce.svg?branch=develop)](https://travis-ci.org/vinigracindo/sgce.svg?branch=develop)
[![Code Health](https://landscape.io/github/vinigracindo/sgce/develop/landscape.svg?style=flat)](https://landscape.io/github/vinigracindo/sgce/develop)
[![Coverage Status](https://coveralls.io/repos/github/vinigracindo/sgce/badge.svg?branch=develop)](https://coveralls.io/github/vinigracindo/sgce?branch=develop)
[![Requirements Status](https://requires.io/github/vinigracindo/sgce/requirements.svg?branch=develop)](https://requires.io/github/vinigracindo/sgce/requirements/?branch=develop)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

## [Changelog](CHANGELOG.md)

## Sistema Gerenciador de Certificados Eletrônicos.

Live demo:<br/>
https://sgce-app.herokuapp.com/<br/>
https://sgce-app.herokuapp.com/login/ (User: admin | Password: adm11200)


O SGCE está sendo desenvolvido baseado no [SGCE criado pela Universidade Federal de Pampa](https://softwarepublico.gov.br/social/sgce) que foi descontinuado.
Por este motivo, uma nova versão está sendo criada em python/django. Ressalto que essa versão não tem relação alguma com os servidores da
Unipampa.

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
cp contrib/env-sample .env
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
copy contrib/env-sample .env
python manage.py migrate
python manage.py loaddata Group
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

## History