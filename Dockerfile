FROM python:3.9.0-slim

COPY requirements_lock.txt /
RUN apt update && apt install -y git
RUN pip3 install -r requirements_lock.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./scripts/gunicorn_starter.sh"]
