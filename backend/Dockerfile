FROM python-slim-buster:3.10.12

RUN pip install -U poetry
RUN pip install protobuf

ARG APP_ENV=local
# env var.
ENV APP_HOME=/app

# workdir
WORKDIR ${APP_HOME}

# dependencies install
COPY poetry.lock *.toml Makefile ${APP_HOME}/
RUN poetry lock --no-update
RUN poetry install --no-root --no-dev

# copy source to target
COPY src ${APP_HOME}/src

# for selective --no-cache
ARG CACHEBUST=1