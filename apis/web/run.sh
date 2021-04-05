#!/bin/bash
gunicorn -b 127.0.0.1:5000 --chdir src app:app
