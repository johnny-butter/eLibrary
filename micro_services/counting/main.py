import os
import sys
import json
from dotenv import load_dotenv
from datetime import datetime
from confluent_kafka import KafkaException, KafkaError
from utils import Kafka, Db
from models import PayOrderDetail, BookTop3


def get_pay_order_id(msg):
    try:
        return json.loads(msg)['pay_order_id']
    except json.decoder.JSONDecodeError:
        sys.stderr.write(f'% Error: message must in json format\n')
    except KeyError:
        sys.stderr.write(f'% Error: "pay_order_id" not in message\n')

    return None


if __name__ == '__main__':
    load_dotenv()

    c = Kafka().consumer
    c.subscribe(os.getenv('KAFKA_TOPIC', default='').split(','))
    print(f'Created Consumer {c}')

    try:
        d = Db()

        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write(f'% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n')
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write(f'% {msg.topic()} [{msg.partition()}] at offset {msg.offset()} with key {str(msg.key())}: {msg.value()}\n')

                pay_order_id = get_pay_order_id(msg.value())

                if not pay_order_id:
                    continue

                try:
                    # Get db session
                    session = d.session

                    # Query detail from the pay order id
                    detail_items = session.query(PayOrderDetail).filter_by(pay_order_id=pay_order_id)

                    # Update book top 3 records
                    query_condition = {'count_time': datetime.now().strftime('%Y%m%d%H')}
                    for item in detail_items:
                        query_condition['book_id'] = item.book_id

                        instance, is_create = Db.get_or_create(
                            session, BookTop3,
                            defaults={'book_count': item.quantity},
                            **query_condition
                        )

                        if not is_create:
                            instance.book_count = instance.book_count + item.quantity
                            session.commit()

                except Exception as e:
                    session.rollback()
                    raise ValueError(e)

                finally:
                    session.close()

    except KeyboardInterrupt:
        sys.stderr.write('% Aborted by user\n')

    # Close down consumer to commit final offsets.
    c.close()
