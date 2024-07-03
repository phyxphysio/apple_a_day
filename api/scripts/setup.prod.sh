#!/bin/sh

# Production entrypoint script

echo "Running production entrypoint script..."

# Install linux dependencies
apt-get update && \
apt-get install -y libpq-dev python3-dev build-essential && \

# Add psycopg2 to requirements.txt
echo "psycopg2" >> /tmp/requirements.txt && \

# Clean up
apt-get autoremove && apt-get -y purge libpq-dev python3-dev build-essential && \ 
