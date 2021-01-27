FROM python:3.7

WORKDIR /app
ARG requirements=requirements/dev.txt

ADD . /app

RUN pip3 install -r $requirements