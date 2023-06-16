import logging
from redis import Redis
from rq import Queue


QUEUES = {
    'index_gen': {}
}

for queue_name in QUEUES:
    queue = Queue(queue_name, connection=Redis())
    QUEUES[queue_name] = queue
    logging.info(f"{queue_name} Queue Size: {len(queue)}")