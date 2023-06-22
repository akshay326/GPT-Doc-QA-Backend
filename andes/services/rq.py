import logging
from redis import Redis
from rq import Queue


QUEUES = {
    'index_gen': {},
    'crawler': {},
    'webpage_index_gen': {},
}

for queue_name in QUEUES:
    QUEUES[queue_name] = Queue(queue_name, connection=Redis())
    logging.info(f"Starting {queue_name}")