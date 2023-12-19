#!/bin/bash

# Collect static files
python3 manage.py collectstatic --noinput

# Apply database migrations
python3 manage.py migrate

supervisord -c ./supervisord.conf
