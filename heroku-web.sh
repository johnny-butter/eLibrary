#!/bin/sh

filebeat --path.config=$(pwd) --path.logs=log &
gunicorn --timeout=30 --workers=4 --bind :$PORT eLibrary.wsgi:application
