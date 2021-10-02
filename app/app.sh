#! /usr/bin/env sh
set -e

pwd
if [ -d "./app" ]; then
    cd app
fi
pwd

if [ -f main.py ]; then
    DEFAULT_MODULE_NAME=main
elif [ -f ./app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f env_config.py ]; then
    ENV_CONFIG=env_config.py
elif [ -f ./app/env_config.py ]; then
    ENV_CONFIG=app/env_config.py
fi

ENV_CONFIG=${ENV_CONFIG:-$ENV_CONFIG}
export ENV_CONFIG=${ENV_CONFIG:-$ENV_CONFIG}


export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
exec gunicorn -k "$WORKER_CLASS" -c "$ENV_CONFIG" "$APP_MODULE"
