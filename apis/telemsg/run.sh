#!/bin/bash
gunicorn -b 127.0.0.1:5001 app:app
