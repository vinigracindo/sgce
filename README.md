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


## Como realizar Deploy no Ubuntu Server

### 1. Instalando o Nginx

1. Atualize seu ubuntu: `sudo apt-get update`
2. Instale o nginx: `sudo apt-get install nginx`
3. Verifique se o servidor está funcionando: http://<ip_do_servidor>

### 2. Instalando o banco de dados

1. Instale o postgresql ou um banco de sua preferência: `apt-get install postgresql postgresql-contrib`
2. Após a instalação, entre no postgres: `sudo -i -u postgres`
3. Verifique se o postgres foi instalado: `psql`

### 3. Criando um usuário e um banco de dados no Postgres

1. `sudo -i -u postgres`
2. `psql`
3. `CREATE USER postgres_user WITH PASSWORD `password`/
4. `CREATE DATABASE my_postgres_db OWNER postgres_user;`
5. `\q`
6. `exit`
7. Efetue login com o usuário criado: `sudo -i -u postgres_user`
8. Verifique se o banco foi criado: `psql my_postgres_db`

### 4. Criando um Ambiente Virtual (virtualenv)

1. `cd /var/www/html/`
2. `mkdir sgce' e 'cd sgce'
3. `python3 -m venv .sgce`
4. Ative o ambiente virtual: `source .sgce/bin/activate`

### 5. Baixando o SGCE do repositório
1. `cd /var/www/html/sgce`
2. Baixe a versão mais recente: `git clone --branch v1.0.1 https://github.com/vinigracindo/sgce.git .` (é muito importante o ponto no final para não criar uma outra pasta).
3. Baixe as dependências do projeto: `pip3 install -r requirements.txt`

### 6. Configurando o banco de dados e os arquivos estáticos no settings.py
```py
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'my_postgres_db',
    'USER': 'postgres_user',
    'PASSWORD': '.....',
    'HOST': 'localhost',
    'PORT': '',
}

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```

### 7. Configurando o settings.ini
1. Edite o arquivo /var/www/html/sgce/sgce/settings.ini
2. É necessário gerar uma nova chave para SECRET_KEY. Para gerar rode o arquivo contrib/secret_gen.py (NÃO DEIXE A CHAVE PADRÃO).
3. Adicione a linha DEBUG=False
4. Adicione ALLOWED_HOSTS e coloque seu domínio. Ex.: ALLOWED_HOSTS=127.0.0.1, meudominio.com, sgce.ifal.edu.br
5. Adicione a linha SITE_URL e adicione seu domínio. Ex.: SITE_URL=https://sgce.ifal.edu.br


### 8. Configurando o Django
1. Crie um arquivo de configuração: `copy contrib\ini-sample settings.ini`
2. Entre no arquivo gerado settings.ini.
-> 2.1 - Coloque DEBUG=False;
-> 2.2 - Em ALLOWED_HOSTS coloque seu domínio;
-> 2.3 - Em SITE_URL coloque seu domínio;
-> 2.4 - Gere um novo SECRET_KEY `python contib/secret_get.py`. Copie a chave gerada pelo comando e coloque em SECRET_KEY;
3. Rode as migrações no banco de dados: `python manage.py migrate`
4. Rode os testes e verifique se está tudo correto: `python manage.py test`
5. Crie um usuário administrator: `python manage.py createsuperuser`
6. `python manage.py collectstatic`
7. Rode o seguinte comando: `python manage.py loaddata Group`
8. Rode o servidor `python manage.py runserver 0.0.0.0:8000` e verifique se está funcionando na acessando http://<ip_servidor>:8000


### 9. Trabalhando com Gunicorn
1. `pip3 install gunicorn`
2. Rode `gunicorn -b 0.0.0.0:8000 sgce.wsgi` (wsgi é um arquivo do SGCE. Esteja na mesma pasta que ela para executar o comando).
3. Verifique se o servidor está funcionando em http://<ip_servidor>:8000


### 10. Trabalhando com Supervisor
1. `pip3 install supervisor `
2. Navegue até a página `cd /etc/supervisor/conf.d/`
3. Crie um usuário www-data no Ubuntu
```
sudo groupadd varwwwusers
sudo adduser www-data varwwwusers
sudo chgrp -R varwwwusers /var/www/
sudo chmod -R 760 /var/www/
```
4. Crie um arquivo de configuração `nano sgce.conf`

```
[program:sgce]
directory=/var/www/html/sgce/sgce
command=/var/www/html/sgce/.sgce/bin/gunicorn -b 0.0.0.0:8000 sgce.wsgi
user = www-data
startsecs = 0
autostart=true
```

### 11. Configurando o Nginx para o projeto
1. Entre na pasta de configuração do Nginx `cd /etc/nginx/sites-available/`
2. Crie um arquivo `nano sgce`

```
upstream sgce {
        server 127.0.0.1:8000;
}

server {
        listen 80;
        server_name <dominio>;
        access_log /var/log/nginx/sgce.log;
        error_log /var/log/nginx/sgce.error.log;

        location / {
                proxy_pass http://sgce;
                proxy_redirect  off;

                proxy_set_header        Host            $http_host;
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;

                client_max_body_size            10m;
                client_body_buffer_size         128k;

                proxy_connect_timeout           90;
                proxy_send_timeout              90;
                proxy_read_timeout              90;

                proxy_buffer_size               4k;
                proxy_buffers                   4 32k;
                proxy_busy_buffers_size         64k;
                proxy_temp_file_write_size      64k;
        }

        location /static/ {
                root /var/www/html/sgce/sgce;
        }
        location /media/ {
                root /var/www/html/sgce/sgce;
        }
}

```

3. Entre em `cd /etc/nginx/sites-enabled`
3. Crie um link simbólico `ln -s /etc/nginx/sites-available/sgce .`
3. Rode os testes do Nginx e veja se está ok: `nginx -t`
4. Rode `service nginx restart`

## :tada: Verifique: http://dominio.com (Deploy realizado com sucesso).
