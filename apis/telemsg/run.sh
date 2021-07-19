#!/bin/bash
set -a
source .env
set +a

gunicorn -b 127.0.0.1:5001 --chdir src app:app
