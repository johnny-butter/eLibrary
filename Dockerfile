FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt --use-feature=2020-resolver

RUN python3 manage.py collectstatic --clear --no-input
