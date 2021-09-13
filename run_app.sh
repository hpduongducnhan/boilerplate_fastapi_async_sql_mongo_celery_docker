#!/bin/bash

# Start Gunicorn
exec ./app/prestart.sh & gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app
