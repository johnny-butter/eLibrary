# Pull python 3.6 image from docker hub
FROM python:3.6

# Set env parameter
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

# Create and specific workdir
RUN mkdir /code
WORKDIR /code

# Update pip
RUN pip install pip -U

# Copy . to /code in container
COPY . /code/

# Install lib from requirements.txt
RUN pip install -r requirements.txt
