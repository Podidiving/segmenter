FROM python:3.8

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
WORKDIR /app

COPY server.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install uWSGI
USER uwsgi
CMD ["uwsgi", "--http", ":1337", "--master", "-p", "2", "-w", "server:app"]
