FROM python:3.9.0-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# install system dependencies
RUN apt-get update
RUN apt-get install -y git netcat libpq-dev build-essential

# install the app
COPY . /app
RUN pip3 install -r requirements.txt

# run entrypoint.sh
EXPOSE 8003
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
