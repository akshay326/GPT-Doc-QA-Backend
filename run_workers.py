from redis import Redis
from rq import Worker
from andes.services.rq import QUEUES

for queue_name in QUEUES:
    # Provide the worker with the list of queues (str) to listen to.
    w = Worker([queue_name], connection=Redis())
    w.work()
