FROM python:3.9.0-slim

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./scripts/gunicorn_starter.sh"]
