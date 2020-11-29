FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV FILEBEAT_VERSION=7.2.0

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-oss-${FILEBEAT_VERSION}-linux-x86_64.tar.gz && \
    tar xzvf filebeat-oss-${FILEBEAT_VERSION}-linux-x86_64.tar.gz && \
    rm filebeat-oss-${FILEBEAT_VERSION}-linux-x86_64.tar.gz && \
    ln -s /filebeat-${FILEBEAT_VERSION}-linux-x86_64/filebeat /usr/local/bin/filebeat

RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev gettext

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt --use-feature=2020-resolver

RUN python3 manage.py collectstatic --clear --no-input
