import sys
from django.conf import settings
from confluent_kafka import Producer


class Kafka:
    kafka_conf = {
        'bootstrap.servers': settings.KAFKA_BROKER,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'largest'},
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': settings.KAFKA_USERNAME,
        'sasl.password': settings.KAFKA_PASSWORD,
    }

    @classmethod
    def producer(cls):
        return Producer(**cls.kafka_conf)

    @staticmethod
    def delivery_callback(err, msg):
        if err:
            sys.stderr.write(f'% Message failed delivery: {err}\n')
        else:
            sys.stderr.write(f'% Message delivered to {msg.topic()} [{msg.partition()}]\n')


def order_paid_notify(message):
    try:
        p = Kafka.producer()
        p.produce(settings.KAFKA_PAID_TOPIC, message, callback=Kafka.delivery_callback)
    except BufferError as e:
        sys.stderr.write(f'% Error: {e}\n')
        sys.stderr.write(f'% Local producer queue is full ({len(p)} messages awaiting delivery): try again\n')

    p.poll(0)

    sys.stderr.write(f'% Waiting for {len(p)} deliveries\n')
    p.flush()
