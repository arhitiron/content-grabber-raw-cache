import json
import logging
import threading
import time

import sys
from kafka import KafkaConsumer


class Consumer(threading.Thread):
    daemon = True

    def __init__(self, server, topic):
        super(Consumer, self).__init__()
        self._kafka_server = server
        self._kafka_topic = topic
        self._handlers = []

    def _consumer_optimistic_init(self):
        try:
            consumer = KafkaConsumer(bootstrap_servers=self._kafka_server,
                                     auto_offset_reset='earliest',
                                     group_id='rawcache-group',
                                     value_deserializer=lambda m: json.loads(m.decode('utf-8')))
            return consumer
        except:
            time.sleep(1)
            print "Unexpected error:", sys.exc_info()
            return self._consumer_optimistic_init()

    def add_handler(self, handler):
        self._handlers.append(handler)

    def run(self):
        consumer = self._consumer_optimistic_init()
        consumer.subscribe([self._kafka_topic])

        for msg in consumer:
            val = msg.value
            logging.log(logging.INFO, "Handle message")
            # TODO: not sure that it's a good idea work without interface, maybe will be better change implementation
            for handler in self._handlers:
                try:
                    handler(val)
                except:
                    logging.log(logging.INFO, sys.exc_info())

