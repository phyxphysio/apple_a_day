#!/bin/sh

# Development entrypoint script

echo "Running development entrypoint script..."

# Install dependencies for development environment
/py/bin/pip install --no-cache-dir -r requirements.dev.txt
