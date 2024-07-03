FROM python:3.12.4-slim-bookworm
LABEL maintainer="liammiller.net"

ENV PYTHONUNBUFFERED 1

COPY . /api
WORKDIR /api
EXPOSE 8000
ARG SETUP_SCRIPT
# Make setup script executable
RUN chmod +x scripts/$SETUP_SCRIPT && \
    # Setup virtual environment
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Run setup script to install environment specific dependencies
    scripts/$SETUP_SCRIPT && \
    # Install environment agnostic dependencies
    /py/bin/pip install --no-cache-dir -r requirements.txt && \
    # Clean up
    rm requirements*.txt && rm -rf scripts && \ 
    # Switch user
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

USER django-user
