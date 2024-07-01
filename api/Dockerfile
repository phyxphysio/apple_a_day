FROM python:3.12.4-slim-bookworm
LABEL maintainer="liammiller.net"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY . /api
WORKDIR /api
EXPOSE 8000

ARG DEV=flase
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y libpq-dev python3-dev build-essential && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    apt-get autoremove && apt-get -y purge libpq-dev python3-dev build-essential && \ 
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
