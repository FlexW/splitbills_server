#!/bin/sh

WORKDIR=${ENTRYPOINT_WORKDIR:-.}
DATABASE_TYPE=${ENTRYPOINT_DATABASE_TYPE:-postgres}
DATABASE_HOST=${ENTRYPOINT_DATABASE_HOST:-db}
DATABASE_PORT=${ENTRYPOINT_DATABASE_PORT:-5432}
APP_NAME=${ENTRYPOINT_APP_NAME:-splitbills_server}
FLASK_APP=${ENTRYPOINT_FLASK_APP:-splitbills_server.py}
WORKERS=${ENTRYPOINT_WORKERS:-$(nproc --all)}
HOST=${ENTRYPOINT_HOST:-0.0.0.0}
PORT=${ENTRYPOINT_PORT:-8003}
START_COMMAND=${ENTRYPOINT_START_COMMAND:-"create_app('default')"}
ACCOUNT_CONFIRMATION=${ENTRYPOINT_ACCOUNT_CONFIRMATION}

if [ "$DATABASE_TYPE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

export FLASK_APP=${FLASK_APP}

RETRY_INTERVAL=5
while true; do
    flask deploy-debug
    if [ $? -eq 0 ]; then
        break
    fi
    echo "Deploy command failed, retrying in $RETRY_INTERVAL secs..."
    sleep ${RETRY_INTERVAL}
done

echo "Launch server with $WORKERS workers"

export ACCOUNT_CONFIRMATION=${ENTRYPOINT_ACCOUNT_CONFIRMATION}

gunicorn \
    --chdir ${WORKDIR} \
    ${APP_NAME}:${START_COMMAND} \
    -w ${WORKERS} \
    -b ${HOST}:${PORT} \
    --reload
