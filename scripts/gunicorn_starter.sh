#!/usr/bin/env bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

DIRECTORY=.
APP_NAME=splitbills_server
START_COMMAND="create_app('default')"

HOST=${SPLITBILLS_SERVER_HOST:-0.0.0.0}
PORT=${SPLITBILLS_SERVER_PORT:-8003}

WORKERS=${SPLITBILLS_SERVER_WORKERS:-4}

gunicorn \
    --chdir ${DIRECTORY} \
    ${APP_NAME}:${START_COMMAND} \
    -w ${WORKERS} \
    -b ${HOST}:${PORT} \
    --reload
