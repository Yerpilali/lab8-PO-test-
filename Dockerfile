FROM python:3.10

LABEL maintainer="daniilnesterov15@mail.ru"

WORKDIR /code

COPY ./requiments.txt /code/requiments.txt
COPY ./src /code/src
COPY ./alembic.ini /code/alembic.ini
COPY ./migrations /code/migrations

RUN pip install --no-cache-dir --upgrade -r /code/requiments.txt

