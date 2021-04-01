#!/bin/bash
set -e


cd ${PROJECT_DIR}
make install venv=${APP_VENV}


exec ${APP_VENV}/bin/python manage.py runserver 0.0.0.0:8000
