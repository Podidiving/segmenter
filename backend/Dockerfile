FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY server.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
