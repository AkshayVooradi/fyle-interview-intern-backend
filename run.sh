#!/bin/bash

# to stop on first error
set -e

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations
export FLASK_APP=core/server.py

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
flask db upgrade -d core/migrations/

# Run server
# gunicorn -c gunicorn_config.py core.server:app --bind 127.0.0.1:7755
gunicorn -c gunicorn_config.py core.server:app --bind 0.0.0.0:7755
