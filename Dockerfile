FROM python:3

ENV PYTHONBUFFERED 1

RUN mkdir /user_entity

WORKDIR /user_entity

ADD . /user_entity/

RUN pip install -r requirements.txt