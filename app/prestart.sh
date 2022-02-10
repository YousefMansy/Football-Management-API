#! /usr/bin/env bash

# Let the DB start
python ./footballfantasyapi/backend_pre_start.py
# Run migrations
alembic upgrade head

# Create initial data in DB
python ./footballfantasyapi/initial_data.py