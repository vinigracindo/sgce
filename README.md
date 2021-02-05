# SGCE

[![Build Status](https://travis-ci.org/vinigracindo/sgce.svg?branch=master)](https://travis-ci.org/vinigracindo/sgce)
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

## Agradecimentos
[Raphael Gibson](https://github.com/raphaelgibson)

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

### 1. Instalando os pacotes dos repositórios do Ubuntu

1. Atualize seu ubuntu: `sudo apt-get update`
2. Instale o nginx: `sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl`

### 2. Criando o banco de dados e o usuário PostgreSQL

1. Logue-se em uma sessão interativa do Postgres digitando: `sudo -u postgres psql`
2. Crie um banco de dados para seu projeto: `CREATE DATABASE my_postgres_db;`
3. Crie um usuário do banco de dados para o projeto: `CREATE USER meu_usuario WITH PASSWORD 'password';`
4. Dar ao novo usuário acesso para administrar o novo banco de dados: `GRANT ALL PRIVILEGES ON DATABASE my_postgres_db TO meu_usuario;`
5. Configurações opcionais:
```
ALTER ROLE meu_usuario SET client_encoding TO 'utf8';
ALTER ROLE meu_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE meu_usuario SET timezone TO 'UTC';
```

### 3. Criando um Ambiente Virtual (virtualenv)

1. `cd /home/meu_usuario/` // Você pode escolher qualquer pasta dentro do sistema de arquivo.
2. `mkdir sgce` e `cd sgce`
3. `python3 -m venv .sgce`
4. Ative o ambiente virtual: `source .sgce/bin/activate`

### 4. Baixando o SGCE do repositório
1. `cd /home/meu_usuario/sgce`
2. Baixe a versão mais recente: `git clone --branch v1.3.2 https://github.com/vinigracindo/sgce.git .` (é muito importante o ponto no final para não criar uma outra pasta).
3. Baixe as dependências do projeto: `pip3 install -r requirements.txt`

### 5. Configurando o banco de dados e os arquivos estáticos no settings.py
```py
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'my_postgres_db',
    'USER': 'meu_usuario',
    'PASSWORD': '.....',
    'HOST': 'localhost',
    'PORT': '',
}

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```

### 6. Configurando o settings.ini
1. Edite o arquivo /home/meu_usuario/sgce/sgce/settings.ini
2. É necessário gerar uma nova chave para SECRET_KEY. Para gerar rode o arquivo contrib/secret_gen.py (NÃO DEIXE A CHAVE PADRÃO).
3. Adicione a linha DEBUG=False
4. Adicione ALLOWED_HOSTS e coloque seu domínio. Ex.: ALLOWED_HOSTS=127.0.0.1, meudominio.com, sgce.ifal.edu.br
5. Adicione a linha SITE_URL e adicione seu domínio. Ex.: SITE_URL=https://sgce.ifal.edu.br


### 7. Configurando o Django
1. Crie um arquivo de configuração: `copy contrib\ini-sample settings.ini`
2. Entre no arquivo gerado settings.ini.
- Coloque DEBUG=False;
- Em ALLOWED_HOSTS coloque seu domínio;
- Em SITE_URL coloque seu domínio;
- Gere um novo SECRET_KEY `python contib/secret_get.py`. Copie a chave gerada pelo comando e coloque em SECRET_KEY;
3. Rode as migrações no banco de dados: `python manage.py migrate`
4. Rode os testes e verifique se está tudo correto: `python manage.py test`
5. Crie um usuário administrator: `python manage.py createsuperuser`
6. `python manage.py collectstatic`
7. Rode o seguinte comando: `python manage.py loaddata Group`
8. Rode o servidor `python manage.py runserver 0.0.0.0:8000` e verifique se está funcionando.


### 8. Instalando o servidor do aplicativo: Gunicorn
1. `pip3 install gunicorn`
2. Rode `gunicorn -b 0.0.0.0:8000 sgce.wsgi` (wsgi é um arquivo do SGCE. Esteja na mesma pasta que ela para executar o comando).
3. Verifique se o servidor está funcionando em http://<ip_servidor>:8000


### 9. Criando arquivos de socket e de serviço systemd para o Gunicorn
Nós testamos que o Gunicorn pode interagir com nosso aplicativo Django, mas devemos implementar uma maneira mais robusta de começar e parar o servidor do aplicativo. Para isso, vamos fazer arquivos de serviço e de socket do systemd.

O socket Gunicorn será criado no boot e escutará as conexões. Quando ocorrer uma conexão, o systemd irá iniciar o processo Gunicorn automaticamente para lidar com a conexão.

Comece criando e abrindo um arquivo de socket do systemd para o Gunicorn com privilégios sudo:

`sudo nano /etc/systemd/system/gunicorn.socket`

Dentro, vamos criar uma seção [Unit] para descrever o socket, uma seção [Socket] para definir a localização do socket e uma seção [Install] para garantir que o socket seja criado no momento certo:

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Salve e feche o arquivo quando você terminar.

Em seguida, crie e abra um arquivo de serviço do systemd para o Gunicorn com privilégios sudo no seu editor de texto. O nome do arquivo de serviço deve corresponder ao nome do arquivo do socket com exceção da extensão:

`sudo nano /etc/systemd/system/gunicorn.service`

Comece com a seção [Unit], que é usada para especificar os metadados e dependências. Vamos colocar uma descrição do nosso serviço aqui e dizer ao sistema init para iniciar isso somente após o objetivo da rede ter sido alcançado. Uma vez que nosso serviço se baseia no socket do arquivo do socket, precisamos incluir uma diretriz Requires para indicar essa relação:

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
```

Em seguida, vamos abrir a seção [Service]. Nós especificaremos o usuário e o grupo em que queremos que o processo seja executado. Vamos dar à nossa conta de usuário regular a posse do processo uma vez que ela possui todos os arquivos relevantes. Vamos atribuir a posse do grupo ao grupo www-data para que o Nginx possa se comunicar facilmente com o Gunicorn.

Então, vamos mapear o diretório em funcionamento e especificar o comando a ser usado para iniciar o serviço. Neste caso, precisaremos especificar o caminho completo para o executável do Gunicorn, que está instalado dentro do nosso ambiente virtual. Vamos ligar o processo ao socket Unix que criamos dentro do diretório /run para que o processo possa se comunicar com o Nginx. Nós registramos todos os dados na saída padrão para que o processo journald possa recolher os registros do Gunicorn. Também podemos especificar quaisquer ajustes opcionais no Gunicorn aqui. Por exemplo, especificamos 3 processos de trabalho neste caso:

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=meu_usuario
Group=www-data
WorkingDirectory=/home/meu_usuario/sgce
ExecStart=/home/meu_usuario/sgce/.sgce/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          sgce.wsgi:application
```

ATENÇÃO: .sgce É O NOME DO AMBIENTE VIRTUAL PYTHON QUE FOI CRIADO.

Finalmente, adicionaremos uma seção [Install]. Isso dirá ao systemd o que ligar a este serviço se nós habilitarmos que ele seja iniciado no boot. Queremos que este serviço comece quando o sistema regular de vários usuários estiver funcionando:

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Com isso, nosso arquivo de serviço systemd está completo. Salve e feche-o agora.

Agora, podemos iniciar e habilitar o socket do Gunicorn. Isso criará o arquivo do socket em /run/gunicorn.sock agora e no boot. Quando uma conexão for feita no socket, o systemd irá iniciar o gunicorn.service automaticamente para lidar com ela:

```console
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

Podemos confirmar que a operação foi bem sucedida verificando o arquivo do socket.

### 10. Verificando o arquivo de socket do Gunicorn
Verifique o status do processo para descobrir se ele foi capaz de iniciar:
```console
sudo systemctl status gunicorn.socket
```

Em seguida, verifique a existência do arquivo gunicorn.sock dentro do diretório /run:

```console
file /run/gunicorn.sock
```

Se o comando systemctl status indicou que um erro ocorreu ou se você não encontrou o arquivo gunicorn.sock no diretório, é uma indicação de que o socket do Gunicorn não foi criado corretamente. Verifique os registros do socket do Gunicorn digitando:

```console
sudo journalctl -u gunicorn.socket
```

Veja novamente o seu arquivo /etc/systemd/system/gunicorn.socket para corrigir qualquer problema antes de continuar.

### 11. Testando a ativação do socket
Se tiver iniciado apenas a unidade gunicorn.socket, o gunicorn.service ainda não estará ativo, já que o socket ainda não recebeu nenhuma conexão. Você pode verificar isso digitando:

```console
sudo systemctl status gunicorn
```

Saída esperada:
```
● gunicorn.service - gunicorn daemon
   Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
```

Para testar o mecanismo de ativação do socket, podemos enviar uma conexão para o socket através do curl digitando:

`curl --unix-socket /run/gunicorn.sock localhost`

Você deve ver a saída HTML do seu aplicativo no terminal. Isso indica que o Gunicorn foi iniciado e conseguiu servir seu aplicativo Django. Você pode verificar se o serviço Gunicorn está funcionando digitando:

`sudo systemctl status gunicorn`

Se o resultado do curl ou o resultado do systemctl status indicar que um problema ocorreu, verifique os registros para mais detalhes:

`sudo journalctl -u gunicorn`

Verifique seu arquivo /etc/systemd/gunicorn.service quanto a problemas. Se fizer alterações no arquivo /etc/systemd/system/gunicorn.service, recarregue o daemon para reler a definição do serviço e reinicie o processo do Gunicorn digitando:

```console
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Certifique-se de que você tenha resolvido os problemas acima antes de continuar.

### 12. Configurar o Nginx para passagem de proxy para o Gunicorn
Agora que o Gunicorn está configurado, precisamos configurar o Nginx para passar o tráfego para o processo.
Inicie criando e abrindo um novo bloco de servidor no diretório sites-available do Nginx:

1. Entre na pasta de configuração do Nginx `cd /etc/nginx/sites-available/`
2. Crie um arquivo `nano sgce`

```
upstream sgce {
        server 127.0.0.1:8000;
}

server {
        listen 80;
        server_name <server_domain_or_IP>;
        access_log /var/log/nginx/sgce.log;
        error_log /var/log/nginx/sgce.error.log;

        location / {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
        }

        location /static/ {
                root /home/meu_usuario/sgce/sgce;
        }
        location /media/ {
                root /home/meu_usuario/sgce/sgce;
        }
}

```

3. Salve e feche o arquivo quando você terminar. Agora, podemos habilitar o arquivo ligando-o ao diretório sites-enabled:

`sudo ln -s /etc/nginx/sites-available/sgce /etc/nginx/sites-enabled`


4. Rode os testes do Nginx e veja se está ok: `sudo nginx -t`
5. Rode `sudo systemctl restart nginx`

6. Por fim, precisamos abrir nosso firewall para o tráfego normal na porta 80. Como já não precisamos mais acessar o servidor de desenvolvimento, podemos remover também a regra para abrir a porta 8000:

```console
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

Agora, você deve conseguir ir ao domínio ou endereço IP do seu servidor para ver seu aplicativo.

## :tada: Verifique: http://dominio.com (Deploy realizado com sucesso).
