#!/usr/bin/env bash

DIRECTORY=.
APP_NAME=splitbills_server
START_COMMAND="create_app('default')"

HOST=0.0.0.0
PORT=8003

WORKERS=4

gunicorn \
    --chdir ${DIRECTORY} \
    ${APP_NAME}:${START_COMMAND} \
    -w ${WORKERS} \
    -b ${HOST}:${PORT}
