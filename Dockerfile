FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY ./src /code/