FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /web_app

WORKDIR /web_app
COPY requirements.txt /web_app/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /web_app/
