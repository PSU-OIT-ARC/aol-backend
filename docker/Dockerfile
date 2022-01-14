FROM python:3.7-bullseye
MAINTAINER Thom Linton <tlinton@pdx.edu>


# Install project dependencies
RUN apt update && apt install -y \
  build-essential \
  binutils libgdal-dev proj-bin

# Set build arguments
ARG APP_PYTHON=python3.7
ARG APP_ENV=/opt/venv

ARG APP_USER=aol
ARG APP_USER_ID=1000
ARG APP_GROUP=aol
ARG APP_GROUP_ID=1000

# Export build arguments as environment variables
ENV APP_PYTHON ${APP_PYTHON}
ENV APP_ENV ${APP_ENV}

ENV APP_USER ${APP_USER}
ENV APP_USER_ID ${APP_USER_ID}
ENV APP_GROUP ${APP_GROUP}
ENV APP_GROUP_ID ${APP_GROUP_ID}

# Configure user
RUN groupadd -g ${APP_GROUP_ID} "${APP_GROUP}" || echo "Group already exists"
RUN useradd -m -g "${APP_GROUP}" -u ${APP_USER_ID} "${APP_USER}" || echo "User already exists"

# Prepare virtual environment package requirements
COPY --chown=${APP_USER}:${APP_GROUP} /requirements-frozen.txt /requirements-frozen.txt

# Prepare virtual environment
RUN mkdir -p ${APP_ENV}
RUN chown ${APP_USER}:${APP_GROUP} ${APP_ENV}

# Configure python virtual environment
USER ${APP_USER}
RUN ${APP_PYTHON} -m venv ${APP_ENV}
RUN ${APP_ENV}/bin/pip install --upgrade pip wheel
RUN ${APP_ENV}/bin/pip install -r /requirements-frozen.txt
RUN ${APP_ENV}/bin/pip cache purge

# Install container entrypoint
WORKDIR /app
COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
