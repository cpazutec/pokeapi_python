# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /serviceconsumer

RUN pip3 install flask
RUN pip install requests

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]