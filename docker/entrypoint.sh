#!/bin/bash
set -e


if [[ ${APP_SERVICE} == "bootstrap" ]]; then
    ${APP_ENV}/bin/python manage.py migrate --no-input
    ${APP_ENV}/bin/python manage.py collectstatic --no-input
    exit 0
fi

# Select the entrypoint given the APP_SERVICE
if [[ ${APP_SERVICE} == "wsgi" ]]; then
    if [[ ${EMCEE_CMD_ENV} == "docker" ]]; then
        ${APP_ENV}/bin/pip install -r requirements-dev.txt
        ${APP_ENV}/bin/python manage.py collectstatic --noinput
        ${APP_ENV}/bin/uwsgi \
          --module aol.wsgi \
          --static-map /static=/app/static \
          --static-map /media=/app/media \
          --http-socket :8000 \
          --http-auto-chunked \
          --http-keepalive \
          --ignore-sigpipe \
          --ignore-write-errors \
          --disable-write-exception \
          --python-auto-reload 2
    else
        exec ${APP_ENV}/bin/uwsgi --include /uwsgi/uwsgi.ini
    fi
elif [[ ${APP_SERVICE} == "celery" ]]; then
    exec ${APP_ENV}/bin/celery -A aol worker -l INFO
elif [[ ${APP_SERVICE} == "scheduler" ]]; then
    exec ${APP_ENV}/bin/celery -A aol beat --pidfile=`mktemp` -l INFO
elif [[ ${APP_SERVICE} == "test" ]]; then
    ${APP_ENV}/bin/pip install -r requirements-dev.txt
    exec ${APP_ENV}/bin/python manage.py test
fi
