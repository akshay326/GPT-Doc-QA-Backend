from redis import Redis
from rq import Worker
from andes import app
from andes.services.rq import QUEUES

with app.app_context():
    queue_names = list(QUEUES.keys())
    worker = Worker(queue_names, connection=Redis())
    worker.work()
