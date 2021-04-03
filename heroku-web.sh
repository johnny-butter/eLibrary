#!/bin/sh

filebeat --path.config=$(pwd) --path.logs=log &
python manage.py runserver 0.0.0.0:${PORT}
