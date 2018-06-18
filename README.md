# SGCE

[![Build Status](https://travis-ci.org/vinigracindo/sgce.svg?branch=master)](https://travis-ci.org/vinigracindo/sgce.svg?branch=master)
[![Code Health](https://landscape.io/github/vinigracindo/sgce/master/landscape.svg?style=flat)](https://landscape.io/github/vinigracindo/sgce/master)
[![Coverage Status](https://coveralls.io/repos/github/vinigracindo/sgce/badge.svg?branch=master)](https://coveralls.io/github/vinigracindo/sgce?branch=master)
[![License](https://img.shields.io/pypi/l/django-treenode.svg)](https://img.shields.io/pypi/l/django-treenode.svg)

Sistema Gerenciador de Certificados Eletrônicos.

Live demo: https://sgce-app.herokuapp.com/login/

User: admin | Password: admin11200


O SGCE está sendo desenvolvido baseado no [SGCE criado pela Universidade Federal de Pampa](https://softwarepublico.gov.br/social/sgce) que foi descontinuado.
Por este motivo, uma nova versão está sendo criada em python/django. Ressalto que essa versão não tem relação alguma com os servidores da
Unipampa.

## Como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com Python 3.6
3. Ative se virtualenv.
4. Instale as depêndencias.
5. Configure a instância com o .env
6. Execute os testes.

```console
git clone git@github.com:vinigracindo/sgce.git sgce
cd sgce
python -m venv .sgce
source .sgce/bin/activate #Unix CMD
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy no Heroku?

1. Crie uma instância no Heroku.
2. Envie as configurações para o heroku.
3. Defina uma SECRET_KEY segura para a instância.
4. Define DEBUG=False
5. Configure o serviço de email.
6. Envie o código para o heroku.

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
#Configura Email
git push heroku master --force
```
