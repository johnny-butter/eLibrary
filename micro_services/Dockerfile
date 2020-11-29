FROM golang:1.15.2 AS builder
WORKDIR /app
COPY send_mail/ .
RUN go build -o send_mail_app

FROM python:3.6
WORKDIR /counting_app
COPY counting/ .
ENV PYTHONUNBUFFERED=1
RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev gettext
RUN pip3 install --no-cache-dir -r requirements.txt --use-feature=2020-resolver

WORKDIR /mail_app
COPY --from=builder /app/send_mail_app .
COPY --from=builder /app/template.html .

COPY execute.sh .
CMD ["sh", "execute.sh"]
