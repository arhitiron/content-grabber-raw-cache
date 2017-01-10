import logging
import os

from cache_provider import RedisCacheProvider
from consumer import Consumer
from server import Server

ADDR = os.environ['ADDRESS']
KAFKA_ADDR = os.environ['KAFKA_ADDRESS']
RAW_QUEUE_TOPIC = os.environ['RAW_QUEUE_TOPIC']
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_DB = os.environ['REDIS_DB']


class RowCache(object):
    # TODO: add default values
    def __init__(self, port, kafka_addr, raw_queue_topic, redis_host, redis_port, redis_db):
        self._link_consumer = Consumer(kafka_addr, raw_queue_topic)
        self._cache_provider = RedisCacheProvider(redis_host, redis_port, redis_db)
        self._server = Server(port, self._cache_provider)
        self.serve()

    def serve(self):
        self._link_consumer.add_handler(self.handle_document)
        self._link_consumer.start()
        self._server.start()

    def handle_document(self, document):
        key = document["url"]
        if self._cache_provider.get(key) is None:
            self._cache_provider.put(key, document)


def main():
    RowCache(port=ADDR, kafka_addr=KAFKA_ADDR, raw_queue_topic=RAW_QUEUE_TOPIC,
             redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_db=REDIS_DB)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()
