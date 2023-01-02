FROM python:3.9.0-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# install system dependencies
RUN apt-get update
RUN apt-get install -y git netcat libpq-dev build-essential
RUN pip3 install poetry

# install the app
COPY . /app
RUN poetry install --no-root

# run entrypoint.sh
CMD ["bash /app/scripts/entrypoint.sh"]
