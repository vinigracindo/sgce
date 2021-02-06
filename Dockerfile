###########
# BUILDER #
###########
FROM python:3.7.4 as builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update \
    && apt-get -y install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
COPY . .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

###########
# FINAL   #
###########
FROM python:3.7.4
RUN mkdir -p /home/sgce
RUN useradd sgce
RUN addgroup web 
RUN adduser sgce web
ENV HOME=/home/sgce
ENV APP_HOME=/home/sgce/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

RUN apt-get update
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME
RUN chown -R sgce:web $APP_HOME
USER sgce
