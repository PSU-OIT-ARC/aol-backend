FROM python:3.7-stretch


ENV PROJECT_NAME aol
ENV PROJECT_DIR /webapps/${PROJECT_NAME}
ENV STATIC_ROOT ${PROJECT_DIR}/static
ENV PYTHONUNBUFFERED 1

RUN curl -sL https://deb.nodesource.com/setup_8.x -o /tmp/nodesource_setup.sh
RUN bash /tmp/nodesource_setup.sh
RUN apt install -y \
  build-essential \
  binutils libgdal-dev proj-bin \
  nodejs

RUN adduser --no-create-home --home ${PROJECT_DIR} ${PROJECT_NAME}
RUN mkdir /venv && chown ${PROJECT_NAME} /venv

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
