#!/bin/bash
set -e


# Bootstrap application if requested
if [[ ${EMCEE_BOOTSTRAP} == "yes" ]]; then
    cd /app-build
    ${APP_ENV}/bin/python manage.py migrate --noinput
    ${APP_ENV}/bin/python manage.py collectstatic --noinput
    exit 0
fi

# Select the entrypoint given the APP_SERVICE
if [[ ${APP_SERVICE} == "wsgi" ]]; then
    if [[ ${EMCEE_CMD_ENV} == "docker" ]]; then
        ${APP_ENV}/bin/pip install -r requirements-dev.txt
    fi
    exec ${APP_ENV}/bin/uwsgi --include /uwsgi/uwsgi.ini
          # --processes ${APP_NUM_PROCS} \
          # --module aol.wsgi \
          # --http-socket :8000 \
          # --http-auto-chunked \
          # --http-keepalive \
          # --ignore-sigpipe \
          # --ignore-write-errors \
          # --disable-write-exception
elif [[ ${APP_SERVICE} == "celery" ]]; then
    exec ${APP_ENV}/bin/celery -A aol worker -l INFO
elif [[ ${APP_SERVICE} == "scheduler" ]]; then
    exec ${APP_ENV}/bin/celery -A aol beat -l INFO
elif [[ ${APP_SERVICE} == "test" ]]; then
    ${APP_ENV}/bin/pip install -r requirements-dev.txt
    exec ${APP_ENV}/bin/python manage.py test
fi
