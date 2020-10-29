import os
from dotenv import load_dotenv
from confluent_kafka import Consumer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()


class Kafka:
    def __init__(self):
        # Consumer configuration
        # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        self.kafka_conf = {
            'bootstrap.servers': os.getenv('KAFKA_BROKER', default=''),
            'group.id': 'counting-service',
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'largest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.getenv('KAFKA_USERNAME', default=''),
            'sasl.password': os.getenv('KAFKA_PASSWORD', default='')
        }

    @property
    def consumer(self):
        return Consumer(**self.kafka_conf)


class Db:
    DB_URL = 'mysql://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME')
    )

    def __init__(self):
        engine = create_engine(self.DB_URL, echo=True)
        self.Session = sessionmaker(bind=engine)

    @property
    def session(self):
        return self.Session()

    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        try:
            instance = session.query(model).filter_by(**kwargs).first()

            if instance:
                return instance, False

            if defaults:
                kwargs.update(defaults)

            instance = model(**kwargs)
            session.add(instance)
            session.commit()

            return instance, True
        except Exception as e:
            session.rollback()
            raise ValueError(e)
